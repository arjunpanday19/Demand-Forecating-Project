import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from models.base_model import BaseForecaster
from utils.preprocess import create_time_features
from config import TARGET_COL, DATE_COL

class LinearForecaster(BaseForecaster):
    def __init__(self, target_col=TARGET_COL, date_col=DATE_COL):
        super().__init__(target_col, date_col)
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('lr', LinearRegression())
        ])
        self.features = []

    def _prepare_features(self, df):
        df = create_time_features(df, self.date_col)
        # Keep only numeric features
        numeric_df = df.select_dtypes(include=['number'])
        features = [col for col in numeric_df.columns if col not in [self.target_col, self.date_col]]
        return df, features

    def fit(self, train_df):
        df, features = self._prepare_features(train_df)
        self.features = features
        df = df.dropna(subset=self.features + [self.target_col])
        self.model.fit(df[self.features], df[self.target_col])

    def predict(self, test_df):
        df, _ = self._prepare_features(test_df)
        for col in self.features:
            if col not in df.columns:
                df[col] = 0
        df = df.fillna(0)
        return self.model.predict(df[self.features])
