import re
from typing import Dict, Any, List, Optional
from agents.state import CustomerIntent

class DeterministicIntentExtractor:
    """
    100% offline, deterministic customer intent extractor using regex and NLP tokenization.
    Guarantees seamless demo operation without API keys.
    
    Supports all 6 product categories with extensive synonym coverage:
    - Headphones (audio, earphones, earbuds, TWS, ANC, etc.)
    - Laptops (notebook, MacBook, ultrabook, PC, etc.)
    - Smartphones (phone, mobile, iPhone, Android, etc.)
    - Wearables (watch, smartwatch, fitness tracker, band, etc.)
    - Footwear (shoes, sneakers, running shoes, trainers, etc.)
    - Accessories (mouse, keyboard, power bank, charger, etc.)
    """

    CATEGORY_SYNONYMS = {
        "Headphones": [
            "headphone", "headphones", "earphone", "earphones", "earbuds", "earbud",
            "tws", "audio", "headset", "headsets", "anc", "noise cancelling",
            "noise canceling", "over-ear", "over ear", "on-ear", "in-ear",
            "wireless headphone", "bluetooth headphone", "music", "listening",
            "bass", "sound", "speakers", "speaker", "airpods", "buds"
        ],
        "Laptops": [
            "laptop", "laptops", "notebook", "notebooks", "ultrabook", "ultrabooks",
            "macbook", "mac book", "chromebook", "pc", "computer", "computers",
            "computing", "workstation", "dell", "hp laptop", "lenovo", "asus",
            "acer", "coding laptop", "programming", "development machine"
        ],
        "Smartphones": [
            "phone", "phones", "smartphone", "smartphones", "mobile", "mobiles",
            "android", "iphone", "handset", "cellphone", "cell phone",
            "oneplus", "samsung phone", "redmi", "realme phone", "pixel",
            "5g phone", "camera phone", "selfie"
        ],
        "Wearables": [
            "watch", "watches", "smartwatch", "smartwatches", "smart watch",
            "band", "bands", "fitness tracker", "fitness band", "wearable", "wearables",
            "activity tracker", "apple watch", "amazfit", "noise watch", "fire-boltt",
            "health tracker", "step counter", "heart rate"
        ],
        "Footwear": [
            "shoes", "shoe", "sneakers", "sneaker", "running shoes", "running shoe",
            "footwear", "trainers", "trainer", "sports shoes", "walking shoes",
            "jogging shoes", "athletic shoes", "nike", "adidas", "puma shoes",
            "asics", "gym shoes", "workout shoes", "casual shoes"
        ],
        "Accessories": [
            "mouse", "mice", "keyboard", "keyboards", "power bank", "powerbank",
            "charger", "chargers", "accessory", "accessories", "peripherals",
            "peripheral", "usb", "cable", "cables", "adapter", "dock",
            "logitech", "keychron", "anker", "mechanical keyboard", "gaming mouse",
            "wireless mouse", "portable charger"
        ]
    }

    # General shopping intent signals (not category-specific)
    SHOPPING_SIGNALS = [
        "buy", "purchase", "need", "want", "looking for", "find", "search",
        "recommend", "recommendation", "suggest", "suggestion", "compare",
        "comparison", "best", "top", "cheapest", "affordable", "budget",
        "premium", "show me", "show all", "browse", "explore",
        "gift", "deal", "deals", "offer", "offers", "discount",
        "what should i", "help me pick", "which one", "help me choose",
        "i need", "i want", "get me", "order"
    ]

    @classmethod
    def extract_intent(cls, query: str) -> CustomerIntent:
        q_lower = query.lower().strip()

        # 1. Extract Budget (e.g. "under 5000", "under ₹5,000", "below 60k", "less than 25000", "budget 4000")
        budget: Optional[float] = None
        budget_match = re.search(
            r'(?:under|below|less than|budget|within|max|around|upto|up to|at most)\s*'
            r'(?:rs\.?|inr|₹)?\s*([0-9]+(?:,[0-9]+)*(?:\.[0-9]+)?)\s*(k|thousand|lakh)?',
            q_lower
        )
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

        # 2. Extract Category (with comprehensive synonym matching)
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
            "battery", "battery life", "long battery", "noise cancellation", "anc",
            "wireless", "bluetooth", "wired", "usb-c", "type-c",
            "coding", "programming", "gaming", "fast charge", "quick charge",
            "lightweight", "light weight", "portable", "compact", "slim",
            "amoled", "oled", "display", "screen",
            "running", "jogging", "marathon", "trail",
            "bass", "deep bass", "hi-res", "spatial audio",
            "camera", "5g", "4g", "dual sim",
            "cushioning", "comfort", "ergonomic", "breathable",
            "mechanical", "rgb", "backlit",
            "waterproof", "water resistant", "ip68", "ipx5",
            "calling", "microphone", "mic",
            "premium", "professional", "pro",
            "student", "office", "work from home",
            "touch screen", "fingerprint", "face unlock"
        ]
        for kw in feature_keywords:
            if kw in q_lower:
                preferences.append(kw)

        # 4. Extract Min Rating (e.g. "good reviews", "top rated", "4+ rating", "best")
        min_rating = None
        if any(r in q_lower for r in ["good review", "good reviews", "top rated", "highly rated", "best rated", "highest rated"]):
            min_rating = 4.2
        elif "rating > 4" in q_lower or "4+ rating" in q_lower or "four star" in q_lower:
            min_rating = 4.0
        elif any(r in q_lower for r in ["best", "top", "premium", "flagship"]):
            min_rating = 4.0

        # 5. If no category matched but query has shopping intent, set preferences from query words
        if not category and not preferences:
            # Extract meaningful words from the query as search preferences
            stop_words = {"i", "a", "an", "the", "me", "my", "for", "to", "in", "on", "and", "or",
                          "with", "that", "is", "it", "of", "can", "you", "want", "need", "buy",
                          "find", "search", "show", "get", "help", "please", "some", "any", "good",
                          "best", "top", "under", "below", "above", "around"}
            query_words = [w for w in re.findall(r'\b\w+\b', q_lower) if len(w) > 2 and w not in stop_words]
            preferences = query_words[:5]  # Use top meaningful words as search terms

        return CustomerIntent(
            raw_query=query,
            category=category,
            budget=budget,
            min_rating=min_rating,
            preferences=preferences if preferences else ["general"],
            confidence=0.95 if category else 0.70
        )
