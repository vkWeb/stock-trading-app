import flask
import flask_sqlalchemy
import flask_migrate

import config

app = flask.Flask(__name__)

app.config.from_object(config.Config)

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from finance import routes
