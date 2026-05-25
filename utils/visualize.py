import plotly.graph_objects as go
import plotly.express as px

def plot_time_series(df, date_col, target_col, title="Time Series"):
    fig = px.line(df, x=date_col, y=target_col, title=title, template='plotly_white')
    fig.update_layout(xaxis_title="Date", yaxis_title="Demand")
    return fig

def plot_forecast(train, test, forecast, date_col, target_col, title="Forecast"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=train[date_col], y=train[target_col], mode='lines', name='Train', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=test[date_col], y=test[target_col], mode='lines', name='Actual Test', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=test[date_col], y=forecast, mode='lines', name='Forecast', line=dict(color='orange')))
    fig.update_layout(title=title, template='plotly_white', xaxis_title="Date", yaxis_title="Demand")
    return fig

def plot_feature_importance(importance_dict, title="Feature Importance"):
    features = list(importance_dict.keys())
    scores = list(importance_dict.values())
    fig = px.bar(x=scores, y=features, orientation='h', title=title, template='plotly_white')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Importance", yaxis_title="Feature")
    return fig
