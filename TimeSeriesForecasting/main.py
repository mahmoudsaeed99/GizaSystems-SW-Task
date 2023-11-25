# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 20:46:13 2023

@author: Mahmoud Saeed
"""
from flask import Flask ,jsonify , request ,Response
import json
import joblib
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

import pandas as pd
import numpy as np

from Transformer import TransformedData
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
# df = pd.DataFrame({"value":[1,2,4],"timestamp":["12123","2323","23243"]})


#

#http://127.0.0.1:5000/predict
@app.route("/predict" , methods = ['POST'])
def predict_data():
    data = request.get_json()
    dataset_id = data.get('dataset_id')
    values = data.get('values')
    df = pd.DataFrame(values)
    model = Ridge()
    # read config file
    with open('configs.json') as f:
        data = json.load(f)
    #load only specific configs
    data = data[str(dataset_id)]
    # get model weight
    weights = np.array(data['weight'])
    model.coef_ = weights
    model.intercept_ = data['intercept']

    df = TransformedData(data).transform(df)
    print(df)
    df = df.tail(1)
    df_test = df.drop(['value'], axis=1)
    p = model.predict(df_test)
    dic = {"prediction":list(p)}
    return json.dumps(dic)
if __name__ == "__main__":
    app.run(debug = True )        
