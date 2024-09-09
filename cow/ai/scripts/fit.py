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
    
    X = data.drop(columns=['resource_id', 'ts'] + target_params, axis=1)
    y = data['node_disk_read_bytes_total_y']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = CatBoostRegressor(allow_writing_files=False)
    model.fit(X_train, y_train)
    
    for callback in callbacks:
        callback(model)

if __name__ == '__main__':
    fit_model()