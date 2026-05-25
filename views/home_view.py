import streamlit as st


def render_home_page():
    """Renders the public Home Page with project info — light / off-white theme."""

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

    /* ── Hero ── */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem 2.5rem;
        background: linear-gradient(135deg, #3949ab 0%, #5c6bc0 60%, #7986cb 100%);
        border-radius: 24px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(57,73,171,0.22);
    }
    .hero-section * {
        text-align: center !important;
    }
    .hero-section p.hero-subtitle {
        display: block;
        width: 100%;
        max-width: 580px;
        margin: 0 auto !important;
        text-align: center !important;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -40%;
        right: -10%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 50px;
        padding: 0.32rem 1rem;
        font-size: 0.75rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 1.1rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.9rem;
        line-height: 1.18;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: rgba(255,255,255,0.82);
        width: 100%;
        max-width: 580px;
        margin: 0 auto;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.7;
        font-weight: 400;
        text-align: center;
    }

    /* ── Stats row ── */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.8rem;
    }
    .stat-chip {
        flex: 1;
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.18s, box-shadow 0.18s;
    }
    .stat-chip:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(57,73,171,0.1);
    }
    .stat-number {
        font-size: 1.9rem;
        font-weight: 800;
        color: #3949ab;
        display: block;
        line-height: 1;
        margin-bottom: 0.35rem;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #9ea3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Section cards ── */
    .section-card {
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 18px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.18s, box-shadow 0.18s;
    }
    .section-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(57,73,171,0.09);
    }
    .section-icon {
        font-size: 2rem;
        margin-bottom: 0.6rem;
        display: block;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0 0 0.8rem;
        letter-spacing: -0.2px;
    }
    .section-text {
        color: #5a6075;
        font-size: 0.93rem;
        line-height: 1.75;
        margin: 0;
    }

    /* ── Feature grid ── */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1.2rem;
    }
    .feature-item {
        background: #f5f6fa;
        border: 1px solid #e8eaf0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        transition: border-color 0.15s, background 0.15s;
    }
    .feature-item:hover {
        background: #eef0fc;
        border-color: #c5cae9;
    }
    .feature-item-icon {
        font-size: 1.4rem;
        flex-shrink: 0;
        margin-top: 0.05rem;
    }
    .feature-item-text strong {
        display: block;
        color: #2c3e6a;
        font-size: 0.87rem;
        font-weight: 600;
        margin-bottom: 0.22rem;
    }
    .feature-item-text span {
        color: #7a8099;
        font-size: 0.79rem;
        line-height: 1.5;
    }

    /* ── Objective list ── */
    .objective-list { list-style: none; padding: 0; margin: 0; }
    .objective-list li {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.65rem 0;
        border-bottom: 1px solid #f0f1f8;
        color: #5a6075;
        font-size: 0.92rem;
        line-height: 1.6;
    }
    .objective-list li:last-child { border-bottom: none; }
    .obj-bullet {
        width: 22px;
        height: 22px;
        background: linear-gradient(135deg, #3949ab, #5c6bc0);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.68rem;
        color: white;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 2px;
    }

    /* ── CTA ── */
    .cta-section {
        text-align: center;
        padding: 2.2rem 2rem;
        background: linear-gradient(135deg, #eef0fc 0%, #e8eaf8 100%);
        border: 1px solid #c5cae9;
        border-radius: 18px;
        margin-top: 0.5rem;
    }
    .cta-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.45rem;
    }
    .cta-text {
        color: #7a8099;
        font-size: 0.88rem;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">📈 AI-Powered Platform</div>
        <h1 class="hero-title" style= "color: white" >Demand Forecasting<br>Intelligence System</h1>
        <p class="hero-subtitle" >
            Leverage advanced machine learning algorithms to predict future demand,
            optimize your supply chain, and make data-driven decisions with confidence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="stats-row">
        <div class="stat-chip">
            <span class="stat-number">5+</span>
            <span class="stat-label">ML Models</span>
        </div>
        <div class="stat-chip">
            <span class="stat-number">95%</span>
            <span class="stat-label">Accuracy</span>
        </div>
        <div class="stat-chip">
            <span class="stat-number">365</span>
            <span class="stat-label">Days Forecast</span>
        </div>
        <div class="stat-chip">
            <span class="stat-number">24/7</span>
            <span class="stat-label">Available</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Introduction ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
        <span class="section-icon">🔍</span>
        <h2 class="section-title" style="color:#3949ab;">Introduction</h2>
        <p class="section-text">
            The <strong style="color:#3949ab;">Demand Forecasting Intelligence System</strong> is a
            state-of-the-art machine learning platform built to help businesses, supply chain managers,
            and analysts predict future product demand with remarkable accuracy. By combining classical
            statistical methods with modern ensemble learning algorithms, the system transforms raw
            historical sales data into actionable forward-looking forecasts.
            <br><br>
            Whether you're a retail business managing inventory, a manufacturer planning production
            cycles, or a logistics company optimizing delivery routes — accurate demand forecasting is
            the cornerstone of operational efficiency. This platform makes that capability accessible
            through an intuitive interface, removing the need for deep data science expertise.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Objectives ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
        <span class="section-icon">🎯</span>
        <h2 class="section-title" style="color:#3949ab;">Objectives</h2>
        <ul class="objective-list">
            <li>
                <div class="obj-bullet">1</div>
                <span>Accurately forecast future product demand using state-of-the-art machine learning models trained on historical time-series data.</span>
            </li>
            <li>
                <div class="obj-bullet">2</div>
                <span>Enable businesses to reduce overstock and stockout scenarios by providing intelligent inventory planning insights.</span>
            </li>
            <li>
                <div class="obj-bullet">3</div>
                <span>Support data ingestion from multiple sources — including live HuggingFace datasets and custom CSV uploads — for maximum flexibility.</span>
            </li>
            <li>
                <div class="obj-bullet">4</div>
                <span>Provide comprehensive model evaluation metrics (MAE, RMSE, R²) to help users select the best-performing model.</span>
            </li>
            <li>
                <div class="obj-bullet">5</div>
                <span>Deliver interactive visualizations of historical trends, model predictions, and future forecasts for clear business insights.</span>
            </li>
            <li>
                <div class="obj-bullet">6</div>
                <span>Empower non-technical users with a secure, easy-to-use interface backed by a robust authentication and admin management system.</span>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Functionality ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
        <span class="section-icon">⚙️</span>
        <h2 class="section-title" style="color:#3949ab;">Key Functionalities</h2>
        <p class="section-text" style="margin-bottom:1rem;">
            The platform is packed with powerful features designed to make demand forecasting
            seamless from data ingestion to forecast generation.
        </p>
        <div class="feature-grid">
            <div class="feature-item">
                <span class="feature-item-icon">📂</span>
                <div class="feature-item-text">
                    <strong>Flexible Data Loading</strong>
                    <span>Load data from HuggingFace's open datasets or upload your own CSV files with automatic column detection.</span>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-item-icon">🤖</span>
                <div class="feature-item-text">
                    <strong>Multi-Model Training</strong>
                    <span>Train and compare multiple ML models: Linear Regression, Random Forest, XGBoost, and more simultaneously.</span>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-item-icon">📊</span>
                <div class="feature-item-text">
                    <strong>EDA &amp; Visualization</strong>
                    <span>Explore your data with automated statistical analysis, trend plots, and distribution charts.</span>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-item-icon">🔮</span>
                <div class="feature-item-text">
                    <strong>Future Forecasting</strong>
                    <span>Generate demand forecasts up to 365 days into the future using your best-performing trained model.</span>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-item-icon">📈</span>
                <div class="feature-item-text">
                    <strong>Model Comparison</strong>
                    <span>Compare MAE, RMSE, and R² metrics across all models with interactive bar charts to pick the winner.</span>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-item-icon">🔐</span>
                <div class="feature-item-text">
                    <strong>Secure Authentication</strong>
                    <span>Full user registration and login with password hashing, strength validation, and admin management.</span>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-item-icon"></span>
                <div class="feature-item-text">
                    <strong>Admin Dashboard</strong>
                    <span>Admin panel to monitor all registered users with account details and registration timestamps.</span>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-item-icon">☁️</span>
                <div class="feature-item-text">
                    <strong>Cloud-Ready</strong>
                    <span>Built on Streamlit — deployable to Streamlit Cloud, AWS, GCP, or any container environment.</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">🚀 Ready to Forecast Smarter?</div>
        <p class="cta-text">Sign in or create an account to start making data-driven decisions today.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:center;color:#c8cad8;font-size:0.73rem;margin-top:2rem;font-family:'Inter',sans-serif;">
        © 2025 Demand Forecasting Intelligence System · Powered by Machine Learning
    </p>
    """, unsafe_allow_html=True)
