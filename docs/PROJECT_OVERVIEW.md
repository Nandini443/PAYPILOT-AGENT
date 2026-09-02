# PayPilot Agent — Project Overview

> **Project Title**: PayPilot Agent — AI-Powered Agentic Commerce & Merchant Growth Platform  
> **Target Program**: Razorpay AI Builder Internship 2026 — Track 1: AI Growth  
> **Core Focus**: Dual-Sided Autonomous Commerce Workflows & Telemetry-Driven Merchant Advisory

---

## 1. Executive Summary

Traditional ecommerce systems treat AI merely as text-based chatbots or surface-level recommendation widgets. These interfaces suffer from three critical flaws:
1. **Lack of Action Autonomy**: Chatbots cannot autonomously inspect catalog attributes, manage cart line items, or initiate secure checkout sessions.
2. **Hallucination in Business Metrics**: AI summaries often invent fictional numbers, failing to provide reproducible insights to merchants.
3. **Safety Violations**: Unchecked agent autonomy risks unauthorized financial transactions without explicit human approval.

**PayPilot Agent** bridges this gap by introducing a **dual-sided, production-grade agentic commerce architecture**:
- **Customer Shopping Agent**: Understands natural language shopping intents (budget ceilings, category, feature preferences), executes multi-step catalog search/filtering/ranking tools, explains selection rationales, manages cart state, and coordinates a **Human-in-the-Loop (HITL) simulated checkout flow**.
- **Merchant Growth Copilot**: Continuously scans commerce telemetry (1,500+ orders across 90 days), detects 6 high-impact growth vectors (e.g. checkout abandonment on orders > ₹3,000, payment gateway latency, Net Banking friction), and delivers zero-hallucination business recommendations backed by deterministic SQL queries.

---

## 2. Key Problem Statements Solved

| Problem Domain | Industry Challenge | PayPilot Agent Solution |
| :--- | :--- | :--- |
| **Customer Discovery** | Users struggle with rigid multi-filter UI sliders and search boxes. | Natural Language intent parsing with semantic match scoring and explainable decision criteria. |
| **Checkout Abandonment** | High drop-off at checkout (~24% on orders > ₹3,000). | Proactive detection of friction points with actionable Razorpay Affordability recommendations. |
| **Payment Gateways** | Latency and bank declines cause silent revenue leakage. | Real-time payment method diagnostics (UPI vs Card vs Net Banking vs Wallet) with smart retry strategies. |
| **Safety & Control** | Agents authorizing real financial charges without consent. | Finite state machine with mandatory Human-in-the-Loop confirmation before any payment execution. |
| **Offline Reliability** | LLM downtime breaks demos and mission-critical workflows. | 100% deterministic fallback mode that works offline with zero API key dependencies. |

---

## 3. Target Personas

### Persona A: The High-Intent Shopper
- Wants fast, tailored product recommendations without endless scrolling.
- Values transparency on why a product is recommended.
- Demands complete visibility and control before any money is transferred.

### Persona B: The Growth-Focused Merchant / D2C Founder
- Needs immediate diagnostic answers to "Why are checkouts dropping?" and "Which payment method fails most?".
- Requires actionable, low-risk A/B experiments rather than generic advice.
- Relies on 100% accurate mathematical telemetry from real store transactions.

---

## 4. Key Feature Matrix

```
┌──────────────────────────────────────────────┐
│             PAYPILOT AGENT CORE             │
└──────────────────────┬───────────────────────┘
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│  CUSTOMER SHOPPING AGENT  │   │  MERCHANT GROWTH COPILOT  │
├───────────────────────────┤   ├───────────────────────────┤
│ • Intent Extraction       │   │ • Executive KPIs          │
│ • Catalog Search & Filter │   │ • 6-Vector Growth Engine  │
│ • AI Match Scoring (0-100)│   │ • Funnel Diagnostics      │
│ • Comparative Matrix      │   │ • NL SQL Telemetry Chat   │
│ • Dynamic Cart & Taxes    │   │ • Zero Hallucination Math │
│ • HITL Payment Approval   │   │ • A/B Experiment Planner  │
│ • State Machine Execution │   │ • Interactive Plotly Maps │
└───────────────────────────┘   └───────────────────────────┘
```
