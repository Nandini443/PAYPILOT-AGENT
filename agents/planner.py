from typing import List, Dict, Any, Optional
from agents.state import AgentExecutionStep, CustomerIntent

class AgentPlanner:
    """
    Formulates executable multi-step plans for customer commerce intents and merchant growth tasks.
    Produces user-friendly activity milestones without exposing raw inner chain-of-thought.
    """

    @staticmethod
    def create_customer_shopping_plan(intent: CustomerIntent) -> List[AgentExecutionStep]:
        """Generate structured plan for customer product discovery."""
        budget_str = f" under ₹{intent.budget:,.0f}" if intent.budget else ""
        cat_str = f" for '{intent.category}'" if intent.category else ""
        
        return [
            AgentExecutionStep(
                step_id="STEP-1",
                title="Understanding user shopping intent",
                tool_name="intent_extractor",
                status="COMPLETED",
                details=f"Extracted requirements: category={intent.category or 'All'}, budget={budget_str or 'None'}, preferences={', '.join(intent.preferences) or 'General'}"
            ),
            AgentExecutionStep(
                step_id="STEP-2",
                title="Searching product catalog",
                tool_name="search_products",
                status="COMPLETED",
                details=f"Querying catalog{cat_str}{budget_str}"
            ),
            AgentExecutionStep(
                step_id="STEP-3",
                title="Filtering candidates & checking stock",
                tool_name="filter_products",
                status="COMPLETED",
                details="Evaluating pricing boundaries, ratings, and active inventory"
            ),
            AgentExecutionStep(
                step_id="STEP-4",
                title="Scoring & ranking best options",
                tool_name="rank_products",
                status="COMPLETED",
                details="Computing AI match scores (0-100%) against user preferences"
            ),
            AgentExecutionStep(
                step_id="STEP-5",
                title="Formulating recommendation & decision rationale",
                tool_name="explain_selection",
                status="COMPLETED",
                details="Synthesizing key purchase drivers (battery life, reviews, value)"
            )
        ]

    @staticmethod
    def create_checkout_plan(product_name: str, amount: float, method: str) -> List[AgentExecutionStep]:
        """Generate structured plan for checkout & payment sequence."""
        return [
            AgentExecutionStep(
                step_id="CHK-1",
                title=f"Added '{product_name}' to cart",
                tool_name="add_to_cart",
                status="COMPLETED",
                details=f"1 item added at ₹{amount:,.2f}"
            ),
            AgentExecutionStep(
                step_id="CHK-2",
                title="Calculated order breakdown & taxes",
                tool_name="calculate_cart_total",
                status="COMPLETED",
                details=f"Subtotal: ₹{amount:,.2f}, GST included, Free delivery eligible"
            ),
            AgentExecutionStep(
                step_id="CHK-3",
                title="Created pending order",
                tool_name="create_order",
                status="COMPLETED",
                details="Order record initialized in database"
            ),
            AgentExecutionStep(
                step_id="CHK-4",
                title=f"Initiated {method} payment session",
                tool_name="initiate_payment",
                status="COMPLETED",
                details="Transaction state set to INITIATED. Human approval required."
            )
        ]

agent_planner = AgentPlanner()
