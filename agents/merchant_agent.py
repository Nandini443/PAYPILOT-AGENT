from typing import Dict, Any, List, Optional
from agents.state import MerchantSessionState
from tools.analytics_tools import analytics_tools, AnalyticsTools
from ai.llm_client import llm_client, LLMClient

class MerchantGrowthAgent:
    """
    Autonomous Merchant Growth Agent analyzing synthetic commerce/payment telemetry
    to detect lost revenue, diagnose conversion drop-offs, and recommend high-impact growth actions.
    """

    def __init__(
        self,
        a_tools: Optional[AnalyticsTools] = None,
        llm: Optional[LLMClient] = None
    ):
        self.analytics_tools = a_tools or analytics_tools
        self.llm = llm or llm_client

    def answer_query(self, query: str, state: MerchantSessionState) -> Dict[str, Any]:
        """
        Processes natural language merchant question with guaranteed zero data hallucination.
        """
        # Step 1: Query deterministic insights engine
        analysis = self.analytics_tools.answer_merchant_nl_question(query)

        # Step 2: Record in session history
        chat_item = {
            "query": query,
            "response": analysis,
            "timestamp": "Now"
        }
        state.chat_history.append(chat_item)

        return analysis

    def get_growth_opportunities(self) -> List[Dict[str, Any]]:
        """Fetch all 6 growth opportunity vectors with severity & experiments."""
        return self.analytics_tools.detect_growth_opportunities()

    def get_dashboard_kpis(self) -> Dict[str, Any]:
        """Fetch real-time executive dashboard KPIs."""
        return self.analytics_tools.query_sales_data()

merchant_agent = MerchantGrowthAgent()
