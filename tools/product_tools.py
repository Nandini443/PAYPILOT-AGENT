import json
import re
from typing import List, Dict, Any, Optional
from database.database import db, Database

class ProductTools:
    """Structured product catalog tools for PayPilot Agent."""

    def __init__(self, database: Optional[Database] = None):
        self.db = database or db

    def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search the product catalog with keyword matching, optional category,
        price ceiling, and minimum rating.
        """
        sql = "SELECT * FROM products WHERE 1=1"
        params = []

        q_terms = [t.strip().lower() for t in query.split() if len(t.strip()) > 2]
        
        # Keyword search across product_name, category, brand, features
        if q_terms:
            term_clauses = []
            for term in q_terms:
                term_clauses.append("(LOWER(product_name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(brand) LIKE ? OR LOWER(features) LIKE ?)")
                params.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"])
            sql += f" AND ({' OR '.join(term_clauses)})"

        if category:
            sql += " AND LOWER(category) = LOWER(?)"
            params.append(category)

        if max_price is not None:
            sql += " AND price <= ?"
            params.append(float(max_price))

        if min_rating is not None:
            sql += " AND rating >= ?"
            params.append(float(min_rating))

        sql += f" ORDER BY rating DESC, review_count DESC LIMIT {limit}"
        
        results = self.db.execute_query(sql, tuple(params))
        for r in results:
            if isinstance(r.get("features"), str):
                try:
                    r["features_list"] = json.loads(r["features"])
                except Exception:
                    r["features_list"] = [f.strip() for f in r["features"].split(",")]
        return results

    def filter_products(
        self,
        products: List[Dict[str, Any]],
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        required_features: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Filter a list of product candidates in memory."""
        filtered = []
        for p in products:
            if category and p.get("category", "").lower() != category.lower():
                continue
            if max_price is not None and float(p.get("price", 0)) > float(max_price):
                continue
            if min_rating is not None and float(p.get("rating", 0)) < float(min_rating):
                continue
            if required_features:
                features_str = (str(p.get("features", "")) + " " + str(p.get("product_name", ""))).lower()
                if not any(rf.lower() in features_str for rf in required_features):
                    continue
            filtered.append(p)
        return filtered

    def get_product_details(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve full details of a specific product."""
        query = "SELECT * FROM products WHERE product_id = ?"
        res = self.db.execute_query(query, (product_id,))
        if res:
            p = res[0]
            if isinstance(p.get("features"), str):
                try:
                    p["features_list"] = json.loads(p["features"])
                except Exception:
                    p["features_list"] = [f.strip() for f in p["features"].split(",")]
            return p
        return None

    def compare_products(self, product_ids: List[str]) -> List[Dict[str, Any]]:
        """Retrieve and format comparison attributes for multiple products."""
        placeholders = ",".join(["?"] * len(product_ids))
        query = f"SELECT * FROM products WHERE product_id IN ({placeholders})"
        res = self.db.execute_query(query, tuple(product_ids))
        for p in res:
            if isinstance(p.get("features"), str):
                try:
                    p["features_list"] = json.loads(p["features"])
                except Exception:
                    p["features_list"] = [f.strip() for f in p["features"].split(",")]
        return res

    def rank_products(
        self,
        products: List[Dict[str, Any]],
        user_intent: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Rank products based on price affinity, rating, and keyword match score (0-100%).
        Generates human-readable decision reasons.
        """
        budget = user_intent.get("budget")
        raw_prefs = user_intent.get("preferences") or []
        preferences = [str(p).lower() for p in raw_prefs]
        category = (user_intent.get("category") or "").lower()

        ranked = []
        for p in products:
            score = 50.0 # baseline
            reasons = []

            price = float(p.get("price", 0))
            rating = float(p.get("rating", 0))
            features_text = (str(p.get("features", "")) + " " + str(p.get("product_name", ""))).lower()

            # Budget adherence
            if budget:
                if price <= float(budget):
                    score += 20.0
                    reasons.append(f"Within budget of ₹{budget:,.0f} (₹{price:,.0f})")
                else:
                    score -= 25.0
                    reasons.append(f"Exceeds budget by ₹{(price - budget):,.0f}")

            # Rating quality
            if rating >= 4.5:
                score += 15.0
                reasons.append(f"Exceptional customer rating ({rating}★)")
            elif rating >= 4.0:
                score += 10.0
                reasons.append(f"Strong rating ({rating}★)")

            # Feature matching
            for pref in preferences:
                if pref in features_text:
                    score += 10.0
                    reasons.append(f"Matches feature: '{pref.capitalize()}'")

            # Category match
            if category and category in p.get("category", "").lower():
                score += 5.0

            # Stock check
            if p.get("stock", 0) > 0:
                reasons.append("In stock & ready to ship")

            final_score = min(100.0, max(10.0, score))
            
            ranked_item = dict(p)
            ranked_item["ai_match_score"] = int(round(final_score))
            ranked_item["match_reasons"] = reasons
            ranked.append(ranked_item)

        # Sort by ai_match_score DESC
        ranked.sort(key=lambda x: (x["ai_match_score"], x["rating"]), reverse=True)
        return ranked

product_tools = ProductTools()
