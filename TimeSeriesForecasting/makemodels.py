import pandas as pd
import json
dataset_id = 9

df = pd.read_csv('./forecasting_train_splits/train_9.csv')
from Transformer import TransformedData
with open('configs.json') as f:
    data = json.load(f)

trans = TransformedData(data[str(dataset_id)])
df = trans.preprocessing_pipeline.fit_transform(df)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from joblib import dump

# Assuming you already have df with the 'moving_average' column
X_train = df.drop(['value'], axis=1)
y_train = df['value']


# Build a model (you can replace this with any model of your choice)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

dump(model,f'./models/model_{dataset_id}.joblib')
