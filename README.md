# ⚡ PayPilot Agent

> **AI-Powered Agentic Commerce & Merchant Growth Platform**  
> *Built for the Razorpay AI Builder Internship 2026 — Track 1: AI Growth*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: Passing](https://img.shields.io/badge/Tests-15%20Passed%20(100%25)-success.svg)](#testing)

---

## 📌 Executive Overview

**PayPilot Agent** is a production-style, dual-sided agentic commerce platform that redefines how consumers discover products and how merchants optimize checkout conversion.

Unlike conventional chatbots that simply emit static text, PayPilot implements **genuine tool-based agent autonomy**:
1. **Customer Shopping Agent**: Understands conversational shopping requirements, searches an indexed SQL catalog, evaluates spec trade-offs, scores options (0–100% AI Match), explains selections, prepares cart line items, and guides the user through a **safe Human-in-the-Loop (HITL) checkout**.
2. **Merchant Growth Copilot**: Continuously analyzes 1,500+ orders and transactions, detects 6 high-impact growth vectors (e.g., high-ticket checkout abandonment, payment gateway timeouts), and answers natural language questions with **zero hallucinated metrics** backed by deterministic SQL queries.

> ⚠️ **Safety Notice**: This platform uses a simulated payment state machine for demonstration and research purposes. It never collects real financial credentials, card numbers, or CVVs.

---

## 🎯 Problem & Solution

| The Challenge in Modern Commerce | PayPilot Agent Solution |
| :--- | :--- |
| **Catalog Friction**: Shoppers face decision paralysis with rigid filter menus and search bars. | **Autonomous Discovery Agent**: Conversational intent extraction with semantic feature matching and explainable AI scores. |
| **Checkout Abandonment**: Unexplained drop-offs (~24% on orders > ₹3,000) cost merchants millions. | **Automated Growth Engine**: Diagnoses checkout friction and prescribes actionable Razorpay Affordability experiments. |
| **Payment Failures**: Gateway timeouts and bank declines lead to silent revenue leakage. | **Payment Method Diagnostics**: Telemetry breakdown of UPI, Card, Net Banking, and Wallet success rates with Smart Retry recommendations. |
| **Safety Risks in AI Agents**: Unchecked autonomy authorizing real financial charges. | **Human-in-the-Loop Gate**: Finite state machine strictly requiring explicit human approval before payment processing. |
| **API Dependency / Flakiness**: Cloud LLM rate limits breaking critical demos. | **Dual-Engine Architecture**: Seamless 100% offline deterministic fallback mode requiring zero API keys. |

---

## 🏗️ System Architecture

```
                                  ┌──────────────────────────────┐
                                  │      Streamlit Frontend      │
                                  │  (Customer UI / Merchant UI) │
                                  └──────────────┬───────────────┘
                                                 │
                                  ┌──────────────▼───────────────┐
                                  │     FastAPI Backend API      │
                                  │   (/api/customer, /merchant) │
                                  └──────────────┬───────────────┘
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼                                                           ▼
    ┌─────────────────────────────┐                             ┌─────────────────────────────┐
    │   Customer Shopping Agent   │                             │    Merchant Growth Copilot  │
    ├─────────────────────────────┤                             ├─────────────────────────────┤
    │ • Planner & Reasoning Steps │                             │ • 6-Vector Growth Engine    │
    │ • Catalog Search & Ranking  │                             │ • Deterministic SQL Queries │
    │ • Dynamic Cart & Taxes      │                             │ • Failure Reason Breakdown  │
    │ • Human-in-the-Loop Payment │                             │ • Zero Metric Hallucination │
    └──────────────┬──────────────┘                             └──────────────┬──────────────┘
                   │                                                           │
                   └─────────────────────────────┬─────────────────────────────┘
                                                 │
                                  ┌──────────────▼───────────────┐
                                  │    Autonomous Tools Layer    │
                                  │  (Products, Cart, Pay, SQL)  │
                                  └──────────────┬───────────────┘
                                                 │
                                  ┌──────────────▼───────────────┐
                                  │   SQLite Database (Indexed)  │
                                  │   (products, orders, txns)   │
                                  └──────────────────────────────┘
```

---

## 🔄 Agent Commerce Workflow

```
User Query: "Find wireless headphones under ₹5,000 with good battery life"
   │
   ▼
[Intent Extraction] ──> Budget: ₹5,000 | Category: Headphones | Prefs: ['battery life', 'wireless']
   │
   ▼
[Tool Execution] ────> search_products() -> filter_products() -> rank_products()
   │
   ▼
[Recommendation] ───> 🏆 SonicPulse Pro ANC (₹4,799 | 4.6★ | 95% AI Match)
   │
   ▼
[Checkout Prep] ────> add_to_cart() -> calculate_cart_total() -> initiate_payment()
   │
   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   HUMAN-IN-THE-LOOP SAFETY GATE                        │
│  UI displays: Total Payable = ₹4,799.00 | Method = UPI                 │
│  Awaits explicit click on [Confirm Payment]                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
[Payment Execution] ─> State Transition: INITIATED -> PROCESSING -> SUCCESS
                                    │
                                    ▼
[Order Confirmation] > Order ORD-XXXXX Confirmed | Cart Cleared | Telemetry Logged
```

---

## 💡 Key Features

### 🛍️ Customer Experience
- **Conversational Shopping**: Enter natural prompts or pick from instant demo presets.
- **Transparent Agent Telemetry**: Live timeline showing tool execution (`intent_extractor`, `search_products`, `rank_products`) without exposing private chain-of-thought.
- **Explainable Product Cards**: Visual badges with AI Match % and concrete bulleted criteria checklists.
- **Spec Comparison Matrix**: Side-by-side spec comparison of top candidate products.
- **Safe Simulated Checkout**: Stateful payment processing with controlled demo failure testing (`BANK_DECLINED`, `TIMEOUT`, `INSUFFICIENT_FUNDS`).

### 📈 Merchant Growth Copilot
- **Executive KPI Dashboard**: Live metrics for Gross Revenue, Conversion Rate, AOV, Payment Success Rate, and Abandonment Rate.
- **Interactive Visualizations (Plotly)**: Commerce Conversion Funnel drop-offs, Daily Revenue Trends, Payment Method Success comparisons, and Failure Reason donut charts.
- **6-Vector Growth Opportunity Engine**:
  1. *Mitigate High Checkout Abandonment on Orders > ₹3,000* (Severity: HIGH)
  2. *Elevate Payment Success Rate on Failing Gateways* (Severity: HIGH)
  3. *Reduce Net Banking Timeouts via UPI Intent Defaulting* (Severity: MEDIUM)
  4. *Maximize High Value Customer Segment LTV* (Severity: MEDIUM)
  5. *Capitalize on High Surge Demand Categories* (Severity: LOW)
  6. *Prevent Stockouts on Top-Rated Fast Movers* (Severity: MEDIUM)
- **Natural Language Telemetry Chat**: Ask questions like *"Why are customers abandoning checkout?"* or *"Which payment method performs best?"* with 100% database-verified answers.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.35+, Plotly Express, Custom Fintech CSS
- **Backend API**: FastAPI, Uvicorn, Pydantic V2
- **Data & Analytics Layer**: SQLite 3 (Indexed), Pandas, Scikit-learn
- **AI / LLM Layer**: OpenAI API (`gpt-4o-mini`) + Deterministic NLP Fallback Engine
- **Testing**: Pytest 8.0+

---

## 🚀 Installation & Local Setup

### 1. Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/placeholder/paypilot-agent.git
cd paypilot-agent

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)
```bash
cp .env.example .env
```
> **Note**: An OpenAI API key is purely optional. If left blank, PayPilot automatically operates in **100% Offline Demo Mode** using its deterministic intent engine.

