import re
from typing import Dict, Any, List, Optional
from agents.state import CustomerIntent

class DeterministicIntentExtractor:
    """
    100% offline, deterministic customer intent extractor using regex and NLP tokenization.
    Guarantees seamless demo operation without API keys.
    """

    CATEGORY_SYNONYMS = {
        "Headphones": ["headphone", "headphones", "earphone", "earphones", "earbuds", "tws", "audio", "headset", "anc"],
        "Laptops": ["laptop", "laptops", "notebook", "ultrabook", "macbook", "pc", "computer"],
        "Smartphones": ["phone", "phones", "smartphone", "smartphones", "mobile", "android", "iphone"],
        "Wearables": ["watch", "smartwatch", "smartwatches", "band", "fitness tracker", "wearable"],
        "Footwear": ["shoes", "shoe", "sneakers", "running shoes", "footwear", "trainers"],
        "Accessories": ["mouse", "keyboard", "power bank", "charger", "accessory", "peripherals"]
    }

    @classmethod
    def extract_intent(cls, query: str) -> CustomerIntent:
        q_lower = query.lower()

        # 1. Extract Budget (e.g. "under 5000", "under ₹5,000", "below 60k", "less than 25000", "budget 4000")
        budget: Optional[float] = None
        budget_match = re.search(r'(?:under|below|less than|budget|within|max|around)\s*(?:rs\.?|inr|₹)?\s*([0-9]+(?:,[0-9]+)*(?:\.[0-9]+)?)\s*(k|thousand|lakh)?', q_lower)
        if budget_match:
            val_str = budget_match.group(1).replace(",", "")
            multiplier = 1.0
            unit = budget_match.group(2)
            if unit in ["k", "thousand"]:
                multiplier = 1000.0
            elif unit == "lakh":
                multiplier = 100000.0
            budget = float(val_str) * multiplier
        else:
            # Check standalone numbers like ₹5000
            num_match = re.search(r'(?:rs\.?|inr|₹)\s*([0-9]+(?:,[0-9]+)*(?:\.[0-9]+)?)', q_lower)
            if num_match:
                budget = float(num_match.group(1).replace(",", ""))

        # 2. Extract Category
        category: Optional[str] = None
        for cat, synonyms in cls.CATEGORY_SYNONYMS.items():
            for syn in synonyms:
                if re.search(rf"\b{re.escape(syn)}\b", q_lower):
                    category = cat
                    break
            if category:
                break

        # 3. Extract Preferences / Feature keywords
        preferences: List[str] = []
        feature_keywords = [
            "battery", "battery life", "noise cancellation", "anc", "wireless", "bluetooth",
            "coding", "gaming", "fast charge", "lightweight", "amoled", "running", "bass",
            "camera", "5g", "cushioning", "mechanical", "ergonomic", "waterproof", "calling"
        ]
        for kw in feature_keywords:
            if kw in q_lower:
                preferences.append(kw)

        # 4. Extract Min Rating (e.g. "good reviews", "top rated", "4+ rating", "best")
        min_rating = None
        if any(r in q_lower for r in ["good review", "good reviews", "top rated", "highly rated", "best rated"]):
            min_rating = 4.2
        elif "rating > 4" in q_lower or "4+ rating" in q_lower:
            min_rating = 4.0

        return CustomerIntent(
            raw_query=query,
            category=category,
            budget=budget,
            min_rating=min_rating,
            preferences=preferences,
            confidence=0.95
        )
