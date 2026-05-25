import pandas as pd
from prophet import Prophet
from models.base_model import BaseForecaster
from config import TARGET_COL, DATE_COL
import logging

# Suppress cmdstanpy logging completely
logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.CRITICAL)

class ProphetForecaster(BaseForecaster):
    def __init__(self, target_col=TARGET_COL, date_col=DATE_COL):
        super().__init__(target_col, date_col)
        self.model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)

    def _prepare_prophet_df(self, df):
        p_df = df[[self.date_col, self.target_col]].copy()
        if not pd.api.types.is_datetime64_any_dtype(p_df[self.date_col]):
            p_df[self.date_col] = pd.to_datetime(p_df[self.date_col])
        p_df = p_df.rename(columns={self.date_col: 'ds', self.target_col: 'y'})
        return p_df

    def fit(self, train_df):
        p_df = self._prepare_prophet_df(train_df)
        p_df = p_df.dropna()
        self.model.fit(p_df)

    def predict(self, test_df):
        future = test_df[[self.date_col]].copy()
        if not pd.api.types.is_datetime64_any_dtype(future[self.date_col]):
            future[self.date_col] = pd.to_datetime(future[self.date_col])
        future = future.rename(columns={self.date_col: 'ds'})
        forecast = self.model.predict(future)
        return forecast['yhat'].values
