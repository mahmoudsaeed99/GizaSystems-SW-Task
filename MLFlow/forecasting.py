import mlflow
import pandas as pd
import ast
from datetime import timedelta

from flask import Flask, request, jsonify

from pipeline import forecastingPipeline
def load_parameters(run_id):
    # Load parameters from the run
    loaded_params = mlflow.get_run(run_id).data.params

    # Convert string representations to actual Python objects
    loaded_params["number_of_lags"] = ast.literal_eval(loaded_params["number_of_lags"])
    loaded_params["features"] = ast.literal_eval(loaded_params["features"])
    days, rest = loaded_params["timeDiff"].split(" days ")
    hours, minutes, seconds = rest.split(":")
    loaded_params["timeDiff"] = timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    return loaded_params
from pipeline import forecastingPipeline
def forecast_next_timestamp(model, dataset_id , time):
    # You need to implement the forecasting logic here
    # Load the trained model
    with mlflow.start_run():
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        # Search for the model using the dataset_id
        runs = mlflow.search_runs(filter_string=f"params.dataset_id='{dataset_id}'")
        if runs.empty:
            print(f"No model found for dataset_id {dataset_id}")
            return None

        run_id = runs.iloc[0].run_id
        model_path = f"runs:/{run_id}/time_series_model"
        loaded_model = mlflow.sklearn.load_model(model_path)

        # load parameters
        loaded_params = load_parameters(run_id)
        lag_num = loaded_params['number_of_lags']
        features = loaded_params['features']
        timeDiff = loaded_params['timeDiff']
        # get prev row from our data
        prev_time = pd.to_datetime(time) - timeDiff
        data = pd.read_csv(f"forecasting_train_splits/train_{dataset_id}.csv")
        # select the row index to get prev num of lags
        index = data[data['timestamp'] == str(prev_time)].index[0]
        data = data.iloc[index - max(lag_num)+1:index+1]
        data['value'].fillna(int(data['value'].mean()) , inplace = True)
        # add last row that we want to forecast
        new_data = pd.DataFrame({'timestamp':[time],"value":[None]})
        data = pd.concat([data , new_data] , ignore_index=True)
        # fill all nan value with mean
        data['value'].fillna(int(data['value'].mean()) , inplace = True)
        # transform the data using pipe line
        data_transformed = forecastingPipeline(data= data , features= features , lag_num= lag_num)
        forecast_result = loaded_model.predict(data_transformed.drop(['value'] ,axis = 1))
        return forecast_result[0]

app = Flask(__name__)

#http://127.0.0.1:5000/forecast
@app.route("/forecast" , methods = ['POST'])
def forecast():
    # Assuming you have a list of datasets for which you want to forecast

    data = request.get_json()

    dataset_id = data.get('dataset_id')
    time = data.get('start_timestamp')
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    # Call your forecasting function
    forecast_result = forecast_next_timestamp(model=None, dataset_id=dataset_id , time = time)

    if forecast_result is not None:
        response = {
        "prediction": forecast_result,
        "timestamp": time
        }

    else:
        return Exception("error in forecasting")
    return response

if __name__ == "__main__":
    app.run(debug = True )
