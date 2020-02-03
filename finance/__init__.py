import flask

app = flask.Flask(__name__)

from finance import routes
