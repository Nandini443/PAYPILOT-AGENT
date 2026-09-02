from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List
from agents.merchant_agent import merchant_agent
from agents.state import MerchantSessionState
from analytics.metrics import analytics_service
from analytics.growth_engine import growth_engine

merchant_router = APIRouter(prefix="/api/merchant", tags=["Merchant Growth"])

class MerchantQuestionRequest(BaseModel):
    question: str
    session_id: str = "merchant_session"

@merchant_router.get("/kpis")
def get_kpis():
    return analytics_service.get_executive_summary()

@merchant_router.get("/funnel")
def get_funnel():
    return analytics_service.get_funnel_metrics()

@merchant_router.get("/payments")
def get_payment_performance():
    return {
        "methods": analytics_service.get_payment_method_performance(),
        "failures": analytics_service.get_payment_failure_breakdown(),
        "overall": analytics_service.calculate_payment_success_rate()
    }

@merchant_router.get("/opportunities")
def get_opportunities():
    return growth_engine.detect_all_opportunities()

@merchant_router.get("/top-products")
def get_top_products(limit: int = 5):
    return analytics_service.get_top_products(limit=limit)

@merchant_router.post("/ask")
def ask_merchant_copilot(req: MerchantQuestionRequest):
    state = MerchantSessionState(session_id=req.session_id)
    return merchant_agent.answer_query(req.question, state)
