from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from sklearn.pipeline import Pipeline

class TimestampFeatureSelection(BaseEstimator, TransformerMixin):
        def __init__(self , features):
            self.features = features
        def fit(self, X, y=None):
            return self

        def transform(self, X):
            X['day_of_week'] = pd.to_datetime(X['timestamp']).dt.dayofweek
            X['month'] = pd.to_datetime(X['timestamp']).dt.month
            X['hour'] = pd.to_datetime(X['timestamp']).dt.hour
            X['minute'] = pd.to_datetime(X['timestamp']).dt.minute
            X['second'] = pd.to_datetime(X['timestamp']).dt.second
            X['quarter'] = pd.to_datetime(X['timestamp']).dt.quarter
            X = X[self.features]
            return X

class LagFeature(BaseEstimator, TransformerMixin):
        def __init__(self , lag_num = [1]):
            self.lag_num = lag_num

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            for i in self.lag_num:
                X[f'lag{i}'] = X['value'].shift(i)
                # X[f'lag{i}'] = X[f'lag{i}'].fillna(0)
            # print(X)
            X.dropna(inplace = True)
            return X


def forecastingPipeline(data = [] , lag_num = [] , features = []):
    if len(data) == 0:
        return Exception("you should add your dataframe")

    preprocessing_pipeline = Pipeline([
            ('timestamp', TimestampFeatureSelection(features)),
            ('lags',LagFeature(lag_num))
    ])
    # Log parameters with MLflow
    df_transformed = preprocessing_pipeline.fit_transform(data)
    return df_transformed
