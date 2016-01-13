from flask import Flask

from models import db


def create_app(config=None, environment=None):
    app = Flask(__name__)

    # TODO: Get this from a config file
    app.config["MONGODB_SETTINGS"] = {'DB': "eatdb"}
    app.config["SECRET_KEY"] = "KeepThisS3cr3t"
    db.init_app(app)

    # TODO: add routes

    return app
