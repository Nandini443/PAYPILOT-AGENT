# PayPilot Agent — REST API Documentation

The PayPilot Agent platform exposes a modular FastAPI backend for integrating external storefronts, headless checkout clients, and merchant analytics pipelines.

---

## Base URL
```
http://localhost:8000
```

---

## 1. Customer Endpoints

### `POST /api/customer/search`
Discovers and ranks products based on natural language customer queries.

**Request Body:**
```json
{
  "query": "I need wireless headphones under ₹5,000 with good battery life",
  "session_id": "cust_session_001"
}
```

**Response (200 OK):**
```json
{
  "intent": {
    "raw_query": "I need wireless headphones under ₹5,000 with good battery life",
    "category": "Headphones",
    "budget": 5000.0,
    "min_rating": null,
    "preferences": ["wireless", "battery life"],
    "confidence": 0.98
  },
  "recommended_products": [
    {
      "product_id": "PROD-AUD-001",
      "product_name": "SonicPulse Pro Wireless ANC Headphones",
      "price": 4799.0,
      "rating": 4.6,
      "ai_match_score": 95,
      "match_reasons": [
        "Within budget of ₹5,000 (₹4,799)",
        "Exceptional customer rating (4.6★)",
        "Matches feature: 'Battery life'",
        "In stock & ready to ship"
      ]
    }
  ],
  "best_match": { "..." : "..." },
  "decision_explanation": "I recommend the SonicPulse Pro Wireless ANC Headphones..."
}
```

---

### `POST /api/customer/checkout/prepare`
Prepares cart line items, registers a pending order, and initializes a simulated payment session.

**Request Body:**
```json
{
  "product_id": "PROD-AUD-001",
  "payment_method": "UPI",
  "customer_id": "CUST-DEMO-001"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "order": {
    "order_id": "ORD-4B219E0F",
    "customer_id": "CUST-DEMO-001",
    "amount": 4799.0,
    "order_status": "PENDING"
  },
  "transaction": {
    "transaction_id": "TXN-8A1C3D9E",
    "status": "INITIATED",
    "requires_human_confirmation": true
  },
  "cart_summary": {
    "subtotal": 4799.0,
    "shipping_fee": 0.0,
    "total_payable": 4799.0
  }
}
```

---

### `POST /api/customer/checkout/confirm`
Explicit human confirmation endpoint to execute simulated payment.

**Request Body:**
```json
{
  "transaction_id": "TXN-8A1C3D9E",
  "simulate_failure": false,
  "failure_reason": null
}
```

**Response (200 OK):**
```json
{
  "transaction_id": "TXN-8A1C3D9E",
  "order_id": "ORD-4B219E0F",
  "status": "SUCCESS",
  "payment_method": "UPI",
  "amount": 4799.0,
  "processing_time_sec": 1.84,
  "environment": "Demo / Test Payment",
  "is_confirmed": true
}
```

---

## 2. Merchant Growth Endpoints

### `GET /api/merchant/kpis`
Retrieves executive store KPIs.

**Response (200 OK):**
```json
{
  "gross_revenue": 21768219.0,
  "completed_orders": 1005,
  "total_orders": 1500,
  "conversion_rate": 67.0,
  "abandonment_rate": 18.2,
  "average_order_value": 21660.0,
  "payment_success_rate": 87.1,
  "payment_failure_rate": 12.9
}
```

---

### `POST /api/merchant/ask`
Queries the Merchant Growth Copilot with guaranteed zero hallucination.

**Request Body:**
```json
{
  "question": "Why are customers abandoning checkout?",
  "session_id": "merchant_session_001"
}
```

**Response (200 OK):**
```json
{
  "finding": "Checkout abandonment is significantly higher for high-value orders above ₹3,000 (24.2% vs 12.8% for orders <= ₹3,000).",
  "evidence": {
    "orders_above_3000_abandonment": "24.2%",
    "orders_below_3000_abandonment": "12.8%"
  },
  "likely_drivers": [
    "Payment friction during high-ticket verification (OTP/2FA drop-offs)",
    "Lack of prominent No-Cost EMI or 1-Click PayLater options on orders > ₹3,000"
  ],
  "recommendation": "Integrate the Razorpay Affordability Suite (No-Cost EMI, Cardless EMI) and deploy dynamic checkout incentives.",
  "suggested_action": "Launch a 14-day A/B test featuring Razorpay Instant EMI widgets on checkout for baskets exceeding ₹3,000.",
  "expected_impact": "Estimated +12% to +18% recovery in high-basket checkout completions."
}
```
