import pytest
from tools.cart_tools import cart_tools
from tools.order_tools import order_tools
from tools.payment_tools import payment_tools

def test_cart_operations():
    cart = []
    prod1 = {"product_id": "PROD-TEST-1", "product_name": "Test Earbuds", "price": 2000.0}
    
    # Add Item
    cart = cart_tools.add_to_cart(cart, prod1, quantity=2)
    assert len(cart) == 1
    assert cart[0]["subtotal"] == 4000.0

    # Calculate Total (Order > ₹1000 has free delivery)
    summary = cart_tools.calculate_cart_total(cart)
    assert summary["subtotal"] == 4000.0
    assert summary["shipping_fee"] == 0.0
    assert summary["total_payable"] == 4000.0

    # Remove Item
    cart = cart_tools.remove_from_cart(cart, "PROD-TEST-1")
    assert len(cart) == 0

def test_order_and_payment_state_machine():
    customer_id = "CUST-TEST-001"
    items = [{"product_id": "PROD-AUD-001", "product_name": "SonicPulse Pro", "price": 4799.0, "quantity": 1}]
    amount = 4799.0

    # 1. Create Order
    order = order_tools.create_order(customer_id, items, amount)
    assert order["order_id"].startswith("ORD-")
    assert order["order_status"] == "PENDING"

    # 2. Initiate Payment (Requires HITL Confirmation)
    txn = payment_tools.initiate_payment(
        order_id=order["order_id"],
        customer_id=customer_id,
        amount=amount,
        payment_method="UPI"
    )
    assert txn["status"] == "INITIATED"
    assert txn["requires_human_confirmation"] is True

    # 3. Confirm and Process Payment (Success Case)
    confirmed = payment_tools.confirm_and_process_payment(txn["transaction_id"], simulate_failure=False)
    assert confirmed["status"] == "SUCCESS"
    assert confirmed["is_confirmed"] is True

    # Check updated order
    ord_details = order_tools.get_order_status(order["order_id"])
    assert ord_details["order_status"] == "COMPLETED"
    assert ord_details["payment_status"] == "SUCCESS"

def test_payment_failure_simulation():
    customer_id = "CUST-TEST-002"
    items = [{"product_id": "PROD-AUD-001", "product_name": "SonicPulse Pro", "price": 4799.0, "quantity": 1}]
    amount = 4799.0

    order = order_tools.create_order(customer_id, items, amount)
    txn = payment_tools.initiate_payment(order["order_id"], customer_id, amount, "Card")
    
    # Confirm with simulated failure
    confirmed = payment_tools.confirm_and_process_payment(
        txn["transaction_id"],
        simulate_failure=True,
        failure_reason="BANK_DECLINED"
    )
    assert confirmed["status"] == "FAILED"
    assert confirmed["failure_reason"] == "BANK_DECLINED"

    ord_details = order_tools.get_order_status(order["order_id"])
    assert ord_details["order_status"] == "CANCELLED"
    assert ord_details["payment_status"] == "FAILED"
