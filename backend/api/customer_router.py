from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from agents.customer_agent import customer_agent
from agents.state import CustomerSessionState
from tools.product_tools import product_tools
from tools.cart_tools import cart_tools
from tools.order_tools import order_tools
from tools.payment_tools import payment_tools

customer_router = APIRouter(prefix="/api/customer", tags=["Customer Commerce"])

class CustomerSearchRequest(BaseModel):
    query: str
    session_id: str = "default_session"

class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int = 1
    cart: List[Dict[str, Any]] = Field(default_factory=list)

class PrepareCheckoutRequest(BaseModel):
    product_id: str
    payment_method: str = "UPI"
    customer_id: str = "CUST-DEMO-001"

class ConfirmPaymentRequest(BaseModel):
    transaction_id: str
    simulate_failure: bool = False
    failure_reason: Optional[str] = None

@customer_router.post("/search")
def search_and_rank(req: CustomerSearchRequest):
    state = CustomerSessionState(session_id=req.session_id)
    res = customer_agent.process_shopping_query(req.query, state)
    return res

@customer_router.get("/products/{product_id}")
def get_product(product_id: str):
    product = product_tools.get_product_details(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@customer_router.post("/cart/calculate")
def calculate_cart(cart_items: List[Dict[str, Any]]):
    return cart_tools.calculate_cart_total(cart_items)

@customer_router.post("/checkout/prepare")
def prepare_checkout_endpoint(req: PrepareCheckoutRequest):
    state = CustomerSessionState(session_id="session_chk", customer_id=req.customer_id)
    res = customer_agent.prepare_checkout(req.product_id, state, req.payment_method)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Checkout preparation failed"))
    return res

@customer_router.post("/checkout/confirm")
def confirm_payment_endpoint(req: ConfirmPaymentRequest):
    res = payment_tools.confirm_and_process_payment(
        transaction_id=req.transaction_id,
        simulate_failure=req.simulate_failure,
        failure_reason=req.failure_reason
    )
    return res

@customer_router.get("/orders/{order_id}")
def get_order(order_id: str):
    order = order_tools.get_order_status(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
