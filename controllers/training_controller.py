import pandas as pd
from models.linear_model import LinearForecaster
from models.xgboost_model import XGBoostForecaster
from models.prophet_model import ProphetForecaster
from utils.preprocess import chronological_split
from utils.logger import get_logger

logger = get_logger(__name__)

class TrainingController:
    def __init__(self, target_col, date_col):
        self.target_col = target_col
        self.date_col = date_col
        self.models = {
            'Linear Regression': LinearForecaster(target_col, date_col),
            'XGBoost': XGBoostForecaster(target_col, date_col),
            'Prophet': ProphetForecaster(target_col, date_col)
        }
        self.metrics = {}

    def train_all(self, df):
        logger.info(f"Splitting data on date_col={self.date_col}, target_col={self.target_col}")
        
        # Ensure sorting by date
        df = df.copy()
        try:
            df[self.date_col] = pd.to_datetime(df[self.date_col])
            df = df.sort_values(by=self.date_col)
        except Exception as e:
            logger.warning(f"Handled date parsing error on column '{self.date_col}'. User needs to select a valid date column.")
            return None, None, {}, {"Pre-processing": f"Could not parse '{self.date_col}' as a date. Please select a valid date column in the sidebar."}


        
        train_df, test_df = chronological_split(df)
        
        results = {}
        successful_models = {}
        error_msgs = {}
        for name, model in self.models.items():
            logger.info(f"Training {name}...")
            try:
                model.fit(train_df)
                metrics = model.evaluate(test_df)
                forecast = model.predict(test_df)
                results[name] = {
                    'metrics': metrics,
                    'forecast': forecast,
                    'actual': test_df[self.target_col].values,
                    'test_dates': test_df[self.date_col].values,
                    'model_obj': model
                }
                self.metrics[name] = metrics
                successful_models[name] = model
                logger.info(f"{name} trained successfully. Metrics: {metrics}")
            except Exception as e:
                logger.error(f"Failed to train {name}: {e}")
                error_msgs[name] = str(e)
                
        self.models = successful_models
        return train_df, test_df, results, error_msgs
