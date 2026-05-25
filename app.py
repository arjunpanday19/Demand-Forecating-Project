import streamlit as st
import pandas as pd

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Views ─────────────────────────────────────────────────────────────────────
from views.layout        import inject_custom_css, render_sidebar
from views.home_view     import render_home_page
from views.auth_view     import render_auth_page, _login_form, _signup_form, _inject_auth_css
from views.admin_view    import render_admin_page
from views.data_view     import render_data_view
from views.model_view    import render_model_view
from views.forecast_view import render_forecast_view

# ── Controllers ───────────────────────────────────────────────────────────────
from controllers.data_controller     import DataController
from controllers.training_controller import TrainingController
from controllers.forecast_controller import ForecastController


def _init_session():
    """Initialise session-state defaults."""
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"
    if "login_error" not in st.session_state:
        st.session_state["login_error"] = None
    if "admin_login_error" not in st.session_state:
        st.session_state["admin_login_error"] = None


# ─────────────────────────────────────────────────────────────────────────────
def _render_login_page():
    """Standalone Login page with sidebar."""
    _inject_auth_css()
    st.markdown("""
    <div style="text-align:center;padding:0.5rem 0 1.8rem;font-family:'Inter',sans-serif;">
        <div style="font-size:2.5rem;margin-bottom:0.4rem;">🔑</div>
        <h1 style="font-size:1.6rem;font-weight:700;color:#1a1a2e;margin:0 0 0.25rem;">
            Sign In
        </h1>
        <p style="color:#888;font-size:0.86rem;margin:0;" >
            Welcome back — access your forecasting dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 1.6, 1])
    with col_c:
        _login_form()

    # After successful user login → forecasting app
    if st.session_state.get("authenticated"):
        st.session_state["current_page"] = "App"
        st.rerun()
    # After admin login (set inside _login_form) → admin page
    if st.session_state.get("admin_authenticated"):
        st.session_state["current_page"] = "Admin"
        st.rerun()


def _render_signup_page():
    """Standalone Sign Up page with sidebar."""
    _inject_auth_css()
    st.markdown("""
    <div style="text-align:center;padding:0.5rem 0 1.8rem;font-family:'Inter',sans-serif;">
        <div style="font-size:2.5rem;margin-bottom:0.4rem;">📝</div>
        <h1 style="font-size:1.6rem;font-weight:700;color:#1a1a2e;margin:0 0 0.25rem;">
            Create Account
        </h1>
        <p style="color:#888;font-size:0.86rem;margin:0;">
            Join the platform and start forecasting demand
        </p>
    </div>
    """, unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 1.6, 1])
    with col_c:
        from views.auth_view import _signup_form
        _signup_form()


# ─────────────────────────────────────────────────────────────────────────────
def _render_forecasting_app():
    """The main forecasting dashboard (requires login)."""
    if not st.session_state.get("authenticated"):
        st.session_state["current_page"] = "Login"
        st.rerun()
        return

    inject_custom_css()

    if "data_controller" not in st.session_state:
        st.session_state["data_controller"] = DataController()
    if "train_results" not in st.session_state:
        st.session_state["train_results"] = None
    if "models" not in st.session_state:
        st.session_state["models"] = None

    dc = st.session_state["data_controller"]

    with st.sidebar:
        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.66rem;color:#9ea3b8;"
            "text-transform:uppercase;letter-spacing:1.2px;font-weight:600;"
            "padding:0 0.2rem;margin-bottom:0.4rem;'>Forecasting Tools</div>",
            unsafe_allow_html=True
        )
        st.markdown("### 1. Data Source")
        data_source = st.radio("Choose source", ["Default HuggingFace Dataset", "Upload CSV"])

        if data_source == "Default HuggingFace Dataset":
            if st.button("Load Default Data"):
                with st.spinner("Loading..."):
                    success, msg = dc.load_default_dataset()
                    if success:
                        st.success(f"Data Loaded! ({msg})")
                    else:
                        st.error(f"Failed to load: {msg}")
        else:
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file:
                with st.spinner("Processing CSV..."):
                    df = dc.load_csv(uploaded_file)
                    if df is not None:
                        st.success("CSV Loaded!")
                    else:
                        st.error("Failed to load CSV.")

        st.markdown("---")
        date_col   = None
        target_col = None

        if dc.df is not None:
            stats = dc.get_eda_stats()
            st.markdown("### 2. Column Mapping")
            cols = list(dc.df.columns)

            date_keywords    = ["date", "time", "period", "year", "month", "day", "epoch"]
            date_exclusions  = ["region", "category", "name", "id", "code", "sku", "product",
                                 "customer", "price", "amt", "value", "type", "store"]
            target_keywords  = ["demand", "value", "target", "quantity", "sales", "amt",
                                 "qty", "amount", "total"]

            def_date = next((c for c, t in stats.get("dtypes", {}).items() if "datetime" in t), None)
            if not def_date:
                def_date = next(
                    (c for c in cols if any(k in c.lower() for k in date_keywords)
                     and not any(k in c.lower() for k in date_exclusions)), None
                )
            confidence_msg = None
            if not def_date:
                def_date = next(
                    (c for c in cols if not any(k in c.lower() for k in date_exclusions)), cols[0]
                )
                confidence_msg = "⚠️ Could not find a clear Date column. Please verify below."

            def_target = next((c for c in cols if any(k in c.lower() for k in target_keywords)), cols[-1])

            if confidence_msg:
                st.warning(confidence_msg)

            date_col   = st.selectbox("Date Column",   cols, index=cols.index(def_date)   if def_date   in cols else 0)
            target_col = st.selectbox("Target Column", cols, index=cols.index(def_target) if def_target in cols else 0)

            if date_col == target_col:
                st.error("Date and Target columns cannot be the same!")

            st.markdown("### 3. Training")
            if st.button("Train Models") and date_col != target_col:
                with st.spinner("Training models..."):
                    tc = TrainingController(target_col, date_col)
                    train_df, _, results, errors = tc.train_all(dc.df)
                    st.session_state["train_results"] = results
                    st.session_state["models"]        = tc.models
                    st.session_state["trained_date_col"] = date_col

                    for model_name, err in (errors or {}).items():
                        st.warning(f"Failed to train {model_name}: {err}")
                    if results:
                        st.success("Training Complete!")
                    else:
                        st.error("No models trained successfully.")

            if st.session_state["models"]:
                st.markdown("### 4. Forecasting")
                forecast_periods = st.number_input("Periods to Forecast", min_value=1, max_value=365, value=30)
                selected_model   = st.selectbox("Model to Use", list(st.session_state["models"].keys()))
                if st.button("Generate Forecast"):
                    fc = ForecastController(st.session_state["models"])
                    with st.spinner("Generating Forecast..."):
                        try:
                            trained_date_col = st.session_state.get("trained_date_col", date_col)
                            future_df = fc.generate_future_forecast(
                                dc.df, trained_date_col, forecast_periods, model_name=selected_model
                            )
                            st.session_state["future_df"]          = future_df
                            st.session_state["forecast_date_col"]  = trained_date_col
                            st.success("Forecast Ready!")
                        except Exception as e:
                            st.error(f"Error during forecasting: {e}")

    # ── Main content ──────────────────────────────────────────────────────────
    st.title("📈 Demand Forecasting Dashboard")
    if dc.df is not None and date_col and target_col:
        stats = dc.get_eda_stats()
        render_data_view(dc.df, date_col, target_col, stats)
        st.markdown("---")
        if st.session_state["train_results"]:
            render_model_view(st.session_state["train_results"], date_col, target_col)
        if "future_df" in st.session_state:
            st.markdown("---")
            render_forecast_view(
                st.session_state["future_df"],
                st.session_state["forecast_date_col"]
            )
    else:
        st.info("👈 Please load data from the sidebar to begin.")


# ─────────────────────────────────────────────────────────────────────────────
def main():
    _init_session()

    current_page = st.session_state.get("current_page", "Home")

    # Render sidebar and handle navigation clicks
    # (sidebar is always rendered; it returns the newly selected page)
    # For Login/Signup pages we override background via auth CSS, but sidebar still shows
    new_page = render_sidebar(current_page)
    if new_page != current_page:
        st.session_state["current_page"] = new_page
        st.rerun()

    # ── Route to page ─────────────────────────────────────────────────────────
    if current_page == "Home":
        if st.session_state.get("authenticated"):
            st.session_state["current_page"] = "App"
            st.rerun()
        elif st.session_state.get("admin_authenticated"):
            st.session_state["current_page"] = "Admin"
            st.rerun()
        render_home_page()

    elif current_page == "Login":
        _render_login_page()

    elif current_page == "Signup":
        _render_signup_page()

    elif current_page == "Admin":
        render_admin_page()

    elif current_page == "App":
        _render_forecasting_app()

    else:
        render_home_page()


if __name__ == "__main__":
    main()
