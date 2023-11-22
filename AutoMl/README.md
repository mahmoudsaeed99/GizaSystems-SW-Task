# AutoML project

This project takes one row to predict the target using calibrated model

## Getting Started

Follow these steps to run the project.

1. after download the folder you can run the project in two easy way
    * you can open main.py and run the script
    * open command line inside the folder and write `python main.py`
2. send your data to this endpoint http://127.0.0.1:5000/calibrated_AutoML/predict using [POST method] as json data like this :
{
    "variance":-5.2049,
    "skewness":7.259,
    "curtosis":0.070827,
    "entropy":-7.3004
}
3. finally you should receive data in this format 
{ 
    "output": 1 
}
