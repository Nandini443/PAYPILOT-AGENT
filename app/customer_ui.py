import streamlit as st
from typing import Dict, Any, List, Optional
from agents.state import CustomerSessionState
from agents.customer_agent import customer_agent
from tools.cart_tools import cart_tools
from app.components.product_card import render_product_card
from app.components.checkout_modal import render_checkout_flow
from app.components.activity_panel import render_agent_activity_panel

def render_customer_view(state: CustomerSessionState):
    """
    Renders the AI Shopping & Autonomous Agentic Commerce Experience.
    """
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            padding: 24px;
            border-radius: 12px;
            color: white;
            margin-bottom: 24px;
        ">
            <h1 style="color: #FFFFFF; font-size: 28px; margin: 0 0 8px 0;">⚡ PayPilot Shopping Agent</h1>
            <p style="color: #94A3B8; font-size: 15px; margin: 0;">
                Autonomous AI Commerce: Describe what you need, let the agent evaluate and rank candidates, and review safe 1-click checkout with human confirmation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Example Prompts — covers all 6 product categories
    st.markdown("##### 💡 Try Example Prompts:")
    row1_c1, row1_c2, row1_c3, row1_c4 = st.columns(4)
    row2_c1, row2_c2, row2_c3, row2_c4 = st.columns(4)
    
    selected_prompt = None
    with row1_c1:
        if st.button("🎧 Wireless headphones under ₹5,000", use_container_width=True):
            selected_prompt = "I need wireless headphones under ₹5,000 with good battery life."
    with row1_c2:
        if st.button("💻 Laptop for coding under ₹60,000", use_container_width=True):
            selected_prompt = "I need a laptop for coding under ₹60,000."
    with row1_c3:
        if st.button("📱 Best phones under ₹25,000", use_container_width=True):
            selected_prompt = "Compare the best phones under ₹25,000."
    with row1_c4:
        if st.button("⌚ Smartwatch with AMOLED display", use_container_width=True):
            selected_prompt = "Find a smartwatch with AMOLED display and good battery."
    with row2_c1:
        if st.button("👟 Running shoes under ₹4,000", use_container_width=True):
            selected_prompt = "Find running shoes under ₹4,000 with cushioning."
    with row2_c2:
        if st.button("🖱️ Keyboard & mouse for work", use_container_width=True):
            selected_prompt = "I need a wireless mouse and mechanical keyboard for office."
    with row2_c3:
        if st.button("🔋 Power bank for laptop charging", use_container_width=True):
            selected_prompt = "Find a power bank that can charge laptops."
    with row2_c4:
        if st.button("🛒 Browse All Products", use_container_width=True):
            selected_prompt = "Show me all products across every category."

    # Search Bar
    user_input = st.text_input(
        "Tell me what you want to buy...",
        value=selected_prompt or "",
        placeholder="e.g. Find wireless headphones under ₹5,000 with good battery life",
        key="customer_search_input"
    )

    col_search_btn, col_cart_btn = st.columns([4, 1])
    with col_search_btn:
        search_clicked = st.button("🚀 Ask PayPilot Agent", type="primary", use_container_width=True)

    if search_clicked and user_input:
        with st.spinner("🤖 PayPilot Agent is understanding requirements and searching catalog..."):
            customer_agent.process_shopping_query(user_input, state)
            st.session_state["checkout_in_progress"] = False
            st.session_state["payment_completed"] = False

    # Layout: Main Content (8 cols) + Agent Activity / Cart (4 cols)
    main_col, side_col = st.columns([2.2, 1])

    with side_col:
        # Cart Box
        st.markdown("### 🛍️ Your Cart")
        if not state.cart:
            st.info("Your cart is empty.")
        else:
            cart_total = cart_tools.calculate_cart_total(state.cart)
            for item in state.cart:
                st.markdown(
                    f"""
                    <div style="background: white; border: 1px solid #E2E8F0; padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                        <div style="font-weight: 600; font-size: 13px;">{item['product_name']}</div>
                        <div style="color: #64748B; font-size: 12px;">Qty: {item['quantity']} × ₹{item['price']:,.2f} = <b>₹{item['subtotal']:,.2f}</b></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(f"**Total Payable**: <span style='font-size: 18px; font-weight: 700; color: #0284C7;'>₹{cart_total['total_payable']:,.2f}</span>", unsafe_allow_html=True)
            if st.button("💳 Proceed to Checkout", key="btn_side_checkout", type="primary", use_container_width=True):
                if state.cart:
                    first_prod_id = state.cart[0]["product_id"]
                    customer_agent.prepare_checkout(first_prod_id, state)
                    st.session_state["checkout_in_progress"] = True

        st.markdown("<br>", unsafe_allow_html=True)
        render_agent_activity_panel(state.activity_log)

    with main_col:
        # If payment just succeeded
        if st.session_state.get("payment_completed") and state.active_transaction:
            txn = state.active_transaction
            if txn.get("status") == "SUCCESS":
                st.success(
                    f"🎉 **Payment Successful & Order Confirmed!**\n\n"
                    f"• **Order ID**: `{txn.get('order_id')}`\n"
                    f"• **Transaction ID**: `{txn.get('transaction_id')}`\n"
                    f"• **Amount Paid**: `₹{txn.get('amount', 0):,.2f}`\n"
                    f"• **Method**: `{txn.get('payment_method')}` (Demo 1-Click)\n"
                    f"• **Processing Latency**: `{txn.get('processing_time_sec')}s`"
                )
            else:
                st.error(
                    f"❌ **Payment Failed!**\n\n"
                    f"• **Transaction ID**: `{txn.get('transaction_id')}`\n"
                    f"• **Failure Reason**: `{txn.get('failure_reason')}`\n"
                    f"• **Notice**: This simulated failure is recorded for merchant telemetry analysis."
                )

        # If checkout is in progress
        elif st.session_state.get("checkout_in_progress") and state.active_transaction:
            cart_sum = cart_tools.calculate_cart_total(state.cart)
            
            def handle_confirm(simulate_fail, fail_reason):
                customer_agent.finalize_payment(state, simulate_failure=simulate_fail, failure_reason=fail_reason)
                st.session_state["checkout_in_progress"] = False
                st.session_state["payment_completed"] = True
                st.rerun()

            def handle_cancel():
                st.session_state["checkout_in_progress"] = False
                st.rerun()

            render_checkout_flow(
                order=state.active_order,
                transaction=state.active_transaction,
                cart_summary=cart_sum,
                on_confirm_payment=handle_confirm,
                on_cancel=handle_cancel
            )

        # Product Recommendations
        elif state.recommended_products:
            st.markdown("### 🎯 Recommended Options Ranked for You")
            
            if state.best_recommendation:
                st.info(f"🏆 **Top AI Pick**: **{state.best_recommendation['product_name']}** ({state.best_recommendation.get('ai_match_score', 95)}% Match)")

            # Callbacks for product card
            def on_add(p):
                cart_tools.add_to_cart(state.cart, p, quantity=1)
                st.toast(f"Added {p['product_name']} to cart!", icon="🛒")
                st.rerun()

            def on_buy_now(p):
                customer_agent.prepare_checkout(p["product_id"], state)
                st.session_state["checkout_in_progress"] = True
                st.rerun()

            for idx, prod in enumerate(state.recommended_products):
                render_product_card(
                    prod,
                    on_add_to_cart=on_add,
                    on_instant_checkout=on_buy_now,
                    key_prefix=f"prod_{idx}"
                )

            # Product Comparison Matrix
            if len(state.recommended_products) > 1:
                with st.expander("📊 Compare Side-by-Side Specifications"):
                    comp_data = []
                    for p in state.recommended_products:
                        comp_data.append({
                            "Product": p["product_name"],
                            "AI Match": f"{p.get('ai_match_score', 0)}%",
                            "Price": f"₹{p['price']:,.2f}",
                            "Rating": f"{p['rating']}★ ({p['review_count']} reviews)",
                            "Key Features": ", ".join(p.get("features_list", [])[:3])
                        })
                    st.dataframe(comp_data, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="text-align: center; padding: 40px; color: #64748B; background: #F8FAFC; border-radius: 12px; border: 1px dashed #CBD5E1;">
                    <h3>🤖 Enter a shopping query above</h3>
                    <p>PayPilot's AI Agent will analyze requirements, retrieve live inventory, score options, and guide you through a safe checkout.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
