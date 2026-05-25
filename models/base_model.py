from abc import ABC, abstractmethod
from utils.evaluate import evaluate_forecast

class BaseForecaster(ABC):
    def __init__(self, target_col, date_col):
        self.target_col = target_col
        self.date_col = date_col
        self.model = None

    @abstractmethod
    def fit(self, train_df):
        pass

    @abstractmethod
    def predict(self, test_df):
        pass

    def evaluate(self, test_df):
        predictions = self.predict(test_df)
        actuals = test_df[self.target_col].values
        return evaluate_forecast(actuals, predictions)
