import pytest
from tools.product_tools import product_tools
from ai.fallback import DeterministicIntentExtractor

def test_product_search():
    results = product_tools.search_products(query="headphones", limit=5)
    assert len(results) > 0
    assert any("Headphones" in r["category"] for r in results)

def test_product_filter_by_price():
    results = product_tools.search_products(query="headphones", max_price=5000.0)
    assert len(results) > 0
    for r in results:
        assert float(r["price"]) <= 5000.0

def test_product_ranking_and_match_score():
    intent = {
        "budget": 5000.0,
        "category": "Headphones",
        "preferences": ["battery", "noise cancellation"]
    }
    candidates = product_tools.search_products(query="headphones", limit=10)
    ranked = product_tools.rank_products(candidates, intent)
    
    assert len(ranked) > 0
    top = ranked[0]
    assert top["ai_match_score"] >= 70
    assert len(top["match_reasons"]) > 0
    assert any("Within budget" in r for r in top["match_reasons"])

def test_product_comparison():
    candidates = product_tools.search_products(query="headphones", limit=2)
    ids = [c["product_id"] for c in candidates]
    compared = product_tools.compare_products(ids)
    assert len(compared) == len(ids)

def test_intent_extraction_headphones():
    query = "I need wireless headphones under ₹5,000 with good battery life"
    intent = DeterministicIntentExtractor.extract_intent(query)
    assert intent.category == "Headphones"
    assert intent.budget == 5000.0
    assert "battery" in intent.preferences or "battery life" in intent.preferences
