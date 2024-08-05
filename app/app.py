#

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

@app.route('/v1/fit')
def fit():
    return 'fitted'

if __name__ == '__main__':
    app.run(port=5678, debug=True)