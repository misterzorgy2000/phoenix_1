import pandas as pd
import os
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor

from cow.conf import CONF
from cow.ai import DS_DATA_DIR, MODEL_DIR

def fit_model(callbacks = []):
    os.makedirs(MODEL_DIR, exist_ok=True, mode=0o777)
    target_params = CONF.ai.target
    
    data = pd.read_csv(f'{DS_DATA_DIR}/data.csv')
    
    X = data
    
    X = X[['CPU load 5 avg', 'Temperature', 'Time', 'Datetime']]
    y = data['Power Consumption']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6)
    
    model = CatBoostRegressor(allow_writing_files=False)
    model.fit(X_train.drop('Datetime', axis=1), y_train) 
    
    for callback in callbacks:
        callback(model)

if __name__ == '__main__':
    fit_model()