from typing import Dict, Any, List, Optional
from agents.state import CustomerSessionState, CustomerIntent, AgentExecutionStep
from tools.product_tools import product_tools, ProductTools
from tools.cart_tools import cart_tools, CartTools
from tools.order_tools import order_tools, OrderTools
from tools.payment_tools import payment_tools, PaymentTools
from ai.llm_client import llm_client, LLMClient
from agents.planner import agent_planner, AgentPlanner

class CustomerShoppingAgent:
    """
    Autonomous AI Shopping Agent guiding customers through requirements analysis,
    catalog discovery, comparative ranking, cart management, and safe HITL checkout.
    """

    def __init__(
        self,
        p_tools: Optional[ProductTools] = None,
        c_tools: Optional[CartTools] = None,
        o_tools: Optional[OrderTools] = None,
        pay_tools: Optional[PaymentTools] = None,
        llm: Optional[LLMClient] = None,
        planner: Optional[AgentPlanner] = None
    ):
        self.product_tools = p_tools or product_tools
        self.cart_tools = c_tools or cart_tools
        self.order_tools = o_tools or order_tools
        self.payment_tools = pay_tools or payment_tools
        self.llm = llm or llm_client
        self.planner = planner or agent_planner

    def process_shopping_query(self, query: str, state: CustomerSessionState) -> Dict[str, Any]:
        """
        Full agentic discovery pipeline:
        1. Extract Intent
        2. Formulate Plan & Steps
        3. Search Catalog
        4. Rank & Score Products
        5. Formulate Top Selection & Explanation
        """
        # Step 1: Extract Intent
        intent: CustomerIntent = self.llm.extract_intent(query)
        state.intent = intent

        # Step 2: Formulate Planner Steps
        steps = self.planner.create_customer_shopping_plan(intent)
        state.activity_log.extend(steps)

        # Step 3: Search Catalog
        raw_candidates = self.product_tools.search_products(
            query=intent.raw_query,
            category=intent.category,
            max_price=intent.budget,
            min_rating=intent.min_rating,
            limit=15
        )

        # Fallback: try progressively broader searches
        if not raw_candidates and intent.category:
            # Try category-only search (drop price/rating filters)
            raw_candidates = self.product_tools.search_products(query="", category=intent.category, limit=10)
        
        if not raw_candidates and intent.budget:
            # Try budget-only search across all categories
            raw_candidates = self.product_tools.search_products(query=intent.raw_query, max_price=intent.budget, limit=10)
        
        if not raw_candidates:
            # Final fallback: browse all products
            raw_candidates = self.product_tools.search_products(query="", limit=15)

        # Step 4: Rank Products
        ranked_products = self.product_tools.rank_products(
            products=raw_candidates,
            user_intent=intent.model_dump()
        )

        top_candidates = ranked_products[:6] if ranked_products else []
        best_pick = top_candidates[0] if top_candidates else None

        state.recommended_products = top_candidates
        state.best_recommendation = best_pick

        # Step 5: Synthesize Decision Rationale
        explanation = self._build_decision_explanation(best_pick, intent)

        return {
            "intent": intent.model_dump(),
            "recommended_products": top_candidates,
            "best_match": best_pick,
            "decision_explanation": explanation,
            "activity_steps": [s.model_dump() for s in steps]
        }

    def _build_decision_explanation(self, best_pick: Optional[Dict[str, Any]], intent: CustomerIntent) -> str:
        if not best_pick:
            return "No products matching your exact criteria were found in our catalog. Please try adjusting your budget or search terms."

        reasons = best_pick.get("match_reasons", [])
        reasons_bullet = "\n".join([f"• {r}" for r in reasons])
        
        return (
            f"I recommend the **{best_pick['product_name']}** as your top option.\n\n"
            f"**Why this product stands out:**\n"
            f"{reasons_bullet}\n\n"
            f"It offers a **{best_pick.get('ai_match_score', 95)}% AI Match Score** for your requirements "
            f"at ₹{best_pick['price']:,.2f} with a {best_pick['rating']}★ customer rating."
        )

    def prepare_checkout(
        self,
        product_id: str,
        state: CustomerSessionState,
        payment_method: str = "UPI"
    ) -> Dict[str, Any]:
        """
        Prepares order and initiates simulated payment session.
        Stops at INITIATED state to require explicit human confirmation.
        """
        product = self.product_tools.get_product_details(product_id)
        if not product:
            return {"success": False, "error": "Product not found."}

        # Update cart
        state.cart = self.cart_tools.clear_cart()
        state.cart = self.cart_tools.add_to_cart(state.cart, product, quantity=1)
        cart_summary = self.cart_tools.calculate_cart_total(state.cart)

        # Create Pending Order
        order = self.order_tools.create_order(
            customer_id=state.customer_id,
            items=state.cart,
            amount=cart_summary["total_payable"]
        )
        state.active_order = order

        # Initiate Payment (Requires Human Confirmation)
        txn = self.payment_tools.initiate_payment(
            order_id=order["order_id"],
            customer_id=state.customer_id,
            amount=cart_summary["total_payable"],
            payment_method=payment_method,
            product_id=product_id
        )
        state.active_transaction = txn

        # Log steps
        steps = self.planner.create_checkout_plan(product["product_name"], cart_summary["total_payable"], payment_method)
        state.activity_log.extend(steps)

        return {
            "success": True,
            "order": order,
            "transaction": txn,
            "cart_summary": cart_summary,
            "product": product,
            "requires_confirmation": True
        }

    def finalize_payment(
        self,
        state: CustomerSessionState,
        simulate_failure: bool = False,
        failure_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes payment after explicit human confirmation button is pressed.
        """
        if not state.active_transaction:
            return {"success": False, "error": "No active payment session found."}

        txn_id = state.active_transaction["transaction_id"]
        result = self.payment_tools.confirm_and_process_payment(
            transaction_id=txn_id,
            simulate_failure=simulate_failure,
            failure_reason=failure_reason
        )

        state.active_transaction = result
        if result["status"] == "SUCCESS" and state.active_order:
            state.active_order["order_status"] = "COMPLETED"
            state.active_order["payment_status"] = "SUCCESS"
            # Clear cart on successful purchase
            state.cart = self.cart_tools.clear_cart()

            state.activity_log.append(AgentExecutionStep(
                step_id="PAY-FINISH",
                title="Payment confirmed & verified",
                tool_name="confirm_payment",
                status="COMPLETED",
                details=f"Transaction {txn_id} verified via {result['payment_method']}. Order confirmed."
            ))
        else:
            state.activity_log.append(AgentExecutionStep(
                step_id="PAY-DECLINED",
                title="Payment processing halted",
                tool_name="confirm_payment",
                status="FAILED",
                details=f"Transaction failed with reason: {result.get('failure_reason', 'UNKNOWN')}"
            ))

        return result

customer_agent = CustomerShoppingAgent()
