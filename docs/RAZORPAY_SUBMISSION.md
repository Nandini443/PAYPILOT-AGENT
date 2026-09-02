# Razorpay AI Builder Internship 2026 — Final Submission

**Track**: Track 1 — AI Growth  
**Focus**: Agentic Commerce  
**Project Title**: PayPilot Agent — AI-Powered Agentic Commerce & Merchant Growth Platform  
**GitHub Repository**: [https://github.com/Nandini443/PAYPILOT-AGENT](https://github.com/Nandini443/PAYPILOT-AGENT)  
**Live Demo**: [https://paypilot-agent.streamlit.app](https://paypilot-agent.streamlit.app) *(Streamlit Community Cloud)*  

---

## 1. Project Objectives

Build an AI-powered agentic commerce platform that enables customers to discover, evaluate, and purchase products through natural-language interactions while providing merchants with AI-driven recommendations to improve checkout conversion, payment success, and customer growth.

---

## 2. What Does It Solve?

### The Core Problem in Modern Digital Commerce
Traditional ecommerce platforms treat AI either as a generic, superficial chatbot or as an opaque, black-box recommendation slider. These legacy paradigms fail both sides of the transaction:
1. **Shoppers face choice paralysis and friction**: Users must navigate convoluted filter menus, manually cross-reference technical specifications, and juggle disparate product tabs.
2. **Merchants face silent revenue leakage**: Millions of rupees are lost at checkout due to unaddressed basket abandonment (e.g. high-ticket orders lacking No-Cost EMI options) and undetected payment gateway latency/declines.
3. **Safety Violations in Agentic Systems**: Autonomous agents that lack guardrails risk executing unauthorized real financial transactions.

### How PayPilot Agent Solves It
PayPilot Agent introduces a **dual-sided, production-grade agentic architecture**:
- **For Shoppers**: An autonomous Shopping Agent extracts requirements from plain language (budget ceiling, category, battery life, use-case), queries an indexed catalog, evaluates trade-offs, assigns an explainable **AI Match Score (0–100%)**, manages dynamic cart pricing, and guides the user through an explicit **Human-in-the-Loop (HITL) simulated payment workflow**.
- **For Merchants**: An automated Growth Copilot scans 1,500+ orders and transactions, identifies 6 high-impact growth vectors (such as a 24.2% abandonment rate on baskets > ₹3,000), and delivers **zero-hallucination** business recommendations and A/B experiments backed by real SQLite database telemetry.

---

## 3. Key Implemented Features

### Customer Agentic Shopping
- **Natural Language Intent Extraction**: Parses category, budget, minimum rating, and feature preferences (`battery life`, `wireless`, `coding`, `running`) using dual-engine AI (OpenAI API + 100% offline deterministic fallback).
- **Transparent Agent Telemetry Timeline**: Displays real-time milestone execution (`intent_extractor`, `search_products`, `filter_products`, `rank_products`, `explain_selection`) without leaking raw internal chain-of-thought.
- **Explainable Product Cards**: Cards feature AI Match badges and itemized decision reasons (e.g. *"Within budget of ₹5,000 (₹4,799)"*, *"Exceptional 4.6★ rating"*).
- **Automated Specification Matrix**: Side-by-side spec comparison table for multi-product evaluations.
- **Dynamic Cart Management**: Item line subtotals, tax calculation, dynamic free delivery (>₹1,000).
- **Human-in-the-Loop Payment FSM**: Stateful simulated payment engine (`INITIATED` -> `PROCESSING` -> `SUCCESS` / `FAILED`) requiring explicit user confirmation via the `[Confirm Payment]` button, with controlled demo failure testing.

### Merchant Growth Copilot
- **Real-Time Executive KPI Dashboard**: Gross Revenue, Total Orders, Conversion Rate (67%), Payment Success Rate (87.1%), Average Order Value (₹21,660), and Checkout Abandonment (18.2%).
- **Interactive Plotly Charts**: Commerce conversion funnel drop-offs, 90-day daily gross revenue trends, payment method success rate comparisons, and failure reason breakdowns.
- **6-Vector Growth Opportunity Engine**: Algorithmic detection of high-value basket abandonment, payment gateway latencies, Net Banking timeout friction, high-value customer LTV, surge category merchandising, and inventory run-rate risks.
- **Zero-Hallucination Natural Language Telemetry Chat**: Resolves merchant questions (*"Why are customers abandoning checkout?"*, *"Which payment method performs best?"*, *"Which payment method fails most frequently?"*) into verified SQL aggregations with structured **Finding**, **Evidence**, **Likely Drivers**, **Recommendation**, **Suggested Action / Experiment**, and **Expected Impact**.

---

## 4. AI & Agentic Architecture

```
CUSTOMER WORKFLOW:
User Request
  │
  ▼
Customer Shopping Agent ──> Agent Planner ──> Product Tools (search, filter, rank)
  │
  ▼
Product Recommendation (with AI Match Score & Decision Reasons)
  │
  ▼
Cart Tools (add_to_cart, calculate_cart_total)
  │
  ▼
Checkout Preparation (create_order: PENDING, initiate_payment: INITIATED)
  │
  ▼
┌───────────────────────────────────────────────┐
│        HUMAN APPROVAL SAFETY GATE             │
│  User reviews total and clicks [Confirm]      │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
Demo Payment State Machine (PROCESSING -> SUCCESS / FAILED)
  │
  ▼
Order Confirmation (order_status: COMPLETED)
```

```
MERCHANT WORKFLOW:
Merchant Inquiry ("Why are customers abandoning checkout?")
  │
  ▼
Merchant Growth Agent
  │
  ▼
Analytics & SQL Tools (calculate_checkout_abandonment, price_bracket breakdown)
  │
  ▼
Verified Telemetry Data (>₹3k = 24.2% drop-off vs 12.8% for <=₹3k)
  │
  ▼
Insights & Growth Engine (6-Vector Detection)
  │
  ▼
Structured Actionable Recommendations (Razorpay Affordability Suite + 14-day A/B Test)
```

---

## 5. Build Challenges & Technical Obstacles

### Challenge 1: Python Module Pathing During Automated Pytest Execution
- **Problem**: Running `pytest tests/ -v` failed during module collection with `ModuleNotFoundError: No module named 'agents'`, `'tools'`, `'analytics'`.
- **Investigation**: In Python subpackage architectures without an active editable install, sibling test directories do not automatically inherit the project root in `sys.path`.
- **Solution**: Created `tests/conftest.py` with explicit top-level path insertion (`sys.path.insert(0, ...)`) and added `__init__.py` files across all packages.
- **Result**: All 15 unit and integration tests collected and passed with 100% test success rate.

### Challenge 2: Natural Language Keyword Stemming in Telemetry Routing
- **Problem**: Natural language merchant queries with varied verb forms (e.g. `"Which payment method fails most frequently?"`) fell through to general fallback handlers.
- **Investigation**: Multi-word string matching on exact phrases like `"fail most"` failed when users included adverbs like `"frequently"`.
- **Solution**: Refactored token matching in `analytics/insights.py` to match root lemmas (`["fail", "fails", "failing", "failed", "failure"]`).
- **Result**: Robust semantic routing across diverse merchant inquiries without brittle phrasing restrictions.

### Challenge 3: Maintaining Human-in-the-Loop State Across Streamlit Re-runs
- **Problem**: Streamlit's top-to-bottom re-execution model risked clearing intermediate checkout states and premature payment triggers.
- **Investigation**: Ephemeral variables are reset on button clicks unless persisted in `st.session_state`.
- **Solution**: Architected Pydantic session models (`CustomerSessionState`) synchronized with flow control flags (`checkout_in_progress`, `payment_completed`).
- **Result**: Reliable, multi-stage human confirmation modal that securely retains cart context across all re-renders.

### Challenge 4: Zero-Hallucination Telemetry Guarantee
- **Problem**: Generative LLMs frequently hallucinate believable but false numbers when summarizing business metrics.
- **Investigation**: Unconstrained prompt completions invent conversion figures and average order values.
- **Solution**: Engineered a strict pipeline where all numbers are derived via deterministic SQLite aggregations in `analytics/metrics.py`, enforcing an immutable 5-element output contract.
- **Result**: 100% reproducible, verifiable business intelligence with zero fabricated statistics.

---

## 6. Future Scope

1. **Razorpay Magic Checkout Integration**: Native 1-click address autofill and tokenized biometric checkout.
2. **Real Payment Gateway Sandbox Integration**: Seamless toggle between Demo Simulation Mode and Razorpay Test Mode API keys.
3. **Multi-Agent Negotiation**: Real-time pricing negotiation where Customer Agent and Merchant Agent agree on personalized bulk discounts.
4. **Voice Commerce**: Conversational voice shopping and hands-free merchant telemetry querying across regional Indian languages.
5. **Production Observability**: OpenTelemetry tracing for agent tool execution latency and LLM token profiling.
