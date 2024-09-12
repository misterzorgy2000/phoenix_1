import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
import joblib
import json
import os

from phoenix.conf import CONF
from phoenix.ai import CV_RESULTS_DIR, DS_DATA_DIR, MODEL_DIR

# Model validation
def evaluate_model(model_path):
    target_params = CONF.ai.target
    data = pd.read_csv(f'{DS_DATA_DIR}/data.csv')
    data = data.drop(columns=['resource_id', 'ts'], axis=1)
    with open(model_path, 'rb') as fd:
        model = joblib.load(fd) 

    cv_strategy = StratifiedKFold(n_splits=5)
    
    cv_res = cross_validate(
        model,
        data,
        data['node_disk_read_bytes_total_y'],
        cv=5,
        n_jobs = CONF.ai.n_jobs,
        scoring= CONF.ai.scoring
        )

    for key, value in cv_res.items():
        cv_res[key] = round(value.min(), 3)

    os.makedirs(CV_RESULTS_DIR, exist_ok=True)
    
    with open(f'{CV_RESULTS_DIR}/res.json', 'w') as fd:
        json.dump(cv_res, fd)

if __name__ == '__main__':
	evaluate_model()