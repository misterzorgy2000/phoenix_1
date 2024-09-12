from flask import Flask, request, jsonify
import json
import pandas as pd

from phoenix.ai import CV_RESULTS_DIR, MODEL_VERSION_FILE
from phoenix.conf import CONF
from phoenix.ai.service import PhoenixAI

app = Flask(__name__)

prefix = '/v1'

class PhoenixAPI():
    def __init__(self, service):
        self.service = service
    
@app.route('/')
def info():
    return {
        "version": version()
    }
    
@app.route(f'{prefix}/fit')
def fit():
    try:
        PhoenixAI.instance.fit_save()
    except Exception:
        raise "Fit failed"
    
    return f'Fitted: new version: {version()}'


@app.route(f'{prefix}/monitor')
def monitor():
    PhoenixAI.instance.evaluate()

    stat = {}
    
    with open(f'{CV_RESULTS_DIR}/res.json', 'r') as file:
        stat = json.load(file) 

    return stat


@app.route(f'{prefix}/predict', methods=['GET'])
def predict():
    model = PhoenixAI.get_model_version(version())

    data = request.json

    try:
        return model.predict(data).tolist()
    except Exception:
        print(data)
        
        raise(f'Prediction failed. Cause: {Exception}')

@app.route(f'{prefix}/version')
def version():
    return PhoenixAI.get_latest_version()

def run():
    app.run(port=CONF.api.port, debug=True)
    