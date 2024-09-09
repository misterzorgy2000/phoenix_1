from flask import Flask
from cow.conf import CONF
from cow.ai.service import AIService as Phoenix

app = Flask(__name__)

prefix = '/v1'

@app.route('/')
def info():
    return 'info'

@app.route(f'{prefix}/fit')
def fit():
    return 'fit'


@app.route(f'{prefix}/monitor')
def monitor():
    return 'monitor'


@app.route(f'{prefix}/predict')
def predict():
    return 'predict'


@app.route(f'{prefix}/version')
def version():
    return Phoenix.get_latest_version()

def run():
    app.run(port=CONF.api.port, debug=True)
    