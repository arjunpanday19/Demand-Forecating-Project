import streamlit as st
import hashlib
import json
import os
import re
from datetime import datetime

# ── Path for the local users store ──────────────────────────────────────────
_USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")


def _load_users() -> dict:
    os.makedirs(os.path.dirname(_USERS_FILE), exist_ok=True)
    if os.path.exists(_USERS_FILE):
        with open(_USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_users(users: dict):
    os.makedirs(os.path.dirname(_USERS_FILE), exist_ok=True)
    with open(_USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email))


# ── Password strength ────────────────────────────────────────────────────────
def _password_strength(pw: str):
    score = 0
    if len(pw) >= 8:                     score += 1
    if re.search(r"[A-Z]", pw):         score += 1
    if re.search(r"\d", pw):            score += 1
    if re.search(r"[^A-Za-z0-9]", pw): score += 1
    labels = ["Weak", "Fair", "Good", "Strong"]
    colors = ["#e53935", "#fb8c00", "#43a047", "#1e88e5"]
    widths = ["25%", "50%", "75%", "100%"]
    idx = max(0, score - 1)
    return score, labels[idx], colors[idx], widths[idx]


def _show_strength_bar(pw: str):
    if not pw:
        return
    _, label, color, width = _password_strength(pw)
    st.markdown(f"""
    <div style="margin-top:4px;margin-bottom:8px;">
        <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">
            Password strength: <b style="color:{color};">{label}</b>
        </div>
        <div style="height:4px;border-radius:4px;background:#e0e0e0;">
            <div style="height:4px;border-radius:4px;width:{width};background:{color};
                        transition:width 0.3s,background 0.3s;"></div>
        </div>
    </div>""", unsafe_allow_html=True)


