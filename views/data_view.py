import streamlit as st
import pandas as pd
from utils.visualize import plot_time_series

def render_data_view(df, date_col, target_col, stats):
    st.header("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", stats.get('num_rows', 0))
    col2.metric("Total Columns", stats.get('num_columns', 0))
    col3.metric("Missing Values", sum(stats.get('missing_values', {}).values()))
    
    st.subheader("Data Preview & Types")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.write("First 5 rows:")
        st.dataframe(df.head(), width='stretch')
    with col_r:
        st.write("Column Types:")
        st.dataframe(pd.DataFrame(stats.get('dtypes', {}).items(), columns=['Column', 'Type']), width='stretch')

    
    if date_col in df.columns and target_col in df.columns:
        st.subheader("Historical Timeline")
        fig = plot_time_series(df, date_col, target_col, title=f"{target_col.capitalize()} over Time")
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("Please map Date and Target columns correctly to see the timeline.")
