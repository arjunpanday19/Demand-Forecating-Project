import pandas as pd
from datasets import load_dataset
from utils.logger import get_logger

logger = get_logger(__name__)

class DataController:
    def __init__(self):
        self.df = None

    def load_default_dataset(self):
        logger.info("Loading default dataset from HuggingFace...")
        # Try load_dataset first
        try:
            ds = load_dataset("electricsheepafrica/nigerian_energy_and_utilities_demand_forecasting")
            self.df = ds['train'].to_pandas()
            logger.info(f"Dataset loaded via datasets library. Shape: {self.df.shape}")
            return True, "Loaded via datasets library"
        except Exception as e:
            logger.warning(f"Failed to load via datasets library: {e}. Trying fallback...")
            
        # Fallback to direct parquet load
        try:
            url = "hf://datasets/electricsheepafrica/nigerian_energy_and_utilities_demand_forecasting/nigerian_energy_and_utilities_demand_forecasting.parquet"
            self.df = pd.read_parquet(url)
            logger.info(f"Dataset loaded via direct parquet fallback. Shape: {self.df.shape}")
            return True, "Loaded via direct parquet fallback"
        except Exception as e:
            logger.error(f"Failed to load via fallback: {e}")
            return False, str(e)

    def load_csv(self, file):
        try:
            self.df = pd.read_csv(file)
            logger.info("CSV loaded successfully.")
            return self.df
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            return None

    def get_eda_stats(self):
        if self.df is None:
            return {}
        
        stats = {
            'num_rows': len(self.df),
            'num_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'dtypes': self.df.dtypes.astype(str).to_dict()
        }
        return stats
