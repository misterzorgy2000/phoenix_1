import os

MODULE_DIR = f'{os.path.dirname(os.path.abspath(__file__))}'
DS_DATA_DIR = f'{MODULE_DIR}/data'
MODEL_DIR = '/data/ai/models'
MODEL_VERSION_FILE = f'{MODEL_DIR}/version.txt'
CV_RESULTS_DIR = f'{MODEL_DIR}/cv_results'