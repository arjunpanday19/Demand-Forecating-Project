import xgboost as xgb
from models.base_model import BaseForecaster
from utils.preprocess import create_time_features
from config import TARGET_COL, DATE_COL

class XGBoostForecaster(BaseForecaster):
    def __init__(self, target_col=TARGET_COL, date_col=DATE_COL, n_estimators=100, learning_rate=0.1):
        super().__init__(target_col, date_col)
        self.model = xgb.XGBRegressor(n_estimators=n_estimators, learning_rate=learning_rate, early_stopping_rounds=10)
        self.features = []

    def _prepare_features(self, df):
        df = create_time_features(df, self.date_col)
        # Keep only numeric features
        numeric_df = df.select_dtypes(include=['number'])
        features = [col for col in numeric_df.columns if col not in [self.target_col, self.date_col]]
        return df, features

    def fit(self, train_df):
        df, self.features = self._prepare_features(train_df)
        df = df.dropna(subset=self.features + [self.target_col])
        
        split_idx = int(len(df) * 0.8)
        if split_idx == 0 or split_idx == len(df):
            # Not enough data for val set
            self.model.set_params(early_stopping_rounds=None)
            self.model.fit(df[self.features], df[self.target_col], verbose=False)
        else:
            X_train, y_train = df[self.features].iloc[:split_idx], df[self.target_col].iloc[:split_idx]
            X_val, y_val = df[self.features].iloc[split_idx:], df[self.target_col].iloc[split_idx:]
            
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                verbose=False
            )

    def predict(self, test_df):
        df, _ = self._prepare_features(test_df)
        for col in self.features:
            if col not in df.columns:
                df[col] = 0
        df = df.fillna(0)
        return self.model.predict(df[self.features])
        
    def get_feature_importance(self):
        if not self.features:
            return {}
        importance = self.model.feature_importances_
        # Sort by importance
        imp_dict = {f: float(imp) for f, imp in zip(self.features, importance)}
        return dict(sorted(imp_dict.items(), key=lambda item: item[1]))
