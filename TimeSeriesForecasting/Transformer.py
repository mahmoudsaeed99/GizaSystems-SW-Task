import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import numpy as np

class TimestampFeatureSelection(BaseEstimator, TransformerMixin):
    def __init__(self , cols):
        self.cols = cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        mean_value = X['value'].mean()
        # X['value'].fillna(value=mean_value, inplace=True)
        X['timestamp'] = pd.to_datetime(X['timestamp'])
        X['day_of_week'] = pd.to_datetime(X['timestamp']).dt.dayofweek
        X['month'] = pd.to_datetime(X['timestamp']).dt.month
        X['quarter'] = pd.to_datetime(X['timestamp']).dt.quarter
        X['hour'] = pd.to_datetime(X['timestamp']).dt.hour
        X['minute'] = pd.to_datetime(X['timestamp']).dt.minute
        X['second'] = pd.to_datetime(X['timestamp']).dt.second
        # X = X.drop(columns=['timestamp'])
        # X = X.drop(['anomaly'] , axis = 1)
        self.cols.append('timestamp')
        self.cols.append('value')
        X = X[self.cols]
        return X
class SeasonalityFeatureSelection(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        col = X.drop(['value','timestamp'] , axis = 1).columns
        i = 0
        for c in col:
            df_new = X.set_index(c)
            fft_result = np.fft.fft(df_new['value'])
            psd = np.abs(fft_result) ** 2

            frequencies = np.fft.fftfreq(len(psd), d=1)
            dominant_frequencies = frequencies[np.argsort(psd)[::-1]][:5]

            seasonal_filter = np.isin(np.fft.fftfreq(len(psd), d=1), dominant_frequencies)

            seasonality_component = np.fft.ifft(seasonal_filter * fft_result)
            X[f's{i}'] = seasonality_component.real
            i += 1

        return X

class AverageWeightFeature(BaseEstimator, TransformerMixin):
    def __init__(self , window_size):
        self.window_size = window_size
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['moving_average'] = X['value'].rolling(window=self.window_size,min_periods=1).mean()
        X = X.drop(['timestamp'] , axis = 1)
        return X

class LagFeature(BaseEstimator, TransformerMixin):
    def __init__(self, lag_num=[]):
        self.lag_num = lag_num

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        for i in self.lag_num:
            X[f'lag{i}'] = X['value'].shift(i)
            X[f'lag{i}'] = X[f'lag{i}'].fillna(0)
        return X

class DropOutliers(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X , interpolate ='value'):
        p = X.iloc[[-1]]
        index = X.index
        X = X[:-1]
        Q1 = X[interpolate].quantile(0.25)
        Q3 = X[interpolate].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        X[interpolate][(X[interpolate] < lower_bound) | (X[interpolate] > upper_bound)] = np.nan
        X[interpolate] = X[interpolate].interpolate(method='linear')
        X = pd.concat([X, p])
        X.index = index
        return X




class TransformedData():
    def __init__(self , configs):
        self.configs = configs
        self.preprocessing_pipeline = Pipeline([
                ('timestamp', TimestampFeatureSelection(configs['timestamp_col'])),
                # ('seasonality', SeasonalityFeatureSelection()),
                # ('dropOutlier',DropOutliers()),
                ('weight_avg',AverageWeightFeature(configs['window_avg'])),
                ('lags',LagFeature(configs['lags']))
            ])

    def transform(self , X):
        X['timestamp'] = pd.to_datetime(X['timestamp'])
        time_interval = self.configs['time_interval']
        if time_interval[0] == "minutes":
            new_timestamp = X['timestamp'].iloc[-1] + timedelta(minutes=time_interval[1])
        elif time_interval[0] == "hours":
            new_timestamp = X['timestamp'].iloc[-1] + timedelta(hours=time_interval[1])
        elif time_interval[0] == "days":
            new_timestamp = X['timestamp'].iloc[-1] + timedelta(days=time_interval[1])

        X = X.ffill()
        l = len(X)
        r = pd.DataFrame({'timestamp':[new_timestamp] , "value":[None]})
        X = pd.concat([X, r], ignore_index=True)
        # Apply the pipeline to the training data
        window_size = self.configs['window_avg']
        df_transformed = self.preprocessing_pipeline.fit_transform(X)

        # df_transformed['moving_average'].iloc[-1] = None
        # print(df_transformed['moving_average'])
        # df_transformed['moving_average'] = df_transformed['moving_average'].interpolate(method='linear')
        # print(df_transformed['moving_average'])
        # if l <= window_size:
        #     df_transformed['moving_average'].iloc[-1] = None
        #     df_transformed['moving_average'] = df_transformed['moving_average'].interpolate(method='linear')

        # df_transformed = DropOutliers().transform(df_transformed , interpolate="moving_average")
        # last_weighted_average = df_transformed['moving_average'].iloc[-2]
        #
        # num_values_in_window = min(window_size, len(df_transformed))  # Number of values in the rolling window
        #
        # new_value = df_transformed['value'].iloc[-2]
        #
        # next_weighted_average = ((last_weighted_average * num_values_in_window) + new_value) / (num_values_in_window + 1)

        # df_transformed['moving_average'].iloc[-1] = next_weighted_average
        df_transformed = df_transformed.ffill()
        return df_transformed
