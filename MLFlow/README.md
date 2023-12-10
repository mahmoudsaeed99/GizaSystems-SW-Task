# MLFlow Forecasting

This project takes start time stamp  to forecast the next time stamp value

## Getting Started

Follow these steps to run the project.

1. after download the folder you can run the project in two easy way
    * you can open forecasting.py and run the script
    * open command line inside the folder and write `python forecasting.py`
2. send your data to this endpoint http://127.0.0.1:5000/forecast using [POST method] as json data like this :
{
  "dataset_id": "79",
  "start_timestamp": "2021-09-23 00:00:00"
}