# ── CSS ──────────────────────────────────────────────────────────────────────
def _inject_auth_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Base ── */
    html, body { font-family: 'Inter', sans-serif !important; }

    /* ── Light background everywhere ── */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main {
        background: #f5f6fa !important;
    }

    /* ── Block container: no extra padding, full width ── */
    .block-container {
        padding: 2.5rem 1rem 2rem !important;
        max-width: 100% !important;
    }

    /* ── Streamlit chrome ── */
    [data-testid="stHeader"]  { background: transparent !important; box-shadow: none !important; }
    footer { display: none !important; }

    /* ──────────────────────────────────────────────────────
       WHITE CARD — pure CSS approach.
       Streamlit renders each column's content inside:
         [data-testid="column"] > div > [data-testid="stVerticalBlock"]
       We use the :nth-child selector on the columns flex row.
       The actual flex container is [data-testid="stHorizontalBlock"].
    ────────────────────────────────────────────────────── */

    /* The whole horizontal-block row — no card; transparent */
    [data-testid="stHorizontalBlock"] {
        align-items: flex-start !important;
    }

    /* Center column = second [data-testid="column"] child */
    /* Using gap: the columns sit inside a flex row */
    [data-testid="stHorizontalBlock"]
        > div[data-testid="column"]:nth-child(2) {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.8rem 2.2rem 1.6rem !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07),
                    0 14px 44px rgba(0,0,0,0.08);
    }

    /* Transparent inner wrappers so background shows through */
    [data-testid="stHorizontalBlock"]
        > div[data-testid="column"]:nth-child(2)
        > div,
    [data-testid="stHorizontalBlock"]
        > div[data-testid="column"]:nth-child(2)
        > div > * {
        background: transparent !important;
    }


    /* ── Tabs ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: #eef0f4 !important;
        border-radius: 12px !important;
        padding: 4px !important;
        border: none !important;
        gap: 0 !important;
        margin-bottom: 1.4rem !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 9px !important;
        color: #888 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        flex: 1 !important;
        justify-content: center !important;
        padding: 0.48rem 1rem !important;
        border: none !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: #ffffff !important;
        color: #3949ab !important;
        box-shadow: 0 1px 6px rgba(0,0,0,0.1) !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"],
    [data-testid="stTabs"] [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ── Input fields ── */
    [data-testid="stTextInput"] input {
        background: #f7f8fa !important;
        border: 1.5px solid #dde1ea !important;
        border-radius: 10px !important;
        color: #1a1a2e !important;
        font-size: 0.9rem !important;
        padding: 0.65rem 0.9rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        box-shadow: none !important;
    }
    [data-testid="stTextInput"] input::placeholder {
        color: #aab0be !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #5c6bc0 !important;
        box-shadow: 0 0 0 3px rgba(92,107,192,0.14) !important;
        outline: none !important;
        background: #fff !important;
    }
    [data-testid="stTextInput"] label {
        color: #3d3d5c !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1px !important;
    }

    /* ── Checkbox (show password) ── */
    [data-testid="stCheckbox"] label {
        color: #666 !important;
        font-size: 0.82rem !important;
        font-weight: 400 !important;
    }
    [data-testid="stCheckbox"] input[type="checkbox"] {
        accent-color: #5c6bc0 !important;
    }

    /* ── Primary button ── */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #3949ab 0%, #5c6bc0 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.68rem 1.2rem !important;
        font-size: 0.93rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.15px !important;
        cursor: pointer !important;
        transition: transform 0.18s, box-shadow 0.18s !important;
        box-shadow: 0 3px 14px rgba(57,73,171,0.28) !important;
        margin-top: 0.3rem !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(57,73,171,0.38) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Alert boxes ── */
    .stAlert {
        border-radius: 10px !important;
        font-size: 0.85rem !important;
    }

    /* ── Error / access-denied banner ──
       Only shown when login attempt fails
       ────────────────────────────────── */
    .err-banner {
        background: #fff5f5;
        border: 1px solid #ffcdd2;
        border-left: 4px solid #e53935;
        border-radius: 10px;
        padding: 0.85rem 1.1rem;
        margin-bottom: 0.9rem;
        color: #b71c1c;
        font-size: 0.85rem;
        line-height: 1.55;
        font-family: 'Inter', sans-serif;
    }
    .err-banner b { color: #c62828; }

    /* ── Divider ── */
    .auth-divider {
        border: none;
        border-top: 1px solid #eee;
        margin: 1.2rem 0 0.8rem;
    }

    /* ── Hint text under card ── */
    .auth-hint {
        text-align: center;
        font-size: 0.79rem;
        color: #aaa;
        font-family: 'Inter', sans-serif;
    }
    .auth-hint b { color: #5c6bc0; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #eef0f4; }
    ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)


# Admin credentials (hardcoded) — checked inside login form
_ADMIN_EMAIL    = "admin@gmail.com"
_ADMIN_PASSWORD = "Admin@01"


# ── Login form ───────────────────────────────────────────────────────────────
def _login_form():
    users = _load_users()

    # Show access-denied banner only when explicitly triggered
    if st.session_state.get("login_error"):
        st.markdown(
            f"<div class='err-banner'>🔒 <b>Access Denied</b> — "
            f"{st.session_state['login_error']}</div>",
            unsafe_allow_html=True
        )

    email = st.text_input(
        "Email address", placeholder="you@example.com", key="login_email"
    )

    show_pw = st.checkbox("👁  Show password", key="login_show_pw")
    if show_pw:
        password = st.text_input(
            "Password", placeholder="Enter your password",
            key="login_pw_vis", type="default"
        )
    else:
        password = st.text_input(
            "Password", placeholder="Enter your password",
            key="login_pw_hid", type="password"
        )

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("Sign In →", key="login_btn"):
        if not email or not password:
            st.session_state["login_error"] = "Please fill in all fields."
            st.rerun()

        # ── Admin shortcut: if admin credentials entered → Admin Dashboard ──
        elif email == _ADMIN_EMAIL and password == _ADMIN_PASSWORD:
            st.session_state["login_error"]     = None
            st.session_state["admin_authenticated"] = True
            st.session_state["current_page"]    = "Admin"
            st.rerun()

        elif email not in users:
            st.session_state["login_error"] = (
                "No account found with that email — you are not registered. "
                "Please <b>sign up</b> first."
            )
            st.rerun()
        elif users[email]["password"] != _hash(password):
            st.session_state["login_error"] = "Incorrect password. Please try again."
            st.rerun()
        else:
            st.session_state["login_error"] = None
            st.session_state["authenticated"] = True
            st.session_state["user_name"]  = users[email]["name"]
            st.session_state["user_email"] = email
            st.rerun()

    st.markdown('<hr class="auth-divider"/>', unsafe_allow_html=True)
    st.markdown(
        "<p class='auth-hint'>Don't have an account? "
        "Switch to the <b>Sign Up</b> tab.</p>",
        unsafe_allow_html=True
    )


# ── Signup form ──────────────────────────────────────────────────────────────
def _signup_form():
    users = _load_users()

    full_name = st.text_input(
        "Full name", placeholder="John Doe", key="su_name"
    )
    email = st.text_input(
        "Email address", placeholder="you@example.com", key="su_email"
    )

    show_pw = st.checkbox("👁  Show password", key="su_show_pw")
    if show_pw:
        password  = st.text_input(
            "Password", placeholder="Create a strong password",
            key="su_pw_vis", type="default"
        )
        password2 = st.text_input(
            "Confirm password", placeholder="Repeat password",
            key="su_pw2_vis", type="default"
        )
    else:
        password  = st.text_input(
            "Password", placeholder="Create a strong password",
            key="su_pw_hid", type="password"
        )
        password2 = st.text_input(
            "Confirm password", placeholder="Repeat password",
            key="su_pw2_hid", type="password"
        )

    _show_strength_bar(password)
    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

    if st.button("Create Account →", key="signup_btn"):
        if not full_name or not email or not password or not password2:
            st.error("📋 Please fill in all fields.")
        elif not _is_valid_email(email):
            st.error("📧 Please enter a valid email address.")
        elif email in users:
            st.error("⚠️ An account with this email already exists. Please sign in.")
        elif _password_strength(password)[0] < 2:
            st.error("🔑 Password too weak. Use 8+ chars, a number, and uppercase.")
        elif password != password2:
            st.error("❗ Passwords do not match.")
        else:
            users[email] = {
                "name": full_name.strip(),
                "password": _hash(password),
                "created_at": datetime.utcnow().isoformat()
            }
            _save_users(users)
            st.success(f"🎉 Account created! Welcome, **{full_name.strip()}**. Sign in now.")

    st.markdown('<hr class="auth-divider"/>', unsafe_allow_html=True)
    st.markdown(
        "<p class='auth-hint'>Already have an account? "
        "Switch to the <b>Sign In</b> tab.</p>",
        unsafe_allow_html=True
    )


# ── Legacy entry point kept for import compatibility ─────────────────────────
def render_auth_page() -> bool:
    """
    Legacy function — routing is now managed by app.py.
    Returns True if already authenticated.
    """
    return st.session_state.get("authenticated", False)
