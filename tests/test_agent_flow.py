import pytest
from agents.customer_agent import customer_agent
from agents.merchant_agent import merchant_agent
from agents.state import CustomerSessionState, MerchantSessionState

def test_customer_agent_end_to_end_flow():
    state = CustomerSessionState(session_id="test_cust_session")
    query = "I need wireless headphones under ₹5,000 with good battery life"
    
    # 1. Process Discovery Query
    res = customer_agent.process_shopping_query(query, state)
    assert len(res["recommended_products"]) > 0
    best_prod = res["best_match"]
    assert best_prod is not None
    assert best_prod["price"] <= 5000.0
    assert len(state.activity_log) >= 5

    # 2. Prepare Checkout (Cart + Order + Payment INITIATED)
    chk_res = customer_agent.prepare_checkout(best_prod["product_id"], state, payment_method="UPI")
    assert chk_res["success"] is True
    assert chk_res["requires_confirmation"] is True
    assert state.active_transaction["status"] == "INITIATED"

    # 3. Finalize Payment (Human approves)
    pay_res = customer_agent.finalize_payment(state, simulate_failure=False)
    assert pay_res["status"] == "SUCCESS"
    assert state.active_order["order_status"] == "COMPLETED"
    assert len(state.cart) == 0 # Cart cleared on purchase

def test_merchant_agent_query_flow():
    state = MerchantSessionState(session_id="test_merch_session")
    query = "Why did conversion drop this week?"
    
    res = merchant_agent.answer_query(query, state)
    assert "finding" in res
    assert "evidence" in res
    assert "recommendation" in res
    assert len(state.chat_history) == 1
