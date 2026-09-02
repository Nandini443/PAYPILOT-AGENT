# PayPilot Agent — System Architecture & Data Flow

This document details the software architecture, component relationships, agent planner flow, and transaction state machine of the **PayPilot Agent** platform.

---

## 1. High-Level System Architecture

```mermaid
graph TD
    subgraph UI_Layer ["Frontend / UI Layer (Streamlit)"]
        A1[Customer UI]
        A2[Merchant Executive UI]
        A3[Agent Activity Timeline]
        A4[HITL Checkout Modal]
    end

    subgraph API_Layer ["API Layer (FastAPI)"]
        B1[Customer Router]
        B2[Merchant Router]
    end

    subgraph Agent_Layer ["Agent & AI Layer"]
        C1[Agent Planner]
        C2[Customer Shopping Agent]
        C3[Merchant Growth Agent]
        C4[LLM Client / OpenAI]
        C5[Deterministic Fallback Engine]
    end

    subgraph Tools_Layer ["Autonomous Tools Layer"]
        D1[Product Tools]
        D2[Cart Tools]
        D3[Payment Tools]
        D4[Order Tools]
        D5[Analytics Tools]
    end

    subgraph Analytics_Layer ["Analytics & Growth Engine"]
        E1[Metrics Service]
        E2[6-Vector Growth Engine]
        E3[Merchant Insights Engine]
    end

    subgraph Data_Layer ["Persistence Layer (SQLite + CSVs)"]
        F1[(products Table)]
        F2[(customers Table)]
        F3[(orders Table)]
        F4[(transactions Table)]
    end

    A1 --> C2
    A2 --> C3
    A3 -.-> C2
    A4 --> D3

    B1 --> C2
    B2 --> C3

    C2 --> C1
    C2 --> D1
    C2 --> D2
    C2 --> D3
    C2 --> D4
    C2 --> C4
    C2 --> C5

    C3 --> D5
    C3 --> E1
    C3 --> E2
    C3 --> E3

    D1 --> F1
    D2 --> F1
    D3 --> F4
    D4 --> F3
    E1 --> F3
    E1 --> F4
    E2 --> F3
    E2 --> F4
    E3 --> F1
    E3 --> F3
    E3 --> F4
```

---

## 2. Customer Agentic Workflow & HITL Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as Customer
    participant UI as Customer UI
    participant Agent as Customer Agent
    participant Planner as Agent Planner
    participant Tools as Product / Cart Tools
    participant Pay as Payment Engine
    participant DB as SQLite DB

    User->>UI: Enters query ("Headphones under ₹5,000 with good battery")
    UI->>Agent: process_shopping_query()
    Agent->>Planner: Formulate execution plan
    Planner-->>Agent: Plan (Search -> Filter -> Rank -> Explain)
    Agent->>Tools: search_products(query, max_price=5000)
    Tools->>DB: Query indexed catalog
    DB-->>Tools: 12 Product Candidates
    Tools-->>Agent: Raw candidates
    Agent->>Tools: rank_products(candidates, user_intent)
    Tools-->>Agent: Ranked products with AI Match % & reasons
    Agent-->>UI: Top 3 recommendations + decision explanation
    
    User->>UI: Clicks "Buy Now"
    UI->>Agent: prepare_checkout(product_id)
    Agent->>Tools: add_to_cart() & calculate_cart_total()
    Agent->>Tools: create_order(status="PENDING")
    Tools->>DB: INSERT into orders
    Agent->>Pay: initiate_payment(status="INITIATED")
    Pay->>DB: INSERT into transactions (status="INITIATED")
    Pay-->>Agent: Transaction initialized (requires confirmation)
    Agent-->>UI: Display Checkout Modal with [Confirm Payment] button

    Note over User,UI: Human-in-the-Loop Safety Gate: No charge occurs without user click
    User->>UI: Clicks [Confirm Payment]
    UI->>Agent: finalize_payment()
    Agent->>Pay: confirm_and_process_payment(txn_id)
    Pay->>DB: UPDATE transactions (status="SUCCESS", latency=1.8s)
    Pay->>DB: UPDATE orders (status="COMPLETED", payment_status="SUCCESS")
    Pay-->>Agent: Payment Confirmed (Success)
    Agent-->>UI: Order Confirmed Screen with Transaction ID
```

---

## 3. Merchant Telemetry & Zero-Hallucination Query Flow

```mermaid
sequenceDiagram
    autonumber
    actor Merchant
    participant UI as Merchant Dashboard
    participant Agent as Merchant Growth Agent
    participant Insights as Insights Engine
    participant Growth as Growth Engine
    participant DB as SQLite Database

    Merchant->>UI: Asks "Why are customers abandoning checkout?"
    UI->>Agent: answer_query(query)
    Agent->>Insights: answer_question(query)
    Insights->>DB: SELECT abandonment rates GROUP BY price_bracket
    DB-->>Insights: >₹3k = 24.2% abandonment, <=₹3k = 12.8%
    Insights->>Growth: Fetch associated recommended experiments
    Growth-->>Insights: Recommend Razorpay Affordability Suite & Exit-intent A/B test
    Insights-->>Agent: Structured Response (Finding, Evidence, Likely Drivers, Recommendation, Action)
    Agent-->>UI: Formatted executive briefing card (100% database-backed)
```

---

## 4. Payment Finite State Machine (FSM)

```mermaid
stateDiagram-v2
    [*] --> INITIATED: initiate_payment() called by Agent
    
    state INITIATED {
        [*] --> AwaitingUserConfirmation
        AwaitingUserConfirmation --> UserCancelled: [Cancel] Clicked
        AwaitingUserConfirmation --> HumanApproved: [Confirm Payment] Clicked
    }

    UserCancelled --> CANCELLED: Order Status = CANCELLED
    HumanApproved --> PROCESSING: Gateway Handshake

    state PROCESSING {
        [*] --> VerifyingFunds
        VerifyingFunds --> SimulatedSuccess: Valid Response
        VerifyingFunds --> SimulatedFailure: Bank Decline / Timeout / Insufficient Funds
    }

    SimulatedSuccess --> SUCCESS: Order Completed & Cart Cleared
    SimulatedFailure --> FAILED: Telemetry Recorded & Order Cancelled
    
    SUCCESS --> [*]
    FAILED --> [*]
    CANCELLED --> [*]
```
