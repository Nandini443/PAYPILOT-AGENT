import streamlit as st
import os
import sys

# Ensure root directory is on python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.state import CustomerSessionState, MerchantSessionState
from app.customer_ui import render_customer_view
from app.merchant_ui import render_merchant_view
from database.database import db

# Page Configuration
st.set_page_config(
    page_title="PayPilot Agent | AI Commerce & Merchant Growth",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Fintech CSS Styles
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Global metric box styling */
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
    }
    
    /* Clean button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.15s ease-in-out;
    }
    
    /* Sidebar header badge */
    .sidebar-badge {
        background-color: #EEF2FF;
        color: #4F46E5;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Database and seed if empty (for seamless Cloud deployment)
db.init_db()
try:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        if count == 0:
            from database.seed import seed_all
            seed_all()
except Exception:
    pass

# Top Demo Mode Status Indicator
st.markdown(
    """
    <div style="
        background-color: #F1F5F9;
        border-bottom: 1px solid #E2E8F0;
        padding: 6px 16px;
        margin: -4rem -4rem 1.5rem -4rem;
        font-size: 12px;
        color: #475569;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <span>🟢 <b>Demo Mode — Synthetic Commerce Data</b> (100% Offline Capable)</span>
        <span>Razorpay AI Builder Track 1: AI Growth | Canonical: <a href="https://github.com/Nandini443/PAYPILOT-AGENT" target="_blank" style="color: #4F46E5; text-decoration: none;">Nandini443/PAYPILOT-AGENT</a></span>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize Session States
if "customer_state" not in st.session_state:
    st.session_state.customer_state = CustomerSessionState(session_id="cust_session_001")

if "merchant_state" not in st.session_state:
    st.session_state.merchant_state = MerchantSessionState(session_id="merch_session_001")

# Sidebar Navigation
with st.sidebar:
    st.markdown('<span class="sidebar-badge">RAZORPAY AI BUILDER 2026</span>', unsafe_allow_html=True)
    st.title("⚡ PayPilot Agent")
    st.caption("AI-Powered Agentic Commerce & Merchant Growth Platform (Track 1: AI Growth)")
    
    st.markdown("---")
    st.markdown("### 🎭 Select Persona Mode")
    app_mode = st.radio(
        "Choose Mode:",
        ["🛍️ Customer Shopping Agent", "📈 Merchant Growth Copilot"],
        index=0
    )

    st.markdown("---")
    st.markdown("### ⚙️ System Status")
    st.markdown("• **Engine**: `Agentic Planner + Tool Calling`")
    st.markdown("• **Database**: `SQLite (Indexed)`")
    st.markdown("• **Safety**: `Human-in-the-Loop Enabled`")
    st.markdown("• **Payments**: `Demo Simulated Gateway`")
    st.markdown("• **Offline Mode**: `100% Deterministic Fallback Active`")

    st.markdown("---")
    if st.button("🔄 Reset Demo Session", use_container_width=True):
        st.session_state.customer_state = CustomerSessionState(session_id="cust_session_001")
        st.session_state.merchant_state = MerchantSessionState(session_id="merch_session_001")
        st.session_state["checkout_in_progress"] = False
        st.session_state["payment_completed"] = False
        st.rerun()

    st.markdown("<div style='font-size: 11px; color: #94A3B8; margin-top: 20px;'>Built for Razorpay AI Builder Track 1: AI Growth</div>", unsafe_allow_html=True)

# Render Selected View
if app_mode == "🛍️ Customer Shopping Agent":
    render_customer_view(st.session_state.customer_state)
else:
    render_merchant_view(st.session_state.merchant_state)

