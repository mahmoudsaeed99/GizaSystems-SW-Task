from tpot import TPOTClassifier
import pandas as pd
import numpy as np
import joblib
import json
from flask import Flask ,jsonify , request
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

loaded_calibrated_model = joblib.load('calibrated_model.joblib')

@app.route("/calibrated_AutoML/predict" , methods = ['POST'])
def predict():
    # {“variance”:z1, “skewness”:z2, “curtosis”:z3, “entropy”:z4}
    data = request.get_json()
    df = pd.DataFrame(data, index=[0])
    pred = loaded_calibrated_model.predict(df)[0]
    result = {"output": int(pred)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True )
