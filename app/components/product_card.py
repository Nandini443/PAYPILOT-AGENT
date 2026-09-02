import streamlit as st
from typing import Dict, Any, Callable, Optional

def render_product_card(
    product: Dict[str, Any],
    on_add_to_cart: Optional[Callable[[Dict[str, Any]], None]] = None,
    on_instant_checkout: Optional[Callable[[Dict[str, Any]], None]] = None,
    key_prefix: str = "card"
):
    """
    Renders a modern fintech-grade product card with AI match badge,
    reasons checklist, and commerce action buttons.
    """
    pid = product.get("product_id", "")
    name = product.get("product_name", "Product")
    price = float(product.get("price", 0.0))
    rating = float(product.get("rating", 4.0))
    reviews = int(product.get("review_count", 0))
    brand = product.get("brand", "")
    category = product.get("category", "")
    match_score = product.get("ai_match_score", 90)
    reasons = product.get("match_reasons", [])
    features = product.get("features_list", [])
    image_url = product.get("image_url", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80")

    with st.container():
        # Custom styled card container
        st.markdown(
            f"""
            <div style="
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 18px;
                background-color: #FFFFFF;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            ">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span style="
                            background-color: #EEF2FF;
                            color: #4F46E5;
                            font-size: 11px;
                            font-weight: 700;
                            padding: 3px 8px;
                            border-radius: 6px;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        ">{category} • {brand}</span>
                        <h4 style="margin: 8px 0 4px 0; color: #0F172A; font-size: 18px; font-weight: 600;">{name}</h4>
                        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748B; margin-bottom: 12px;">
                            <span style="color: #F59E0B; font-weight: 600;">★ {rating}</span>
                            <span>({reviews:,} reviews)</span>
                            <span>•</span>
                            <span style="color: #10B981; font-weight: 600;">In Stock ({product.get('stock', 10)} units)</span>
                        </div>
                    </div>
                    <div style="
                        background: linear-gradient(135deg, #10B981, #059669);
                        color: white;
                        padding: 6px 12px;
                        border-radius: 20px;
                        font-weight: 700;
                        font-size: 13px;
                        text-align: center;
                        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
                    ">
                        ⚡ AI Match: {match_score}%
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )

        col_img, col_details = st.columns([1, 2])
        with col_img:
            try:
                st.image(image_url, use_container_width=True)
            except Exception:
                st.markdown(
                    f"""<div style="background: #F1F5F9; border-radius: 8px; padding: 40px 10px;
                    text-align: center; color: #94A3B8; font-size: 32px;">📦</div>""",
                    unsafe_allow_html=True
                )

        with col_details:
            st.markdown(
                f"""
                <div style="font-size: 24px; font-weight: 800; color: #0284C7; margin-bottom: 8px;">
                    ₹{price:,.2f}
                    <span style="font-size: 12px; color: #94A3B8; font-weight: 400;">(Incl. all taxes)</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if reasons:
                st.markdown("**AI Match Highlights:**")
                for r in reasons[:3]:
                    st.markdown(f"<span style='color: #059669; font-size: 13px;'>✓ {r}</span>", unsafe_allow_html=True)

            if features:
                st.markdown("<div style='margin-top: 10px; font-size: 12px; color: #475569;'><b>Key Specs:</b> " + " • ".join(features[:4]) + "</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🛒 Add to Cart", key=f"{key_prefix}_add_{pid}", use_container_width=True):
                if on_add_to_cart:
                    on_add_to_cart(product)
        with btn_col2:
            if st.button("⚡ Buy Now (Agent Checkout)", key=f"{key_prefix}_buy_{pid}", type="primary", use_container_width=True):
                if on_instant_checkout:
                    on_instant_checkout(product)
