import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

_USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

# Hardcoded admin credentials
ADMIN_EMAIL    = "admin@gmail.com"
ADMIN_PASSWORD = "Admin@01"


def _load_users() -> dict:
    if os.path.exists(_USERS_FILE):
        with open(_USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def _inject_admin_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
        background: #f5f6fa !important;
        font-family: 'Inter', sans-serif !important;
    }
    .block-container {
        padding: 2rem 3rem 3rem !important;
        max-width: 1100px !important;
        margin: 0 auto !important;
    }
    [data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
    footer { display: none !important; }

    /* ── Admin header banner ── */
    .admin-header {
        background: linear-gradient(135deg, #c62828 0%, #e53935 60%, #ef5350 100%);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 24px rgba(198,40,40,0.2);
        position: relative;
        overflow: hidden;
    }
    .admin-header::before {
        content: '';
        position: absolute;
        top: -40%;
        right: -5%;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    .admin-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 50px;
        padding: 0.28rem 0.9rem;
        font-size: 0.73rem;
        color: #ffffff;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.7rem;
    }
    .admin-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.3rem;
        letter-spacing: -0.3px;
    }
    .admin-subtitle {
        color: rgba(255,255,255,0.78);
        font-size: 0.86rem;
    }

    /* ── Stat cards ── */
    .stat-cards {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.8rem;
    }
    .stat-card {
        flex: 1;
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 14px;
        padding: 1.3rem 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.18s, box-shadow 0.18s;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }
    .stat-card-num {
        font-size: 2rem;
        font-weight: 800;
        color: #3949ab;
        display: block;
        line-height: 1;
        margin-bottom: 0.35rem;
    }
    .stat-card-label {
        font-size: 0.75rem;
        color: #9ea3b8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 600;
    }

    /* ── Table card ── */
    .table-card {
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 18px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .table-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 1.2rem;
    }

    /* Streamlit logout button override on admin page */
    .admin-logout .stButton > button {
        background: #fff5f5 !important;
        color: #c62828 !important;
        border: 1px solid #ffcdd2 !important;
        box-shadow: none !important;
        border-radius: 10px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.2rem !important;
        width: auto !important;
        margin: 0 auto !important;
        display: block !important;
    }
    .admin-logout .stButton > button:hover {
        background: #ffebee !important;
        transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_admin_dashboard():
    """Render the full admin dashboard with registered users table."""
    _inject_admin_css()

    users = _load_users()

    # Header banner
    st.markdown("""
    <div class="admin-header">
        <div class="admin-badge">🛡️ Admin Panel</div>
        <div class="admin-title">Admin Dashboard</div>
        <div class="admin-subtitle">Manage registered users and monitor platform activity</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    total_users   = len(users)
    today_str     = datetime.utcnow().date().isoformat()
    today_signups = sum(
        1 for u in users.values()
        if u.get("created_at", "")[:10] == today_str
    )

    st.markdown(f"""
    <div class="stat-cards">
        <div class="stat-card">
            <span class="stat-card-num">{total_users}</span>
            <div class="stat-card-label">Total Users</div>
        </div>
        <div class="stat-card">
            <span class="stat-card-num">{today_signups}</span>
            <div class="stat-card-label">Signed Up Today</div>
        </div>
        <div class="stat-card">
            <span class="stat-card-num">1</span>
            <div class="stat-card-label">Admin Accounts</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Users table
    st.markdown("""
    <div class="table-card">
        <div class="table-title">👥 Registered Users</div>
    </div>
    """, unsafe_allow_html=True)

    if not users:
        st.info("📭 No users have registered yet.")
    else:
        rows = []
        for idx, (email, info) in enumerate(users.items(), start=1):
            created_raw = info.get("created_at", "N/A")
            try:
                dt = datetime.fromisoformat(created_raw)
                created_fmt = dt.strftime("%d %b %Y, %I:%M %p") + " UTC"
            except Exception:
                created_fmt = created_raw

            rows.append({
                "#":             idx,
                "Full Name":     info.get("name", "N/A"),
                "Email":         email,
                "Registered On": created_fmt,
            })

        df = pd.DataFrame(rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "#":             st.column_config.NumberColumn("#", width="small"),
                "Full Name":     st.column_config.TextColumn("Full Name"),
                "Email":         st.column_config.TextColumn("Email"),
                "Registered On": st.column_config.TextColumn("Registered On"),
            }
        )

    # Logout
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1.2, 2])
    with col2:
        st.markdown("<div class='admin-logout'>", unsafe_allow_html=True)
        if st.button("🚪 Admin Logout", key="admin_logout_btn"):
            st.session_state.pop("admin_authenticated", None)
            st.session_state["current_page"] = "Home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ── Public entry point (imported by app.py) ───────────────────────────────────
def render_admin_page():
    """
    Entry point called by app.py when current_page == 'Admin'.
    Auth is already verified via the login page, so go straight to the dashboard.
    """
    render_admin_dashboard()