### 4. Seed Database
```bash
python -m database.seed
```

---

## 🏃 Running the Application

### Option A: Launch Interactive Streamlit UI (Recommended)
```bash
streamlit run app/streamlit_app.py
```
*Access UI at `http://localhost:8501`.*

### Option B: Launch FastAPI Backend
```bash
uvicorn backend.main:app --reload --port 8000
```
*Access Swagger Interactive Docs at `http://localhost:8000/docs`.*

---

## 🧪 Automated Testing

Run the full automated test suite (15 unit & integration tests):
```bash
python -m pytest tests/ -v
```

### Test Coverage Highlights:
- `tests/test_products.py`: Search, price filtering, AI match scoring, spec comparison.
- `tests/test_cart_checkout.py`: Dynamic cart math, order lifecycle, payment FSM transitions (`INITIATED` -> `SUCCESS`/`FAILED`).
- `tests/test_analytics.py`: Gross revenue, conversion rates, price-bracket abandonment deltas, growth opportunity detection, and zero-hallucination NLP routing.
- `tests/test_agent_flow.py`: End-to-end customer and merchant agent integration workflows.

---

## 📂 Repository Structure

```
paypilot-agent/
├── app/
│   ├── streamlit_app.py          # Unified entrypoint (Customer / Merchant mode)
│   ├── customer_ui.py            # Customer shopping conversational UI
│   ├── merchant_ui.py            # Merchant executive dashboard & Copilot
│   └── components/
│       ├── product_card.py       # Rich product card with AI badge & reasons
│       ├── activity_panel.py     # Real-time transparent agent activity panel
│       └── checkout_modal.py     # Human-in-the-Loop checkout confirmation modal
├── backend/
│   ├── main.py                   # FastAPI REST application
│   └── api/
│       ├── customer_router.py    # Customer search, cart, and checkout endpoints
│       └── merchant_router.py    # Merchant KPIs, telemetry, and copilot endpoints
├── agents/
│   ├── customer_agent.py         # Autonomous customer shopping agent
│   ├── merchant_agent.py         # Merchant telemetry growth agent
│   ├── planner.py                # Multi-step goal planner
│   └── state.py                  # Pydantic session & telemetry state models
├── tools/
│   ├── product_tools.py          # Search, filter, compare, rank catalog tools
│   ├── cart_tools.py             # Cart line items, pricing, dynamic delivery
│   ├── payment_tools.py          # Simulated payment FSM (INITIATED -> SUCCESS/FAILED)
│   ├── order_tools.py            # Order persistence and status management
│   └── analytics_tools.py        # Telemetry aggregations & growth vector tools
├── ai/
│   ├── agent.py                  # Unified AI engine coordinator
│   ├── llm_client.py             # LLM provider abstraction with fallback
│   ├── prompts.py                # System prompts and JSON schemas
│   └── fallback.py               # Deterministic NLP regex intent extractor
├── analytics/
│   ├── metrics.py                # Deterministic revenue, AOV, conversion, gateway rates
│   ├── growth_engine.py          # 6-vector automated opportunity detection
│   └── insights.py               # Natural language question resolver (Zero Hallucination)
├── database/
│   ├── database.py               # Thread-safe SQLite manager & safe read-only query guard
│   ├── schema.sql                # DDL with indexes for products, orders, transactions
│   └── seed.py                   # Deterministic synthetic data generator (SEED=42)
├── data/
│   ├── products.csv              # Synthetic catalog (32 products across 6 categories)
│   ├── customers.csv             # Synthetic customer profiles (300 customers)
│   ├── orders.csv                # Historical orders (1,500 orders)
│   └── transactions.csv          # Payment transactions (1,153 records)
├── tests/
│   ├── conftest.py               # Test configuration & path injection
│   ├── test_products.py          # Product tools tests
│   ├── test_cart_checkout.py     # Cart and payment FSM tests
│   ├── test_analytics.py         # Analytics and growth engine tests
│   └── test_agent_flow.py        # End-to-end integration tests
├── docs/
│   ├── PROJECT_OVERVIEW.md       # Problem, solution, target users, metrics
│   ├── ARCHITECTURE.md           # System architecture & Mermaid sequence diagrams
│   ├── AGENT_DESIGN.md           # Agents, tools, HITL safety, FSM, memory
│   ├── DATA_MODEL.md             # Schema, table specs, synthetic telemetry
│   ├── API.md                    # RESTful FastAPI documentation
│   ├── AI_DESIGN.md              # Anti-hallucination framework & fallback mechanics
│   ├── DEMO_SCRIPT.md            # 5-minute master pitch presentation script
│   ├── BUILD_CHALLENGES.md       # Real engineering challenges & solutions logged
│   └── RAZORPAY_SUBMISSION.md    # Formatted Track 1 submission draft
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🔒 Security & Safety Mandates

1. **Explicit Human-in-the-Loop Confirmation**: No transaction can transition to `PROCESSING` or `SUCCESS` without explicit user button interaction.
2. **Zero Credential Retention**: Never asks for, stores, or transmits real credit card numbers, CVVs, passwords, or banking credentials.
3. **Safe Read-Only SQL Queries**: Built-in query validator strictly rejects destructive statements (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`) in telemetry analytics.

---

## 📄 Documentation Index

- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [System Architecture & Sequence Diagrams](docs/ARCHITECTURE.md)
- [Agent & Tool Design Document](docs/AGENT_DESIGN.md)
- [Data Model & Telemetry Specification](docs/DATA_MODEL.md)
- [FastAPI REST API Documentation](docs/API.md)
- [AI Design & Anti-Hallucination Framework](docs/AI_DESIGN.md)
- [5-Minute Master Pitch Script](docs/DEMO_SCRIPT.md)
- [Engineering Challenges & Lessons](docs/BUILD_CHALLENGES.md)
- [Razorpay Track 1 Submission Draft](docs/RAZORPAY_SUBMISSION.md)

---

## 📜 License

Distributed under the [MIT License](LICENSE). Built for the Razorpay AI Builder Internship 2026.
