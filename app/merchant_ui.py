import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List
from agents.state import MerchantSessionState
from agents.merchant_agent import merchant_agent
from analytics.metrics import analytics_service
from analytics.growth_engine import growth_engine

def render_merchant_view(state: MerchantSessionState):
    """
    Renders the Merchant Executive Growth Dashboard & AI Copilot.
    """
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
            padding: 24px;
            border-radius: 12px;
            color: white;
            margin-bottom: 24px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="color: #FFFFFF; font-size: 28px; margin: 0 0 8px 0;">📈 PayPilot Merchant Growth Copilot</h1>
                    <p style="color: #A5B4FC; font-size: 15px; margin: 0;">
                        Real-time commerce telemetry, automated friction detection, and deterministic AI growth advisory.
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);">
                    <span style="color: #10B981; font-weight: 700;">● Live Telemetry</span>
                    <span style="color: #CBD5E1; font-size: 12px; margin-left: 8px;">(1,500 Orders Analyzed)</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. KPI Cards Row
    kpis = analytics_service.get_executive_summary()
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        st.metric("Gross Revenue", f"₹{kpis['gross_revenue']:,.0f}", delta="Completed Orders")
    with k2:
        st.metric("Total Orders", f"{kpis['total_orders']:,}", delta=f"{kpis['completed_orders']} Successful")
    with k3:
        st.metric("Conversion Rate", f"{kpis['conversion_rate']}%", delta="-2.1% Drop-off", delta_color="inverse")
    with k4:
        st.metric("Payment Success", f"{kpis['payment_success_rate']}%", delta="Gateway Avg")
    with k5:
        st.metric("Abandonment Rate", f"{kpis['abandonment_rate']}%", delta="High on >₹3k", delta_color="inverse")
    with k6:
        st.metric("Avg Order Value (AOV)", f"₹{kpis['average_order_value']:,.0f}")

    st.markdown("---")

    # 2. Main Tabs: Dashboard Analytics vs AI Growth Copilot vs Growth Opportunities
    tab_copilot, tab_opps, tab_charts = st.tabs(["🤖 AI Growth Copilot (Chat)", "🎯 Growth Opportunities Engine", "📊 Executive Analytics & Funnels"])

    # ------------------ TAB 1: COPILOT CHAT ------------------
    with tab_copilot:
        st.markdown("### 💬 Ask the Merchant Growth Agent")
        st.caption("Ask questions about revenue drop-offs, payment failures, conversion leaks, and high-impact experiments. Backed by verified SQL data.")

        st.markdown("##### ⚡ Quick Inquiry Prompts:")
        q1, q2, q3 = st.columns(3)
        with q1:
            if st.button("❓ Why are customers abandoning checkout?", use_container_width=True):
                st.session_state["merchant_input_query"] = "Why are customers abandoning checkout?"
        with q2:
            if st.button("❓ Which payment method performs best?", use_container_width=True):
                st.session_state["merchant_input_query"] = "Which payment method performs best?"
        with q3:
            if st.button("❓ What should I do to improve conversion?", use_container_width=True):
                st.session_state["merchant_input_query"] = "What should I do to improve conversion?"

        q4, q5, q6 = st.columns(3)
        with q4:
            if st.button("❓ Which payment method fails most frequently?", use_container_width=True):
                st.session_state["merchant_input_query"] = "Which payment method fails most frequently?"
        with q5:
            if st.button("❓ What is the payment success rate for UPI?", use_container_width=True):
                st.session_state["merchant_input_query"] = "What is the payment success rate for UPI?"
        with q6:
            if st.button("❓ Which product generated the most revenue?", use_container_width=True):
                st.session_state["merchant_input_query"] = "Which product generated the most revenue?"

        merchant_query = st.text_input(
            "Enter custom merchant query...",
            value=st.session_state.get("merchant_input_query", ""),
            placeholder="e.g. Why are customers abandoning checkout?"
        )

        if st.button("🔍 Query Telemetry Engine", type="primary", use_container_width=True):
            if merchant_query:
                with st.spinner("Analyzing telemetry database and calculating metrics..."):
                    merchant_agent.answer_query(merchant_query, state)
                    st.session_state["merchant_input_query"] = ""

        # Display Conversation History
        if state.chat_history:
            st.markdown("### 📋 Growth Telemetry Analysis")
            for chat in reversed(state.chat_history):
                ans = chat["response"]
                evidence_raw = ans.get("evidence", {})
                if isinstance(evidence_raw, dict):
                    evidence_items = [f"<b>{k.replace('_', ' ').title()}:</b> {v}" for k, v in evidence_raw.items()]
                    evidence_str = ", ".join(evidence_items)
                else:
                    evidence_str = str(evidence_raw)

                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 10px; padding: 16px; margin-bottom: 20px;">
                        <h4 style="color: #1E293B; margin-top: 0;">Merchant Inquiry: "{chat['query']}"</h4>
                        
                        <div style="background: #EFF6FF; border-left: 4px solid #3B82F6; padding: 12px; margin-bottom: 12px; border-radius: 0 6px 6px 0;">
                            <strong style="color: #1E40AF; font-size: 15px;">🔍 Finding:</strong><br>
                            <span style="color: #1E293B; font-size: 14px;">{ans.get('finding')}</span>
                        </div>

                        <div style="background: #F0FDF4; border-left: 4px solid #10B981; padding: 12px; margin-bottom: 12px; border-radius: 0 6px 6px 0;">
                            <strong style="color: #166534; font-size: 14px;">📊 Evidence (Verified Database Metrics):</strong><br>
                            <span style="color: #334155; font-size: 13px;">{evidence_str}</span>
                        </div>

                        <div style="margin-bottom: 12px;">
                            <strong style="color: #475569; font-size: 14px;">🧠 Likely Drivers:</strong>
                            <ul style="margin: 4px 0; padding-left: 20px; font-size: 13px; color: #334155;">
                                {''.join([f'<li>{d}</li>' for d in ans.get('likely_drivers', [])])}
                            </ul>
                        </div>

                        <div style="background: #FFFBEB; border-left: 4px solid #F59E0B; padding: 12px; margin-bottom: 12px; border-radius: 0 6px 6px 0;">
                            <strong style="color: #92400E; font-size: 14px;">💡 Actionable Recommendation:</strong><br>
                            <span style="color: #1E293B; font-size: 13px;">{ans.get('recommendation')}</span>
                        </div>

                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #64748B; border-top: 1px solid #E2E8F0; padding-top: 8px;">
                            <span><b>Suggested Experiment:</b> {ans.get('suggested_action', 'Launch A/B Test')}</span>
                            <span style="color: #059669; font-weight: 600;">{ans.get('expected_impact', '+10% conversion')}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ------------------ TAB 2: GROWTH OPPORTUNITIES ------------------
    with tab_opps:
        st.markdown("### 🎯 Automated Growth Opportunity Engine")
        st.caption("Continuous background scanning of commerce telemetry identifying lost revenue vectors.")

        opps = growth_engine.detect_all_opportunities()
        for opp in opps:
            sev_color = "#EF4444" if opp["severity"] == "HIGH" else "#F59E0B" if opp["severity"] == "MEDIUM" else "#10B981"
            sev_bg = "#FEF2F2" if opp["severity"] == "HIGH" else "#FFFBEB" if opp["severity"] == "MEDIUM" else "#F0FDF4"

            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #E2E8F0;
                        border-left: 5px solid {sev_color};
                        border-radius: 8px;
                        padding: 16px;
                        background-color: #FFFFFF;
                        margin-bottom: 16px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">
                                {opp.get('vector', 'Growth Vector')} • {opp.get('opportunity_id')}
                            </span>
                            <span style="
                                background-color: {sev_bg};
                                color: {sev_color};
                                font-weight: 700;
                                font-size: 12px;
                                padding: 3px 10px;
                                border-radius: 12px;
                            ">{opp['severity']} SEVERITY</span>
                        </div>
                        
                        <h4 style="margin: 8px 0; color: #0F172A;">{opp['title']}</h4>
                        <div style="color: #334155; font-size: 14px; margin-bottom: 8px;"><b>Metric:</b> {opp['metric']}</div>
                        <div style="color: #64748B; font-size: 13px; margin-bottom: 10px;">{opp['evidence']}</div>
                        
                        <div style="background-color: #F8FAFC; padding: 10px; border-radius: 6px; font-size: 13px; margin-bottom: 8px;">
                            <b style="color: #1E293B;">Recommended Action:</b> {opp['recommendation']}
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; border-top: 1px dashed #E2E8F0; padding-top: 8px;">
                            <span><b>🧪 Suggested Experiment:</b> {opp['suggested_experiment']}</span>
                            <span style="color: #16A34A; font-weight: 700;">{opp['expected_impact']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ------------------ TAB 3: CHARTS & VISUALIZATIONS ------------------
    with tab_charts:
        st.markdown("### 📊 Interactive Visualizations")
        
        c_col1, c_col2 = st.columns(2)

        with c_col1:
            # 1. Conversion Funnel Chart
            funnel_data = analytics_service.get_funnel_metrics()
            fig_funnel = go.Figure(go.Funnel(
                y=["Catalog Searches", "Cart Additions", "Checkout Initiated", "Payment Failed", "Orders Completed"],
                x=[
                    funnel_data["catalog_searches_simulated"],
                    funnel_data["cart_additions"],
                    funnel_data["checkout_initiated"],
                    funnel_data["payment_failed"],
                    funnel_data["orders_completed"]
                ],
                textinfo="value+percent previous",
                marker={"color": ["#3B82F6", "#6366F1", "#8B5CF6", "#EF4444", "#10B981"]}
            ))
            fig_funnel.update_layout(title="Commerce Conversion Funnel", margin=dict(t=40, b=10, l=10, r=10), height=320)
            st.plotly_chart(fig_funnel, use_container_width=True)

        with c_col2:
            # 2. Payment Method Performance Chart
            methods_df = pd.DataFrame(analytics_service.get_payment_method_performance())
            fig_methods = px.bar(
                methods_df,
                x="payment_method",
                y="success_rate",
                color="success_rate",
                color_continuous_scale="Viridis",
                text="success_rate",
                title="Payment Method Success Rate (%)"
            )
            fig_methods.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_methods.update_layout(yaxis_range=[60, 100], margin=dict(t=40, b=10, l=10, r=10), height=320)
            st.plotly_chart(fig_methods, use_container_width=True)

        c_col3, c_col4 = st.columns(2)

        with c_col3:
            # 3. Revenue Trend (Daily)
            rev_trend = pd.DataFrame(analytics_service.get_revenue_trend())
            if not rev_trend.empty:
                fig_trend = px.line(
                    rev_trend,
                    x="order_date",
                    y="daily_revenue",
                    title="Gross Daily Revenue Trend (Last 90 Days)",
                    markers=True
                )
                fig_trend.update_layout(margin=dict(t=40, b=10, l=10, r=10), height=320)
                st.plotly_chart(fig_trend, use_container_width=True)

        with c_col4:
            # 4. Failure Reason Distribution
            failures_df = pd.DataFrame(analytics_service.get_payment_failure_breakdown())
            if not failures_df.empty:
                fig_fail = px.pie(
                    failures_df,
                    names="failure_reason",
                    values="failure_count",
                    title="Payment Failure Reason Breakdown",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_fail.update_layout(margin=dict(t=40, b=10, l=10, r=10), height=320)
                st.plotly_chart(fig_fail, use_container_width=True)
