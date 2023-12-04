from tpot import TPOTClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, f1_score

from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.calibration import CalibratedClassifierCV
import joblib
import pickle


def train_model(df):
    X_train , X_test , y_train , y_test = train_test_split(df.drop(['y'] , axis = 1) , df['y'] ,
                                                           test_size=0.2, random_state=42)
    scorer = make_scorer(f1_score)
    preprocessor = StandardScaler()
    custom_config = {
        'sklearn.ensemble.RandomForestClassifier': {},
        'sklearn.naive_bayes.GaussianNB': {},
        'sklearn.linear_model.LogisticRegression': {},
        # Add or remove classifiers as needed
    }
    tpot = TPOTClassifier(
        # config_dict=custom_config,
        population_size=80,
        generations = 5,
        cv=5,
        scoring='f1',
        random_state=42,
        verbosity=2
    )
    x = df.drop(['y'] , axis = 1)
    y = df[['y']]

    tpot.fit( x, y)

    # Evaluate the best pipeline on the test set
    y_pred = tpot.predict(X_test)
    test_f1_score = f1_score(y_test, y_pred, average='weighted')

    print(f"Best pipeline F1-Score on test set: {test_f1_score}")
    print("Best pipeline:")
    print(tpot.fitted_pipeline_)
    return tpot.fitted_pipeline_

def calibrate_model(best_pipeline):
    calibrated_model_sigmoid = CalibratedClassifierCV(best_pipeline, method='sigmoid', cv='prefit')
    calibrated_model_sigmoid.fit(X_train, y_train)
    pred_y = calibrated_model_sigmoid.predict(X_test)
    print(f1_score(y_test , pred_y))
    return calibrated_model_sigmoid

if __name__ == '__main__':
    df = pd.read_csv("/content/drive/MyDrive/AutoML/Train_Split.csv")
    best_pipeline = train_model(df)
    calibratedModel = calibrate_model(best_pipeline)
    print(calibratedModel)
    with open('knn_model.pkl', 'wb') as model_file:
        pickle.dump(calibratedModel, model_file)








