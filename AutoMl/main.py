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
df_train = pd.read_csv("Train_Split.csv")
df_train.drop(['variance'], axis=1, inplace=True)

# Create and fit KNeighborsClassifier
loaded_calibrated_model = KNeighborsClassifier(n_neighbors=3, p=1, weights='distance')
loaded_calibrated_model.fit(df_train.drop(['y'], axis=1), df_train['y'])

@app.route("/calibrated_AutoML/predict" , methods = ['POST'])
def predict():

    # {“variance”:z1, “skewness”:z2, “curtosis”:z3, “entropy”:z4}
    data = request.get_json()
    df = pd.DataFrame(data, index=[0])
    if "variance" in df.columns:
        df.drop(['variance'] , axis = 1 , inplace = True)
    # Get the indices of the k-nearest neighbors
    k_neighbors_indices = loaded_calibrated_model.kneighbors(df, return_distance=False).flatten()

    # Get the labels of the k-nearest neighbors
    k_neighbors_labels = df_train.iloc[k_neighbors_indices]['y']

    # Calculate the predicted probability for the positive class
    predicted_probability_positive_class = k_neighbors_labels.mean()
    prob_positive_class = loaded_calibrated_model.predict_proba(df)
    result = {"output": int(prob_positive_class[:, 1].item())}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True )
