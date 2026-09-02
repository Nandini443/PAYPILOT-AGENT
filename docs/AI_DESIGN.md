# PayPilot Agent — AI Design & Anti-Hallucination Framework

This document outlines the AI architecture, prompt guardrails, zero-hallucination guarantees, and deterministic fallback mechanics.

---

## 1. Zero-Hallucination Architectural Principles

In commerce and financial telemetry, LLM hallucinations (inventing conversion percentages, fabricating GMV, or misquoting stock levels) can lead to catastrophic business decisions.

PayPilot solves this through a **strict separation of concerns**:

```
           Merchant Question
                   │
                   ▼
┌──────────────────────────────────────┐
│       INTENT & ROUTING LAYER         │
│  Classifies query to validated SQL   │
│  analytics pipeline                  │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│     DETERMINISTIC SQL EXECUTION      │
│  Queries real database tables with   │
│  parameterized SQLite aggregations   │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       STRUCTURED OUTPUT INGEST       │
│  Extracts exact metric values        │
│  (e.g., 24.2% abandonment)          │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       SYNTHESIS & EXPLANATION        │
│  Formats strictly grounded findings, │
│  likely drivers & recommendations    │
└──────────────────────────────────────┘
```

---

## 2. LLM Provider Abstraction & Dual-Engine Design

PayPilot supports a flexible dual-engine design:

1. **Cloud LLM Engine (`OpenAI / Gemini / Claude`)**:
   - Activated when `OPENAI_API_KEY` is present in `.env`.
   - Used for advanced natural language intent extraction and polished conversational commentary.
2. **Deterministic Fallback Engine (`DeterministicIntentExtractor`)**:
   - Activated when no API key is present or in offline demo environments.
   - Leverages regular expressions, synonym mappings, and statistical heuristics to extract intent with 100% predictability.
   - **Zero dependency on cloud internet connectivity** ensures test suites and live demo presentations never fail due to API rate limits or network latency.

---

## 3. Structured Prompting & Guardrails

### Customer Intent Guardrails
- Extracts four explicit variables: `category`, `budget`, `min_rating`, `preferences`.
- Prevents rogue instructions or prompt injection by constraining extraction schema to a strict Pydantic model (`CustomerIntent`).

### Merchant Advisory Guardrails
- Enforces an invariant 5-element output contract:
  1. `Finding`: Core takeaway.
  2. `Evidence`: Concrete metric numbers from the database.
  3. `Likely Drivers`: Domain-specific hypotheses.
  4. `Recommendation`: Actionable business guidance.
  5. `Suggested Action / Experiment`: Concrete A/B test or setting change.
  6. `Expected Impact`: Explicitly marked as an estimated projection.
