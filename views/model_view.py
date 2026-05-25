import streamlit as st
from utils.visualize import plot_forecast, plot_feature_importance

def render_model_view(results_dict, date_col, target_col):
    st.header("⚙️ Model Training Results")
    
    if not results_dict:
        st.info("No models trained yet.")
        return
        
    tabs = st.tabs(list(results_dict.keys()))
    
    for tab, (model_name, res) in zip(tabs, results_dict.items()):
        with tab:
            st.subheader(f"{model_name} Metrics")
            metrics = res['metrics']
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("MAE", metrics.get('MAE', 0))
            col2.metric("RMSE", metrics.get('RMSE', 0))
            col3.metric("MAPE", f"{metrics.get('MAPE', 0):.2f}%")
            col4.metric("R2 Score", metrics.get('R2', 0))
            
            st.subheader("Test Data vs Forecast")
            import pandas as pd
            test_df = pd.DataFrame({
                date_col: res['test_dates'],
                target_col: res['actual']
            })
            train_df = pd.DataFrame(columns=[date_col, target_col])
            
            fig = plot_forecast(train_df, test_df, res['forecast'], date_col, target_col, title=f"{model_name} Forecast on Held-out Data")
            st.plotly_chart(fig, width='stretch')
            
            if model_name == 'XGBoost' and 'model_obj' in res:
                st.subheader("Feature Importance")
                imp = res['model_obj'].get_feature_importance()
                if imp:
                    fig_imp = plot_feature_importance(imp)
                    st.plotly_chart(fig_imp, width='stretch')
