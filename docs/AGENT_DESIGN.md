# PayPilot Agent — Agent & Tool Design Document

This document explains the agent lifecycle, tool catalog, state transitions, human-in-the-loop (HITL) safety mechanisms, and error recovery protocols.

---

## 1. Agent Architecture Overview

PayPilot implements two specialized autonomous agents:
1. **`CustomerShoppingAgent`**: Conversational commerce agent operating on the user's behalf.
2. **`MerchantGrowthAgent`**: Analytical growth copilot operating on the merchant's business telemetry.

Both agents leverage structured Pydantic state models (`CustomerSessionState`, `MerchantSessionState`) and execute registered Python tools with strict input/output schemas.

---

## 2. Tools Catalog

### A. Product Catalog Tools (`tools/product_tools.py`)
- **`search_products(query, category, max_price, min_rating, limit)`**: Queries the SQLite product table using keyword tokenization across name, brand, category, and feature arrays.
- **`filter_products(products, category, max_price, min_rating, required_features)`**: Performs in-memory filtering against strict bounds.
- **`compare_products(product_ids)`**: Formats side-by-side spec comparison table for multi-product evaluation.
- **`rank_products(products, user_intent)`**: Calculates an explainable **AI Match Score (0-100%)** combining budget proximity, customer review ratings, and feature tag intersections.
- **`get_product_details(product_id)`**: Fetches deep specifications and inventory counts.

### B. Cart Tools (`tools/cart_tools.py`)
- **`add_to_cart(cart, product, quantity)`**: Appends or increments product quantity with line-item subtotals.
- **`remove_from_cart(cart, product_id)`**: Drops line item.
- **`calculate_cart_total(cart, tax_rate, discount_amount, shipping_fee)`**: Computes subtotal, dynamic free delivery threshold (>₹1,000), tax breakdown, and final payable amount.
- **`clear_cart()`**: Resets cart on successful purchase.

### C. Payment Engine Tools (`tools/payment_tools.py`)
- **`initiate_payment(order_id, customer_id, amount, payment_method)`**: Generates unique transaction ID and enters `INITIATED` state.
- **`confirm_and_process_payment(transaction_id, simulate_failure, failure_reason)`**: Simulates gateway processing latency (1.2s - 2.8s) and sets final state `SUCCESS` or `FAILED`.
- **`get_transaction_details(transaction_id)`**: Retrieves transaction metadata and latency.

### D. Order Lifecycle Tools (`tools/order_tools.py`)
- **`create_order(customer_id, items, amount)`**: Persists order with `PENDING` status.
- **`get_order_status(order_id)`**: Fetches order and parses item list JSON.
- **`list_customer_orders(customer_id)`**: Returns customer order history.

### E. Analytics Tools (`tools/analytics_tools.py`)
- **`query_sales_data()`**: Returns Gross Revenue, AOV, Completed Orders.
- **`query_payment_data()`**: Returns Gateway performance, latencies, failure distributions.
- **`analyze_conversion()`**: Analyzes funnel conversion and abandonment by price bracket.
- **`detect_growth_opportunities()`**: Runs 6-vector opportunity detection.
- **`answer_merchant_nl_question(question)`**: Zero-hallucination semantic question resolver.

---

## 3. Human-In-The-Loop (HITL) Safety Protocol

```
[Agent Prepares Cart & Order]
            │
            ▼
[Transaction Created: Status = INITIATED]
            │
            ▼
┌────────────────────────────────────────┐
│     HUMAN-IN-THE-LOOP SAFETY GATE      │
│  UI displays: Order Total, Method,     │
│  "Demo Payment" badge, and requires    │
│  EXPLICIT press of [Confirm Payment]   │
└───────────────────┬────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 [User Confirms]         [User Cancels]
        │                       │
        ▼                       ▼
[Status: SUCCESS]       [Status: CANCELLED]
```

### Safety Principles Enforced:
1. **No Silent Charges**: The agent can formulate plans and prepare checkouts, but is architecturally blocked from triggering financial execution without user interaction.
2. **Zero Credential Collection**: No card numbers, CVVs, PINs, or net banking credentials are ever accepted or stored.
3. **Transparent Demo Labeling**: Every checkout screen explicitly displays `"Demo / Test Payment"`.

---

## 4. Session Memory Management

- **Customer State (`CustomerSessionState`)**:
  - `intent`: Active budget, category, preferences.
  - `cart`: Line items, quantities, subtotals.
  - `recommended_products`: Top candidate list.
  - `active_order` & `active_transaction`: Current checkout IDs.
  - `activity_log`: Execution steps displayed in the telemetry activity panel.
- **Merchant State (`MerchantSessionState`)**:
  - `chat_history`: Historical inquiries and structured analytics responses.
  - `selected_timeframe`: Filter date window.

---

## 5. Failure & Error Handling

- **Database Errors**: Safe fallback queries; read-only query validator intercepts any rogue non-SELECT statements.
- **No Product Matches**: Fallback broad query executes automatically if strict multi-attribute filters yield empty sets.
- **Simulated Payment Failures**: Controlled failure simulation (`BANK_DECLINED`, `TIMEOUT`, `INSUFFICIENT_FUNDS`) transitions order status to `CANCELLED` and logs telemetry for merchant analysis.
- **Network / API Key Absence**: Automatic graceful switch to 100% offline deterministic fallback engine.
