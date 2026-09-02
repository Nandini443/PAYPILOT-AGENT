import streamlit as st
from typing import List, Dict, Any

def render_agent_activity_panel(activity_log: List[Any]):
    """
    Renders the Agent Execution Activity Panel in the sidebar or designated section.
    Demonstrates real-time transparent tool execution without private chain-of-thought.
    """
    st.markdown("### 🤖 Agent Telemetry & Activity")
    
    if not activity_log:
        st.info("Agent is idle. Enter a shopping prompt or merchant inquiry to observe tool-calling telemetry.")
        return

    st.markdown(
        """
        <div style="
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 16px;
        ">
        """,
        unsafe_allow_html=True
    )

    for i, step in enumerate(reversed(activity_log[-8:])):
        # Handle dict or Pydantic model
        title = step.title if hasattr(step, "title") else step.get("title", "Tool Execution")
        tool = step.tool_name if hasattr(step, "tool_name") else step.get("tool_name", "tool")
        status = step.status if hasattr(step, "status") else step.get("status", "COMPLETED")
        details = step.details if hasattr(step, "details") else step.get("details", "")
        ts = step.timestamp if hasattr(step, "timestamp") else step.get("timestamp", "")

        icon = "✅" if status == "COMPLETED" else "❌" if status == "FAILED" else "⏳"
        status_color = "#10B981" if status == "COMPLETED" else "#EF4444" if status == "FAILED" else "#F59E0B"

        st.markdown(
            f"""
            <div style="
                border-left: 3px solid {status_color};
                padding-left: 10px;
                margin-bottom: 10px;
                background-color: #FFFFFF;
                padding: 8px;
                border-radius: 0 6px 6px 0;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="font-size: 13px; color: #1E293B;">{icon} {title}</strong>
                    <span style="font-size: 10px; color: #94A3B8;">{ts}</span>
                </div>
                <div style="font-size: 11px; color: #6366F1; font-family: monospace; margin-top: 2px;">
                    🔧 Tool: <code>{tool}()</code>
                </div>
                {f"<div style='font-size: 11px; color: #64748B; margin-top: 4px;'>{details}</div>" if details else ""}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
