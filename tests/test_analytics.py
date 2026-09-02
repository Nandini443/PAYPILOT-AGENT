import pytest
from analytics.metrics import analytics_service
from analytics.growth_engine import growth_engine
from analytics.insights import insights_engine

def test_revenue_and_conversion_calculation():
    rev = analytics_service.calculate_revenue()
    assert rev["gross_revenue"] > 0
    assert rev["completed_orders"] > 0

    conv = analytics_service.calculate_conversion_rate()
    assert conv["total_orders"] > 0
    assert 0.0 <= conv["conversion_rate"] <= 100.0
    assert 0.0 <= conv["abandonment_rate"] <= 100.0

def test_payment_success_rate_calculation():
    pay = analytics_service.calculate_payment_success_rate()
    assert pay["total_transactions"] > 0
    assert 50.0 <= pay["success_rate"] <= 100.0

def test_checkout_abandonment_high_value_pattern():
    abandon = analytics_service.calculate_checkout_abandonment()
    breakdown = abandon["breakdown"]
    assert len(breakdown) >= 2
    
    above_3k = next((b for b in breakdown if "Above" in b["price_bracket"]), None)
    below_3k = next((b for b in breakdown if "Below" in b["price_bracket"]), None)

    assert above_3k is not None
    assert below_3k is not None
    # Verify synthetic pattern (>₹3k has ~24% abandonment vs ~13% for <=₹3k)
    assert above_3k["abandonment_rate"] > below_3k["abandonment_rate"]

def test_growth_opportunity_detection():
    opps = growth_engine.detect_all_opportunities()
    assert len(opps) >= 4
    for opp in opps:
        assert "opportunity_id" in opp
        assert "severity" in opp
        assert "metric" in opp
        assert "recommendation" in opp
        assert "suggested_experiment" in opp

def test_merchant_natural_language_insights():
    # 1. Abandonment
    res_abandon = insights_engine.answer_question("Why are customers abandoning checkout?")
    assert "finding" in res_abandon
    assert "evidence" in res_abandon
    assert "recommendation" in res_abandon
    assert "3,000" in res_abandon["finding"]

    # 2. Payment methods
    res_pay = insights_engine.answer_question("Which payment method performs best?")
    assert "UPI" in res_pay["finding"]

    # 3. Failures
    res_fail = insights_engine.answer_question("Which payment method fails most frequently?")
    assert "failure" in res_fail["finding"].lower()
