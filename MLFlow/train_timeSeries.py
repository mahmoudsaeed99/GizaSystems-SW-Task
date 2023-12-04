import mlflow
import mlflow.sklearn
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")
from processing import get_num_of_lags , get_timestamp_feature
from pipeline import forecastingPipeline

def train_time_series_model(train_data, dataset_id):
    # Your time series model training code here
    # ..
    train_data['value'].fillna(int(train_data['value'].mean()) , inplace = True)
    train_data['timestamp'] = pd.to_datetime(train_data['timestamp'])
    time_difference = train_data['timestamp'].iloc[-1] - train_data['timestamp'].iloc[-2]
    features = get_timestamp_feature(train_data)
    lag_num = get_num_of_lags(train_data)
    lag_num = lag_num if len(lag_num) != 0 else [1]

    with mlflow.start_run():
        mlflow.log_param("dataset_id", dataset_id)
        mlflow.log_param("number_of_lags", lag_num)
        mlflow.log_param("features", features)
        mlflow.log_param("timeDiff", time_difference)

        #make pipe line
        df_transformed = forecastingPipeline(data=train_data , lag_num= lag_num , features=features)
        model = RandomForestRegressor()
        model.fit(df_transformed.drop(['value'] , axis = 1) , df_transformed['value'])
        mlflow.sklearn.log_model(model, "time_series_model")


if __name__ == '__main__':
    # Set up MLflow with SQLite backend
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    # Assuming you have a list of 96 datasets
    directory_path = 'forecasting_train_splits/'

    # List all files in the directory
    all_files = os.listdir(directory_path)

    # Filter files with CSV extension
    csv_files = [file for file in all_files if file.endswith('.csv')]

    for file in csv_files:
        file_path = os.path.join(directory_path, file)

        # Read the CSV file into a DataFrame using pandas
        df = pd.read_csv(file_path)
        import re
        match = re.search(r'\d+', file)
        extracted_number = match.group()
        train_time_series_model(df , extracted_number)




