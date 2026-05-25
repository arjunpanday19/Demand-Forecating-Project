# 📈 SmartDemand AI: Interactive Demand Forecasting Suite

SmartDemand AI is a modern, high-performance web application designed for interactive time-series demand forecasting. Built on a clean, decoupled **Model-View-Controller (MVC)** architecture and powered by a beautiful **Streamlit** user interface, the platform empowers analysts and business owners to upload historic transaction/demand data, evaluate multiple state-of-the-art forecasting models, and generate future predictions with visual clarity.

---

## 🌟 Key Features

*   **🔒 Secure User Authentication**: Multi-role system supporting registration, secure logins, and dedicated role dashboards (Standard User vs. Admin).
*   **📊 Dynamic EDA & Visualization**: Automatically detects and parses datetime and target variables with interactive **Plotly**-powered time-series charts.
*   **🤖 Multi-Model Ensemble**:
    *   **Prophet**: Robust additive model optimized for daily/weekly/yearly seasonal patterns and holidays.
    *   **XGBoost**: Gradient-boosted decision trees using lagged features for powerful non-linear forecasting.
    *   **Linear Regression**: Clean statistical baseline for trend estimation.
*   **📈 Model Evaluation & Comparison**: Side-by-side performance metrics including **Mean Absolute Error (MAE)**, **Root Mean Squared Error (RMSE)**, and **Mean Absolute Percentage Error (MAPE)**.
*   **🔮 Future Projection & Export**: Configure custom future prediction horizons (up to 365 days/periods) and download predictions directly as a structured CSV.

---

## 🛠️ Technology Stack

*   **Frontend & Dashboard**: [Streamlit](https://streamlit.io/) (with custom modern glassmorphic CSS overrides)
*   **Data Processing**: [Pandas](https://pandas.pydata.org/), [Scikit-learn](https://scikit-learn.org/)
*   **Forecasting Engines**: [Prophet](https://facebook.github.io/prophet/), [XGBoost](https://xgboost.readthedocs.io/)
*   **Visualizations**: [Plotly Express & Graph Objects](https://plotly.com/)
*   **Datasets API**: [HuggingFace Datasets](https://huggingface.co/docs/datasets/)

---

## 📂 Architecture & Directory Structure

The project implements a strict Model-View-Controller pattern to ensure high maintainability and testability:

```text
Demand-Forecasting/
├── app.py                  # Main entry point (Routing, Session, Streamlit layout)
├── config.py               # Global constants & training configurations
├── requirements.txt        # Package dependencies
├── controllers/            # Core business logic orchestrators
│   ├── data_controller.py  # Loading, preprocessing, and EDA analytics
│   ├── training_controller.py # Model orchestration and performance evaluation
│   └── forecast_controller.py # Future timeline extrapolation
├── models/                 # Time-series algorithm wrapper definitions
│   ├── base_model.py       # Abstract base class for standardized model APIs
│   ├── linear_model.py     # Linear Regression forecasting implementation
│   ├── prophet_model.py    # Meta Prophet time-series model implementation
│   └── xgboost_model.py    # XGBoost regression with time-based features
├── utils/                  # Helper utilities and data utilities
│   ├── preprocess.py       # Time-series feature engineering & lag generators
│   ├── evaluate.py         # Error calculation metrics (MAE, RMSE, MAPE)
│   ├── logger.py           # Standardized logger setup
│   └── visualize.py        # Shared plotting utilities
└── views/                  # UI components and page layouts
    ├── layout.py           # Common page layouts & CSS injection
    ├── home_view.py        # Landing page UI
    ├── auth_view.py        # Register / Login screen UIs
    ├── admin_view.py       # Admin controls & user management panel
    ├── data_view.py        # Raw data & EDA plots
    ├── model_view.py       # Metrics comparisons & backtesting plots
    └── forecast_view.py    # Future forecast charts & data downloaders
```

---

## 🚀 Installation & Getting Started

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/arjunpanday19/Demand-Forecating-Project.git
cd Demand-Forecating-Project
```

### 3. Set Up Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 💡 How to Use

1.  **Sign Up / Sign In**: Register a standard user account to log in to the dashboard.
2.  **Load Data**:
    *   Load the **Default HuggingFace Dataset** directly from the sidebar.
    *   *Or* upload your own custom **CSV** file.
3.  **Map Columns**: The system dynamically flags candidate `Date` and `Target` (e.g., sales quantity) columns. Confirm these mappings in the sidebar.
4.  **Train Models**: Click **Train Models** to build the forecasting suite on your data. View comparative MAE, RMSE, and MAPE errors instantly.
5.  **Predict Future Demand**: Set a prediction period (e.g. 30 days), pick your best-performing model, and click **Generate Forecast**. Visualize the forecast range and download the projected dataset!

---

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for more information.
