from typing import Dict, Any, List, Optional
from agents.customer_agent import customer_agent, CustomerShoppingAgent
from agents.merchant_agent import merchant_agent, MerchantGrowthAgent
from agents.state import CustomerSessionState, MerchantSessionState

class PayPilotAIEngine:
    """Unified AI Engine orchestrating both Customer and Merchant agentic workflows."""

    def __init__(self):
        self.customer = customer_agent
        self.merchant = merchant_agent

    def handle_customer_request(self, query: str, state: CustomerSessionState) -> Dict[str, Any]:
        return self.customer.process_shopping_query(query, state)

    def handle_merchant_request(self, query: str, state: MerchantSessionState) -> Dict[str, Any]:
        return self.merchant.answer_query(query, state)

ai_engine = PayPilotAIEngine()
