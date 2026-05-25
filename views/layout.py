import streamlit as st


# ── Shared sidebar CSS (light / off-white theme) ─────────────────────────────
_SIDEBAR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global font */
html, body, * { font-family: 'Inter', sans-serif !important; }

/* ── Sidebar: clean white panel ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e8eaf0 !important;
    min-width: 230px !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebarContent"]            { padding: 0 !important; }

/* Hide Streamlit chrome */
[data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
footer { display: none !important; }

/* ── Sidebar nav buttons ── */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: transparent !important;
    color: #4a4a6a !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    margin-bottom: 2px !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:#5c6bc0 !important;
    color: #ffffff !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Sidebar hr */
[data-testid="stSidebar"] hr {
    border-color: #eef0f4 !important;
    margin: 0.5rem 0 !important;
}
</style>
"""


def inject_custom_css():
    """Inject light background for the forecasting app main area."""
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
        background: #f5f6fa !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar(current_page: str = "Home"):
    """
    Render the persistent light-themed sidebar with navigation.
    Returns the newly selected page name (or current_page if unchanged).
    """
    st.markdown(_SIDEBAR_CSS, unsafe_allow_html=True)

    with st.sidebar:
        # ── Logo / Branding ───────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:1.4rem 1.2rem 1rem;
                    border-bottom:1px solid #eef0f4;">
            <div style="font-size:1.5rem;margin-bottom:0.2rem;">📈</div>
            <div style="font-size:1rem;font-weight:700;color:#1a1a2e;letter-spacing:-0.3px;">
                Demand Forecasting
            </div>
            <div style="font-size:0.7rem;color:#9ea3b8;margin-top:0.1rem;font-weight:400;">
                AI-Powered Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

        # ── Navigation Label ─────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:0 1rem;font-size:0.65rem;color:#b0b4c8;
                    text-transform:uppercase;letter-spacing:1.2px;
                    font-weight:600;margin-bottom:0.3rem;">
            Navigation
        </div>
        """, unsafe_allow_html=True)

        # Build nav list: only show Home, Sign In, Sign Up when NOT logged in
        is_logged_in = (
            st.session_state.get("authenticated") or
            st.session_state.get("admin_authenticated")
        )

        nav_items = []
        if not is_logged_in:
            nav_items = [
                ("Home", "🏠", "Home"),
                ("Sign In", "🔑", "Login"),
                ("Sign Up", "📝", "Signup"),
            ]

        selected = current_page
        for label, icon, key in nav_items:
            is_active = (current_page == key)
            if is_active:
                st.markdown(
                    f"""<div style="background:#eef0fc;border-left:3px solid #3949ab;
                        border-radius:10px;padding:0.58rem 1rem;
                        color:#3949ab;font-size:0.88rem;font-weight:600;
                        margin-bottom:3px;cursor:default;">
                        {icon}&nbsp;&nbsp;{label}</div>""",
                    unsafe_allow_html=True
                )
            else:
                if st.button(f"{icon}  {label}", key=f"nav_{key}"):
                    selected = key

        # ── Divider ───────────────────────────────────────────────────────────
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        st.markdown(
            "<hr style='border:none;border-top:1px solid #eef0f4;margin:0 0.5rem;'>",
            unsafe_allow_html=True
        )

        # ── Logged-in user info ───────────────────────────────────────────────
        if st.session_state.get("authenticated"):
            user_name  = st.session_state.get("user_name", "User")
            user_email = st.session_state.get("user_email", "")
            st.markdown(f"""
            <div style="padding:0.8rem 1rem;margin:0.7rem 0.5rem 0.3rem;
                        background:#f5f6fa;border:1px solid #e8eaf0;
                        border-radius:12px;">
                <div style="font-size:0.65rem;color:#9ea3b8;text-transform:uppercase;
                            letter-spacing:0.5px;margin-bottom:0.3rem;font-weight:600;">
                    Logged In As
                </div>
                <div style="font-size:0.9rem;color:#3949ab;font-weight:600;">
                    👤 {user_name}
                </div>
                <div style="font-size:0.73rem;color:#9ea3b8;margin-top:0.12rem;">
                    {user_email}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)
            if st.button("🚪 Sign Out", key="sidebar_logout_btn"):
                for k in ["authenticated", "user_name", "user_email",
                          "data_controller", "train_results", "models",
                          "trained_date_col", "future_df", "forecast_date_col"]:
                    st.session_state.pop(k, None)
                st.session_state["current_page"] = "Home"
                st.rerun()

        elif st.session_state.get("admin_authenticated"):
            st.markdown("""
            <div style="padding:0.8rem 1rem;margin:0.7rem 0.5rem 0.3rem;
                        background:#fff5f5;border:1px solid #ffcdd2;
                        border-radius:12px;">
                <div style="font-size:0.9rem;color:#c62828;font-weight:600;">
                    Admin
                </div>
                <div style="font-size:0.73rem;color:#9ea3b8;margin-top:0.12rem;">
                    admin@gmail.com
                </div>
            </div>
            
            """, unsafe_allow_html=True)

        # ── Footer ────────────────────────────────────────────────────────────
        st.markdown("""
         <br> 
        <div style="position:absolute;bottom:1rem;left:0;right:0;
                    text-align:center;font-size:0.68rem;color:#c8cad8;padding:0 1rem;">
            © 2025 Demand Forecasting
        </div>
        """, unsafe_allow_html=True)

    return selected
