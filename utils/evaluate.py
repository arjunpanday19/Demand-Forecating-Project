import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_forecast(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    # Avoid division by zero
    mask = y_true != 0
    if np.any(mask):
        mape = np.mean(np.abs((y_true[mask] - np.array(y_pred)[mask]) / y_true[mask])) * 100
    else:
        mape = np.nan
        
    r2 = r2_score(y_true, y_pred)
    
    return {
        'MAE': round(mae, 4),
        'RMSE': round(rmse, 4),
        'MAPE': round(mape, 4) if not np.isnan(mape) else 0.0,
        'R2': round(r2, 4)
    }
