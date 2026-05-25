import pandas as pd
from config import DATE_COL, TARGET_COL, TEST_SIZE_RATIO

def create_time_features(df, date_col=DATE_COL):
    """Extract standard time features from a datetime column."""
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])
    
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['day'] = df[date_col].dt.day
    df['dayofweek'] = df[date_col].dt.dayofweek
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    return df

def create_lag_features(df, target_col=TARGET_COL, lags=[1, 7, 30]):
    df = df.copy()
    for lag in lags:
        df[f'lag_{lag}'] = df[target_col].shift(lag).fillna(method='bfill')
    return df

def create_rolling_features(df, target_col=TARGET_COL, windows=[7, 30]):
    df = df.copy()
    for window in windows:
        df[f'rolling_mean_{window}'] = df[target_col].rolling(window=window, min_periods=1).mean()
        df[f'rolling_std_{window}'] = df[target_col].rolling(window=window, min_periods=1).std().fillna(0)
    return df

def chronological_split(df, test_size=TEST_SIZE_RATIO):
    n = len(df)
    split_idx = int(n * (1 - test_size))
    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()
    return train, test
