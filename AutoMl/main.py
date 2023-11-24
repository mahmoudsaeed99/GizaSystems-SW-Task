from tpot import TPOTClassifier
import pandas as pd
import numpy as np
import joblib
import json
from flask import Flask ,jsonify , request
import warnings
from sklearn.neighbors import KNeighborsClassifier
warnings.filterwarnings('ignore')

app = Flask(__name__)
# from sklearn.externals import joblib
# loaded_calibrated_model = joblib.load('knn_model.joblib')
import pickle
# loaded_model = pickle.load(open('knnpickle_file', 'rb'))
# result = loaded_model.predict(X_test)
loaded_calibrated_model = KNeighborsClassifier(n_neighbors=3, p=1, weights='distance')
@app.route("/calibrated_AutoML/predict" , methods = ['POST'])
def predict():
    df = pd.read_csv("Train_Split.csv")
    df.drop(['variance'] , axis = 1 , inplace=True)
    loaded_calibrated_model.fit(df.drop(['y'],axis = 1) , df['y'])
    # {“variance”:z1, “skewness”:z2, “curtosis”:z3, “entropy”:z4}
    data = request.get_json()
    df = pd.DataFrame(data, index=[0])
    if "variance" in df.columns:
        df.drop(['variance'] , axis = 1 , inplace = True)
    pred = loaded_calibrated_model.predict(df)[0]
    result = {"output": int(pred)}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True )
