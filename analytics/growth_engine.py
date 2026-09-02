from typing import List, Dict, Any, Optional
from database.database import db, Database
from analytics.metrics import AnalyticsService, analytics_service

class GrowthOpportunityEngine:
    """
    Automated Growth Engine that scans synthetic commerce and payment data
    to detect high-leverage business opportunities with actionable experiments.
    """

    def __init__(self, service: Optional[AnalyticsService] = None):
        self.analytics = service or analytics_service

    def detect_all_opportunities(self) -> List[Dict[str, Any]]:
        opportunities = []

        # Vector 1: High Checkout Abandonment on High-Value Baskets
        opp1 = self._check_high_value_abandonment()
        if opp1:
            opportunities.append(opp1)

        # Vector 2: Payment Gateway Failures & Latency
        opp2 = self._check_payment_method_failures()
        if opp2:
            opportunities.append(opp2)

        # Vector 3: Underperforming / High-Dropoff Payment Options
        opp3 = self._check_netbanking_friction()
        if opp3:
            opportunities.append(opp3)

        # Vector 4: High Value Customer Segment Expansion
        opp4 = self._check_high_value_customer_segment()
        if opp4:
            opportunities.append(opp4)

        # Vector 5: Category Growth & Fast Moving Inventory
        opp5 = self._check_category_growth()
        if opp5:
            opportunities.append(opp5)

        # Vector 6: High Review Low Stock Alert
        opp6 = self._check_stock_vs_demand()
        if opp6:
            opportunities.append(opp6)

        return opportunities

    def _check_high_value_abandonment(self) -> Optional[Dict[str, Any]]:
        abandonment_data = self.analytics.calculate_checkout_abandonment()
        breakdown = abandonment_data.get("breakdown", [])
        
        above_3k = next((b for b in breakdown if "Above" in b.get("price_bracket", "")), None)
        below_3k = next((b for b in breakdown if "Below" in b.get("price_bracket", "")), None)

        if above_3k and below_3k:
            rate_above = above_3k["abandonment_rate"]
            rate_below = below_3k["abandonment_rate"]

            if rate_above > rate_below + 5: # significant delta
                return {
                    "opportunity_id": "GROWTH-OPP-001",
                    "vector": "Checkout Optimization",
                    "title": "Mitigate High Checkout Abandonment on Orders > ₹3,000",
                    "severity": "HIGH",
                    "metric": f"{rate_above}% abandonment for orders > ₹3,000 (vs {rate_below}% for <= ₹3,000)",
                    "evidence": (
                        f"Analysis shows {above_3k['abandoned_orders']} out of {above_3k['total_orders']} "
                        f"orders above ₹3,000 were abandoned at checkout, representing significant lost revenue."
                    ),
                    "likely_drivers": [
                        "Friction in high-ticket payment verification (OTP/2FA friction)",
                        "Absence of No-Cost EMI or 1-Click PayLater options on cart values > ₹3,000",
                        "Unexpected taxes or delivery fees shown late in the checkout flow"
                    ],
                    "recommendation": (
                        "Introduce Razorpay Affordability Widget (No-Cost EMI, Cardless EMI) and "
                        "trigger targeted exit-intent incentives (e.g., instant 5% discount) for cart values > ₹3,000."
                    ),
                    "suggested_experiment": (
                        "A/B Test Razorpay 1-Click Affordability Suite on 50% of traffic with cart value > ₹3,000 "
                        "for 14 days and measure checkout completion rate."
                    ),
                    "expected_impact": "Estimated +12% to +18% recovery in high-basket checkout conversions."
                }
        return None

    def _check_payment_method_failures(self) -> Optional[Dict[str, Any]]:
        methods = self.analytics.get_payment_method_performance()
        if not methods:
            return None

        # Find payment method with lowest success rate
        lowest = min(methods, key=lambda x: x["success_rate"])
        if lowest["success_rate"] < 85.0:
            return {
                "opportunity_id": "GROWTH-OPP-002",
                "vector": "Payment Reliability",
                "title": f"Elevate Payment Success Rate for {lowest['payment_method']}",
                "severity": "HIGH",
                "metric": f"{lowest['payment_method']} success rate is {lowest['success_rate']}% with {lowest['fail_count']} failed transactions",
                "evidence": (
                    f"{lowest['payment_method']} accounts for {lowest['total_transactions']} transactions "
                    f"with average processing time of {lowest['avg_processing_time_sec']}s and {lowest['fail_count']} failures."
                ),
                "likely_drivers": [
                    "Bank server latency and timeout during external gateway redirects",
                    "Insufficient automated retry mechanisms for transient banking errors",
                    "Suboptimal gateway routing during peak transaction hours"
                ],
                "recommendation": (
                    "Implement Razorpay Optimizer for dynamic gateway routing and enable "
                    "seamless Smart Auto-Retry on bank timeouts."
                ),
                "suggested_experiment": (
                    f"Enable Razorpay Smart Retry & Dynamic Routing on {lowest['payment_method']} transactions "
                    "for 30 days to measure reduction in bank decline rates."
                ),
                "expected_impact": "Estimated +6% to +9% boost in overall transaction completion."
            }
        return None

    def _check_netbanking_friction(self) -> Optional[Dict[str, Any]]:
        failures = self.analytics.get_payment_failure_breakdown()
        nb_failures = [f for f in failures if f["payment_method"] == "Net Banking"]
        timeout_count = sum(f["failure_count"] for f in nb_failures if "TIMEOUT" in f.get("failure_reason", ""))

        if timeout_count > 10:
            return {
                "opportunity_id": "GROWTH-OPP-003",
                "vector": "Payment Flow Friction",
                "title": "Reduce Net Banking Timeouts via UPI Intent Defaulting",
                "severity": "MEDIUM",
                "metric": f"{timeout_count} Net Banking transactions aborted due to TIMEOUT errors",
                "evidence": "Net Banking customers experience excessive latency (>8s avg), resulting in high user drop-off.",
                "likely_drivers": [
                    "Clunky 3-step bank login portals",
                    "Mobile browser popup blocking on bank redirect pages"
                ],
                "recommendation": (
                    "Smartly promote UPI & Fast Checkout as top recommended payment modes "
                    "while keeping Net Banking secondary."
                ),
                "suggested_experiment": (
                    "Re-order payment methods to place UPI Intent at the top with a 1-tap badge."
                ),
                "expected_impact": "Estimated +4.5% overall checkout success rate improvement."
            }
        return None

    def _check_high_value_customer_segment(self) -> Optional[Dict[str, Any]]:
        segments = self.analytics.get_customer_segments()
        hv_seg = next((s for s in segments if s["customer_segment"] == "High Value"), None)
        
        if hv_seg:
            return {
                "opportunity_id": "GROWTH-OPP-004",
                "vector": "Customer LTV & Loyalty",
                "title": "Maximize High Value Segment Lifetime Value (LTV)",
                "severity": "MEDIUM",
                "metric": f"High Value segment contributes ₹{hv_seg['total_revenue']:,.2f} with {hv_seg['conversion_rate']}% conversion",
                "evidence": f"Although representing a smaller user base ({hv_seg['customer_count']} customers), they drive significant share of gross margin.",
                "likely_drivers": [
                    "Higher affinity for premium electronics and audio accessories",
                    "Lower price elasticity when guaranteed fast priority delivery"
                ],
                "recommendation": (
                    "Launch an exclusive VIP loyalty tier offering early access to new tech releases and priority dispatch."
                ),
                "suggested_experiment": (
                    "Provide High Value customers with automated VIP perks on orders > ₹10,000."
                ),
                "expected_impact": "Estimated +15% increase in repeat order frequency within 60 days."
            }
        return None

    def _check_category_growth(self) -> Optional[Dict[str, Any]]:
        top_prods = self.analytics.get_top_products(limit=3)
        if top_prods:
            top_cat = top_prods[0]["category"]
            top_name = top_prods[0]["product_name"]
            return {
                "opportunity_id": "GROWTH-OPP-005",
                "vector": "Catalog & Merchandising",
                "title": f"Capitalize on High Surge Demand in {top_cat}",
                "severity": "LOW",
                "metric": f"Top product '{top_name}' generated ₹{top_prods[0]['total_revenue']:,.2f}",
                "evidence": f"{top_cat} is the top revenue-generating category across all completed transactions.",
                "likely_drivers": [
                    "High consumer interest in premium audio gear and active noise cancellation features",
                    "Strong ratings (>= 4.5) driving organic word-of-mouth conversion"
                ],
                "recommendation": (
                    f"Create bundle promotions combining {top_cat} with complementary accessories (e.g., fast chargers)."
                ),
                "suggested_experiment": (
                    f"Feature a 'Frequently Bought Together' bundle with 10% bundle discount on {top_name}."
                ),
                "expected_impact": "Estimated +8% increase in Average Order Value (AOV)."
            }
        return None

    def _check_stock_vs_demand(self) -> Optional[Dict[str, Any]]:
        query = """
            SELECT product_name, stock, rating, review_count
            FROM products
            WHERE stock < 20 AND rating >= 4.5
            ORDER BY rating DESC
            LIMIT 1;
        """
        res = self.analytics.db.execute_query(query)
        if res:
            p = res[0]
            return {
                "opportunity_id": "GROWTH-OPP-006",
                "vector": "Inventory Risk Management",
                "title": f"Prevent Stockout on Top-Rated '{p['product_name']}'",
                "severity": "MEDIUM",
                "metric": f"Only {p['stock']} units remaining in stock with high rating ({p['rating']}★)",
                "evidence": f"Product has {p['review_count']} reviews and high customer satisfaction but low inventory buffer.",
                "likely_drivers": ["Accelerated run-rate exceeding supplier replenishment lead time"],
                "recommendation": "Trigger automated restock reorder with supplier to avert revenue loss from out-of-stock bounce.",
                "suggested_experiment": "Set automated inventory threshold alert at 25 units.",
                "expected_impact": "Protects against estimated ₹1,00,000+ potential revenue leakage per month."
            }
        return None

growth_engine = GrowthOpportunityEngine()
