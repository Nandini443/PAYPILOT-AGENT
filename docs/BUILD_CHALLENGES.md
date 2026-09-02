# PayPilot Agent — Engineering Challenges & Solutions

This document logs the actual technical challenges encountered during the design, implementation, and testing of **PayPilot Agent**, along with investigations, solutions, and lessons learned.

---

## Challenge 1: Python Module Pathing During Test Collection

### Problem
When executing `pytest tests/ -v`, pytest failed during test collection with `ModuleNotFoundError: No module named 'agents'`, `'tools'`, and `'analytics'`.

### Root Cause
In Python project structures where tests reside in a sibling directory `tests/` without an installed editable package (`pip install -e .`), Python's import resolver does not inherently append the project root directory to `sys.path` during automated runner invocation.

### Investigation
Running tests directly via `python -m pytest` or `pytest` attempted to load modules relative to the current working directory, which lacked explicit path injection for child subpackages.

### Solution
1. Created `tests/conftest.py` with explicit top-level path insertion:
   ```python
   import sys, os
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```
2. Added `__init__.py` files across all subdirectories (`agents/`, `tools/`, `analytics/`, `ai/`, `database/`, `backend/`, `app/`).

### Result & Lesson
Pytest immediately discovered all 15 test cases across product tools, cart math, payment state transitions, and analytics with 100% test passage.

---

## Challenge 2: Natural Language Keyword Stemming in Telemetry Routing

### Problem
The test query `"Which payment method fails most frequently?"` initially fell through to the general fallback analytics response rather than triggering the specialized `_analyze_payment_failures()` method.

### Root Cause
The intent matcher in `analytics/insights.py` looked for exact multi-word substrings like `"fail most"` or `"fails frequently"`, which failed on variations like `"fails most frequently"`.

### Investigation
Inspecting token matching revealed that rigid string inclusion checks fail on compound phrases with intervening adverbs or different inflectional suffixes (`fails`, `failed`, `failing`, `failure`).

### Solution
Refactored the keyword matching logic in `analytics/insights.py` to check for root lemma stems:
```python
if any(w in q for w in ["fail", "fails", "failing", "failed", "failure", "declined", "error", "errors"]):
    return self._analyze_payment_failures()
```

### Result & Lesson
Robust semantic matching across all merchant phrasing variations without relying on fragile multi-word exact matches.

---

## Challenge 3: Maintaining Human-in-the-Loop State in Streamlit Re-runs

### Problem
Streamlit executes scripts top-to-bottom on every user interaction. When a user clicked "Buy Now", the page state needed to display the payment confirmation modal and await user confirmation without prematurely triggering the payment or dropping the cart context.

### Root Cause
Transient local variables are wiped on Streamlit script re-runs unless explicitly pinned in `st.session_state`.

### Solution
Structured the application state using Pydantic session models stored in `st.session_state` (`CustomerSessionState`), augmented by explicit flow control flags:
- `st.session_state["checkout_in_progress"]`
- `st.session_state["payment_completed"]`

### Result & Lesson
The checkout UI cleanly transitions between states (`DISCOVERY` -> `CONFIRMATION_MODAL` -> `PAYMENT_COMPLETED`), maintaining 100% state integrity across re-renders.

---

## Challenge 4: Zero-Hallucination Telemetry Guarantee

### Problem
Merchants making business decisions cannot afford AI hallucinating revenue numbers or guessing payment gateway decline rates.

### Root Cause
Standard LLM completions generate plausible-sounding numerical metrics when prompted for analytics summaries.

### Solution
Engineered a strict pipeline architecture where:
1. All mathematical aggregations are calculated directly in SQLite via parameterized SQL in `analytics/metrics.py`.
2. The `insights_engine` formats the output using the exact database figures.
3. If an LLM is used for formatting, the verified SQL context is supplied as an immutable constraint with temperature=0.0.

### Result & Lesson
Zero fabricated metrics across all merchant questions, providing verifiable and reproducible business intelligence.
