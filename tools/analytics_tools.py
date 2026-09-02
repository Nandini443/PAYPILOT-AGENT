from typing import Dict, Any, List, Optional
from analytics.metrics import analytics_service, AnalyticsService
from analytics.growth_engine import growth_engine, GrowthOpportunityEngine
from analytics.insights import insights_engine, MerchantInsightsEngine

class AnalyticsTools:
    """Agent tool wrapper for merchant growth analytics and opportunity discovery."""

    def __init__(
        self,
        service: Optional[AnalyticsService] = None,
        engine: Optional[GrowthOpportunityEngine] = None,
        insights: Optional[MerchantInsightsEngine] = None
    ):
        self.analytics = service or analytics_service
        self.growth = engine or growth_engine
        self.insights = insights or insights_engine

    def query_sales_data(self) -> Dict[str, Any]:
        """Tool: Query revenue, total orders, and average order value."""
        return self.analytics.get_executive_summary()

    def query_payment_data(self) -> Dict[str, Any]:
        """Tool: Query payment success rates, latencies, and failure breakdowns."""
        methods = self.analytics.get_payment_method_performance()
        failures = self.analytics.get_payment_failure_breakdown()
        rates = self.analytics.calculate_payment_success_rate()
        return {
            "overall_payment_metrics": rates,
            "method_breakdown": methods,
            "failure_reasons": failures
        }

    def analyze_conversion(self) -> Dict[str, Any]:
        """Tool: Analyze conversion funnel, checkout drop-off, and price-bracket abandonment."""
        conv = self.analytics.calculate_conversion_rate()
        abandon = self.analytics.calculate_checkout_abandonment()
        funnel = self.analytics.get_funnel_metrics()
        return {
            "conversion_summary": conv,
            "abandonment_breakdown": abandon,
            "funnel_stages": funnel
        }

    def detect_growth_opportunities(self) -> List[Dict[str, Any]]:
        """Tool: Scan telemetry and return structured growth vectors with evidence."""
        return self.growth.detect_all_opportunities()

    def answer_merchant_nl_question(self, question: str) -> Dict[str, Any]:
        """Tool: Translate merchant question into verified data finding, evidence, and recommendation."""
        return self.insights.answer_question(question)

analytics_tools = AnalyticsTools()
