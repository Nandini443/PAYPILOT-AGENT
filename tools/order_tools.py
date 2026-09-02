import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from database.database import db, Database

class OrderTools:
    """Order lifecycle and status tracking tools."""

    def __init__(self, database: Optional[Database] = None):
        self.db = database or db

    def create_order(
        self,
        customer_id: str,
        items: List[Dict[str, Any]],
        amount: float
    ) -> Dict[str, Any]:
        """Create a new order in PENDING status."""
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items_json = json.dumps(items)

        query = """
            INSERT INTO orders (
                order_id, customer_id, timestamp, amount,
                order_status, checkout_status, payment_status, items_json
            ) VALUES (?, ?, ?, ?, 'PENDING', 'COMPLETED', 'PENDING', ?);
        """
        self.db.execute_write(query, (order_id, customer_id, ts, amount, items_json))

        return {
            "order_id": order_id,
            "customer_id": customer_id,
            "amount": amount,
            "order_status": "PENDING",
            "checkout_status": "COMPLETED",
            "payment_status": "PENDING",
            "items": items,
            "timestamp": ts
        }

    def get_order_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve order details with parsed items list."""
        query = "SELECT * FROM orders WHERE order_id = ?"
        res = self.db.execute_query(query, (order_id,))
        if res:
            ord_data = res[0]
            if isinstance(ord_data.get("items_json"), str):
                try:
                    ord_data["items"] = json.loads(ord_data["items_json"])
                except Exception:
                    ord_data["items"] = []
            return ord_data
        return None

    def list_customer_orders(self, customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve historical orders for a given customer."""
        query = "SELECT * FROM orders WHERE customer_id = ? ORDER BY timestamp DESC LIMIT ?"
        orders = self.db.execute_query(query, (customer_id, limit))
        for o in orders:
            if isinstance(o.get("items_json"), str):
                try:
                    o["items"] = json.loads(o["items_json"])
                except Exception:
                    o["items"] = []
        return orders

order_tools = OrderTools()
