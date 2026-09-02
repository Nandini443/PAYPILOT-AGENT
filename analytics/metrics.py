import json
from typing import Dict, Any, List, Optional
import pandas as pd
from database.database import db, Database

class AnalyticsService:
    """Core analytics engine querying the database for deterministic metrics."""

    def __init__(self, database: Optional[Database] = None):
        self.db = database or db

    def calculate_revenue(self) -> Dict[str, Any]:
        """Calculate total gross revenue from completed orders."""
        query = """
            SELECT 
                COALESCE(SUM(amount), 0.0) as gross_revenue,
                COUNT(*) as completed_orders
            FROM orders 
            WHERE order_status = 'COMPLETED' AND payment_status = 'SUCCESS';
        """
        res = self.db.execute_query(query)
        rev = float(res[0]["gross_revenue"]) if res else 0.0
        orders = int(res[0]["completed_orders"]) if res else 0
        return {
            "gross_revenue": round(rev, 2),
            "completed_orders": orders
        }

    def calculate_conversion_rate(self) -> Dict[str, Any]:
        """Calculate overall checkout-to-purchase conversion rate."""
        query = """
            SELECT 
                COUNT(*) as total_orders,
                SUM(CASE WHEN order_status = 'COMPLETED' AND payment_status = 'SUCCESS' THEN 1 ELSE 0 END) as successful_orders,
                SUM(CASE WHEN checkout_status = 'ABANDONED' THEN 1 ELSE 0 END) as abandoned_orders
            FROM orders;
        """
        res = self.db.execute_query(query)
        if not res or res[0]["total_orders"] == 0:
            return {"total_orders": 0, "successful_orders": 0, "conversion_rate": 0.0, "abandonment_rate": 0.0}

        total = res[0]["total_orders"]
        success = res[0]["successful_orders"]
        abandoned = res[0]["abandoned_orders"]
        conv_rate = (success / total) * 100.0
        abandon_rate = (abandoned / total) * 100.0

        return {
            "total_orders": total,
            "successful_orders": success,
            "abandoned_orders": abandoned,
            "conversion_rate": round(conv_rate, 2),
            "abandonment_rate": round(abandon_rate, 2)
        }

    def calculate_payment_success_rate(self) -> Dict[str, Any]:
        """Calculate payment gateway success and failure rates."""
        query = """
            SELECT 
                COUNT(*) as total_tx,
                SUM(CASE WHEN payment_status = 'SUCCESS' THEN 1 ELSE 0 END) as successful_tx,
                SUM(CASE WHEN payment_status = 'FAILED' THEN 1 ELSE 0 END) as failed_tx
            FROM transactions;
        """
        res = self.db.execute_query(query)
        if not res or res[0]["total_tx"] == 0:
            return {"total_transactions": 0, "success_rate": 0.0, "failure_rate": 0.0}

        total = res[0]["total_tx"]
        success = res[0]["successful_tx"]
        failed = res[0]["failed_tx"]
        s_rate = (success / total) * 100.0
        f_rate = (failed / total) * 100.0

        return {
            "total_transactions": total,
            "successful_transactions": success,
            "failed_transactions": failed,
            "success_rate": round(s_rate, 2),
            "failure_rate": round(f_rate, 2)
        }

    def calculate_average_order_value(self) -> float:
        """Calculate Average Order Value (AOV)."""
        query = """
            SELECT AVG(amount) as aov
            FROM orders
            WHERE order_status = 'COMPLETED' AND payment_status = 'SUCCESS';
        """
        res = self.db.execute_query(query)
        if res and res[0]["aov"] is not None:
            return round(float(res[0]["aov"]), 2)
        return 0.0

    def calculate_checkout_abandonment(self) -> Dict[str, Any]:
        """Analyze checkout abandonment with breakdown for high-value orders (> ₹3,000)."""
        query = """
            SELECT 
                CASE WHEN amount > 3000 THEN 'Above ₹3,000' ELSE 'Below/Equal ₹3,000' END as price_bracket,
                COUNT(*) as total_orders,
                SUM(CASE WHEN checkout_status = 'ABANDONED' THEN 1 ELSE 0 END) as abandoned_orders,
                ROUND(100.0 * SUM(CASE WHEN checkout_status = 'ABANDONED' THEN 1 ELSE 0 END) / COUNT(*), 2) as abandonment_rate
            FROM orders
            GROUP BY price_bracket;
        """
        df = self.db.execute_df(query)
        overall = self.calculate_conversion_rate()
        return {
            "overall_abandonment_rate": overall["abandonment_rate"],
            "breakdown": df.to_dict(orient="records")
        }

    def get_top_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Identify top-performing products by revenue and units sold."""
        query = f"""
            SELECT 
                p.product_id,
                p.product_name,
                p.category,
                p.price,
                p.rating,
                COUNT(t.transaction_id) as sales_volume,
                SUM(t.amount) as total_revenue
            FROM transactions t
            JOIN products p ON t.product_id = p.product_id
            WHERE t.payment_status = 'SUCCESS'
            GROUP BY p.product_id, p.product_name, p.category, p.price, p.rating
            ORDER BY total_revenue DESC
            LIMIT {limit};
        """
        return self.db.execute_query(query)

    def get_payment_method_performance(self) -> List[Dict[str, Any]]:
        """Analyze performance, success rate, and average latency by payment method."""
        query = """
            SELECT 
                payment_method,
                COUNT(*) as total_transactions,
                SUM(CASE WHEN payment_status = 'SUCCESS' THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN payment_status = 'FAILED' THEN 1 ELSE 0 END) as fail_count,
                ROUND(100.0 * SUM(CASE WHEN payment_status = 'SUCCESS' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate,
                ROUND(AVG(processing_time), 2) as avg_processing_time_sec
            FROM transactions
            GROUP BY payment_method
            ORDER BY success_rate DESC;
        """
        return self.db.execute_query(query)

    def get_payment_failure_breakdown(self) -> List[Dict[str, Any]]:
        """Analyze failure reasons across failed transactions."""
        query = """
            SELECT 
                payment_method,
                failure_reason,
                COUNT(*) as failure_count
            FROM transactions
            WHERE payment_status = 'FAILED' AND failure_reason != 'NONE'
            GROUP BY payment_method, failure_reason
            ORDER BY failure_count DESC;
        """
        return self.db.execute_query(query)

    def get_customer_segments(self) -> List[Dict[str, Any]]:
        """Customer segment breakdown with conversion and revenue metrics."""
        query = """
            SELECT 
                c.customer_segment,
                COUNT(DISTINCT c.customer_id) as customer_count,
                COUNT(o.order_id) as total_orders,
                SUM(CASE WHEN o.order_status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_orders,
                ROUND(100.0 * SUM(CASE WHEN o.order_status = 'COMPLETED' THEN 1 ELSE 0 END) / COUNT(o.order_id), 2) as conversion_rate,
                ROUND(COALESCE(SUM(CASE WHEN o.order_status = 'COMPLETED' THEN o.amount ELSE 0 END), 0.0), 2) as total_revenue
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_segment
            ORDER BY total_revenue DESC;
        """
        return self.db.execute_query(query)

    def get_funnel_metrics(self) -> Dict[str, Any]:
        """Return full commerce conversion funnel steps."""
        orders_df = self.db.execute_df("SELECT * FROM orders")
        total_orders = len(orders_df)
        checkout_initiated = len(orders_df[orders_df["checkout_status"].isin(["COMPLETED", "INITIATED"])])
        completed = len(orders_df[(orders_df["order_status"] == "COMPLETED") & (orders_df["payment_status"] == "SUCCESS")])
        abandoned = len(orders_df[orders_df["checkout_status"] == "ABANDONED"])
        failed_payment = len(orders_df[orders_df["payment_status"] == "FAILED"])

        return {
            "catalog_searches_simulated": int(total_orders * 2.8),
            "cart_additions": int(total_orders * 1.4),
            "checkout_initiated": total_orders,
            "checkout_abandoned": abandoned,
            "payment_failed": failed_payment,
            "orders_completed": completed
        }

    def get_revenue_trend(self) -> List[Dict[str, Any]]:
        """Daily revenue and orders aggregation for Plotly charts."""
        query = """
            SELECT 
                DATE(timestamp) as order_date,
                COUNT(*) as orders_count,
                SUM(CASE WHEN order_status = 'COMPLETED' AND payment_status = 'SUCCESS' THEN amount ELSE 0 END) as daily_revenue
            FROM orders
            GROUP BY DATE(timestamp)
            ORDER BY order_date ASC;
        """
        return self.db.execute_query(query)

    def get_executive_summary(self) -> Dict[str, Any]:
        """Aggregate all primary KPIs into a single structured summary."""
        rev = self.calculate_revenue()
        conv = self.calculate_conversion_rate()
        pay = self.calculate_payment_success_rate()
        aov = self.calculate_average_order_value()
        abandon = self.calculate_checkout_abandonment()

        return {
            "gross_revenue": rev["gross_revenue"],
            "completed_orders": rev["completed_orders"],
            "total_orders": conv["total_orders"],
            "conversion_rate": conv["conversion_rate"],
            "abandonment_rate": conv["abandonment_rate"],
            "average_order_value": aov,
            "payment_success_rate": pay["success_rate"],
            "payment_failure_rate": pay["failure_rate"],
            "abandonment_breakdown": abandon["breakdown"]
        }

analytics_service = AnalyticsService()
