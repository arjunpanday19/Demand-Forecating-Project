import pandas as pd
import numpy as np

class ForecastController:
    def __init__(self, models_dict):
        # models_dict corresponds to self.models from TrainingController
        self.models = models_dict

    def generate_future_forecast(self, current_df, date_col, periods, freq='D', model_name='Prophet'):
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found or not trained.")

        try:
            last_date = pd.to_datetime(current_df[date_col]).max()
        except Exception as e:
            raise ValueError(f"Could not parse '{date_col}' as a date for forecasting: {e}")
            
        future_dates = pd.date_range(start=last_date, periods=periods + 1, freq=freq)[1:]

        
        future_df = pd.DataFrame({date_col: future_dates})
        
        preds = model.predict(future_df)
        future_df['Forecast'] = preds
        
        return future_df
