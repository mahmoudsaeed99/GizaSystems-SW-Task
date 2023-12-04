from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

def get_timestamp_feature(df):
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['minute'] = pd.to_datetime(df['timestamp']).dt.minute
    df['second'] = pd.to_datetime(df['timestamp']).dt.second
    df['quarter'] = pd.to_datetime(df['timestamp']).dt.quarter
    features = df.drop(columns=['timestamp'] , axis = 1)
    correlations = {}

    target_variable = 'value'

    # Assuming df is your DataFrame
    correlation_matrix = features.corr()

    # Get the absolute correlation values with the target variable
    correlation_with_target = correlation_matrix[target_variable].abs()

    # Select features with correlation above 20%
    selected_features = correlation_with_target[correlation_with_target > 0.2].index.tolist()
    # selected_features.remove(target_variable) if target_variable in selected_features else None
    if "anomaly" in selected_features:
        selected_features.remove("anomaly") if "anomaly" in selected_features else None
    return selected_features
def get_num_of_lags(df):
    from statsmodels.tsa.stattools import pacf

    max_lag = 10
    # Calculate PACF values
    pacf_values = pacf(df['value'], nlags=max_lag)

    # Extract features based on significant PACF values
    significant_lags = [lag for lag, pacf_value in enumerate(pacf_values) if abs(pacf_value) > 0.2]
    significant_lags = significant_lags[1:]
    return significant_lags

