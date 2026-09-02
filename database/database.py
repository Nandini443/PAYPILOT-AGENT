import os
import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "paypilot.db")

class Database:
    """Thread-safe SQLite database manager for PayPilot Agent."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("DATABASE_PATH", DEFAULT_DB_PATH)

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self, schema_file: Optional[str] = None):
        if not schema_file:
            schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
        
        with open(schema_file, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()

    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Execute a parameterized query and return list of dictionaries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def execute_df(self, query: str, params: Tuple = ()) -> pd.DataFrame:
        """Execute query and return results as pandas DataFrame."""
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)

    def execute_write(self, query: str, params: Tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return affected rows."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def execute_safe_readonly_query(self, sql: str) -> Dict[str, Any]:
        """
        Validate and execute a read-only analytics query.
        Guarantees protection against destructive operations (DROP, DELETE, UPDATE, INSERT, ALTER).
        """
        sql_clean = sql.strip()
        sql_upper = sql_clean.upper()

        # Security check: strictly allow only SELECT statements
        if not sql_upper.startswith("SELECT") and not sql_upper.startswith("WITH"):
            return {
                "success": False,
                "error": "Security Error: Only read-only SELECT or WITH queries are permitted."
            }

        forbidden_keywords = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "REPLACE", "CREATE", "GRANT", "REVOKE"]
        for kw in forbidden_keywords:
            # Check if forbidden keyword appears as a standalone word
            import re
            if re.search(rf"\b{kw}\b", sql_upper):
                return {
                    "success": False,
                    "error": f"Security Error: Disallowed keyword '{kw}' detected in query."
                }

        try:
            with self.get_connection() as conn:
                df = pd.read_sql_query(sql_clean, conn)
                return {
                    "success": True,
                    "data": df.to_dict(orient="records"),
                    "dataframe": df,
                    "row_count": len(df)
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Database Execution Error: {str(e)}"
            }

# Global singleton
db = Database()
