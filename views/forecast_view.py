import streamlit as st

def render_forecast_view(future_df, date_col):
    st.header("🚀 Future Predictions")
    
    st.subheader("Forecast Data")
    st.dataframe(future_df, width='stretch')
    
    import plotly.express as px
    fig = px.line(future_df, x=date_col, y='Forecast', title="Future Forecast", template='plotly_white', color_discrete_sequence=['orange'])
    fig.update_layout(xaxis_title="Date", yaxis_title="Predicted Demand")
    st.plotly_chart(fig, width='stretch')
    
    csv = future_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Forecast as CSV",
        data=csv,
        file_name='future_forecast.csv',
        mime='text/csv'
    )
