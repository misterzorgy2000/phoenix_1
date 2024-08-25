import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor
from cow.messaging import get_notifier, get_transport
from oslo_config import cfg

from cow.ai import DS_DATA_DIR, MODEL_DIR

NOTICE_MODEL_CREATED = {
    'created_at': '2012-05-08 20:23:41',
    'version': '1.0.2'
}

def fit_model():
    data = pd.read_csv(f'{DS_DATA_DIR}/data.csv')
    # обучение модели
    # cat_features = data.select_dtypes(include='object')
    # potential_binary_features = cat_features.nunique() == 2

    # binary_cat_features = cat_features[potential_binary_features[potential_binary_features].index]
    # other_cat_features = cat_features[potential_binary_features[~potential_binary_features].index]
    # num_features = data.select_dtypes(['float'])

    # preprocessor = ColumnTransformer(
    #     [
    #     ('binary', OneHotEncoder(drop=params['one_hot_drop']), binary_cat_features.columns.tolist()),
    #     ('cat', CatBoostEncoder(return_df=False), other_cat_features.columns.tolist()),
    #     ('num', StandardScaler(), num_features.columns.tolist())
    #     ],
    #     remainder='drop',
    #     verbose_feature_names_out=False
    # )
    
    X = data.drop(columns=['resource_id', 'ts', 'node_disk_read_bytes_total_y'], axis=1)
    y = data['node_disk_read_bytes_total_y']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = CatBoostRegressor()
    # pipeline = Pipeline(
    #     [
    #         ('preprocessor', preprocessor),
    #         ('model', model)
    #     ]
    # )
    model.fit(X_train, y_train)

    os.makedirs('models', exist_ok=True)
    with open(f'{MODEL_DIR}/model.pkl', 'wb') as fd:
        joblib.dump(model, fd)
        
        notifier = get_notifier(get_transport(cfg.CONF),
                                          'compute.vagrant-precise')
        notifier.info({}, 'ai.model.create',
                       NOTICE_MODEL_CREATED)

if __name__ == '__main__':
    fit_model()