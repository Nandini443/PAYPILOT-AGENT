import streamlit as st
from typing import Dict, Any, Callable, Optional

def render_checkout_flow(
    order: Dict[str, Any],
    transaction: Dict[str, Any],
    cart_summary: Dict[str, Any],
    on_confirm_payment: Callable[[bool, Optional[str]], None],
    on_cancel: Callable[[], None]
):
    """
    Renders Human-in-the-Loop Payment Confirmation view.
    STRICT SAFETY: Requires explicit user button action before simulated payment executes.
    """
    st.markdown("---")
    st.markdown("## 🔒 Secure Simulated Checkout (Demo Payment)")

    st.warning("⚠️ **Safety Notice**: This is a simulated test checkout. No real financial credentials or cards are collected or charged.")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 🛒 Order Review")
        for item in cart_summary.get("items", []):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #F1F5F9;">
                    <span><b>{item.get('product_name')}</b> × {item.get('quantity')}</span>
                    <span style="font-weight: 600;">₹{item.get('subtotal', 0):,.2f}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(f"**Subtotal**: ₹{cart_summary.get('subtotal', 0):,.2f}")
        st.markdown(f"**Delivery**: {'FREE' if cart_summary.get('shipping_fee') == 0 else f'₹{cart_summary.get(\"shipping_fee\"):,.2f}'}")
        st.markdown(f"**Estimated GST (Included)**: ₹{cart_summary.get('tax_amount', 0):,.2f}")
        
        st.markdown(
            f"""
            <div style="
                background-color: #F0FDF4;
                border: 1px solid #BBF7D0;
                padding: 12px;
                border-radius: 8px;
                margin-top: 12px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 16px; font-weight: 700; color: #166534;">Total Payable:</span>
                    <span style="font-size: 22px; font-weight: 800; color: #15803D;">₹{cart_summary.get('total_payable', 0):,.2f}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("### 💳 Payment Method")
        method = transaction.get("payment_method", "UPI")
        st.info(f"Selected Method: **{method} (Simulated 1-Click)**")

        st.markdown("#### 🧪 Test Simulation Controls")
        simulate_fail = st.checkbox("Simulate Gateway Failure (for testing)", value=False)
        fail_reason = None
        if simulate_fail:
            fail_reason = st.selectbox(
                "Select Failure Reason to Simulate",
                ["BANK_DECLINED", "TIMEOUT", "INSUFFICIENT_FUNDS", "NETWORK_ERROR"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"**Your selected product is ₹{cart_summary.get('total_payable', 0):,.2f} and the total payable amount is ₹{cart_summary.get('total_payable', 0):,.2f}.**"
        )
        st.markdown("Would you like to proceed to payment?")

        btn_confirm, btn_cancel = st.columns(2)
        with btn_confirm:
            if st.button("✅ Confirm Payment", type="primary", use_container_width=True, key="btn_confirm_pay"):
                on_confirm_payment(simulate_fail, fail_reason)
        with btn_cancel:
            if st.button("❌ Cancel", use_container_width=True, key="btn_cancel_pay"):
                on_cancel()
