import uuid
import time
import random
from datetime import datetime
from typing import Dict, Any, Optional
from database.database import db, Database

class PaymentTools:
    """
    Simulated Payment Engine implementing a stateful transaction finite state machine:
    INITIATED -> PROCESSING -> SUCCESS / FAILED
    
    SAFETY MANDATE:
    - Never collects real cards, CVV, or banking passwords.
    - Strictly simulated for demonstration purposes.
    """

    def __init__(self, database: Optional[Database] = None):
        self.db = database or db

    def initiate_payment(
        self,
        order_id: str,
        customer_id: str,
        amount: float,
        payment_method: str = "UPI",
        product_id: Optional[str] = None,
        device_type: str = "Desktop"
    ) -> Dict[str, Any]:
        """
        Step 1: Create transaction in INITIATED state.
        Awaits explicit human confirmation before transitioning to PROCESSING.
        """
        txn_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
            INSERT INTO transactions (
                transaction_id, order_id, customer_id, product_id,
                timestamp, amount, payment_method, payment_status,
                failure_reason, processing_time, device_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'INITIATED', 'NONE', 0.0, ?);
        """
        self.db.execute_write(query, (txn_id, order_id, customer_id, product_id, ts, amount, payment_method, device_type))

        return {
            "transaction_id": txn_id,
            "order_id": order_id,
            "customer_id": customer_id,
            "amount": amount,
            "payment_method": payment_method,
            "status": "INITIATED",
            "environment": "Demo / Test Payment",
            "requires_human_confirmation": True,
            "message": f"Payment of ₹{amount:,.2f} via {payment_method} initialized. Explicit user confirmation required to process."
        }

    def confirm_and_process_payment(
        self,
        transaction_id: str,
        simulate_failure: bool = False,
        failure_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Step 2 & 3: Human has explicitly approved transaction.
        Transitions state: INITIATED -> PROCESSING -> SUCCESS / FAILED
        """
        # Fetch initial transaction
        txns = self.db.execute_query("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
        if not txns:
            return {
                "success": False,
                "status": "FAILED",
                "error": "Transaction not found."
            }

        txn = txns[0]
        method = txn["payment_method"]
        order_id = txn["order_id"]

        # Simulated latency (1.2 to 2.8s)
        proc_time = round(random.uniform(1.2, 2.8), 2)

        if simulate_failure:
            final_status = "FAILED"
            reason = failure_reason or random.choice(["BANK_DECLINED", "TIMEOUT", "INSUFFICIENT_FUNDS", "NETWORK_ERROR"])
        else:
            final_status = "SUCCESS"
            reason = "NONE"

        # Update database record
        update_tx_sql = """
            UPDATE transactions
            SET payment_status = ?, failure_reason = ?, processing_time = ?
            WHERE transaction_id = ?;
        """
        self.db.execute_write(update_tx_sql, (final_status, reason, proc_time, transaction_id))

        # Synchronize order table
        order_status = "COMPLETED" if final_status == "SUCCESS" else "CANCELLED"
        update_ord_sql = """
            UPDATE orders
            SET order_status = ?, payment_status = ?
            WHERE order_id = ?;
        """
        self.db.execute_write(update_ord_sql, (order_status, final_status, order_id))

        return {
            "transaction_id": transaction_id,
            "order_id": order_id,
            "status": final_status,
            "payment_method": method,
            "amount": txn["amount"],
            "processing_time_sec": proc_time,
            "failure_reason": reason,
            "environment": "Demo / Test Payment",
            "is_confirmed": True,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_transaction_details(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Fetch transaction record by ID."""
        res = self.db.execute_query("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
        return res[0] if res else None

payment_tools = PaymentTools()
