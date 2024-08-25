import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
import joblib
import json
import os

from cow.ai import CV_RESULTS_DIR, DS_DATA_DIR, MODEL_DIR

def evaluate_model():
    data = pd.read_csv(f'{DS_DATA_DIR}/data.csv')
    with open(f'{MODEL_DIR}/model.pkl', 'rb') as fd:
        model = joblib.load(fd) 

    cv_strategy = StratifiedKFold(n_splits=5)
    cv_res = cross_validate(
        model,
        data,
        data['target'],
        cv=cv_strategy,
        n_jobs=-1,
        scoring=['f1', 'roc_auc']
        )

    for key, value in cv_res.items():
        cv_res[key] = round(value.mean(), 3) 

    os.makedirs('cv_results', exist_ok=True)
    with open(f'{CV_RESULTS_DIR}/res.json', 'w') as fd:
        json.dump(cv_res, fd)

if __name__ == '__main__':
	evaluate_model()