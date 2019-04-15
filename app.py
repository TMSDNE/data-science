import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    data = { 'text': 'Hello World' }
    return flask.jsonify(data) 
