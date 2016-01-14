from flask import Flask
from flask_login import LoginManager

from models import db
from views import register_routes as register_views


def create_app(config=None, environment=None):
    app = Flask(__name__)

    # TODO: Get this from a config file
    app.config["MONGODB_SETTINGS"] = {'DB': "eatdb"}
    app.config["SECRET_KEY"] = "KeepThisS3cr3t"
    db.init_app(app)

    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(id):
        if id in (None, 'None'):
            return None
        try:
            from models.user import User
            return User.objects(id=id).first()
        except:
            return None

    login_manager.init_app(app)

    register_views(app)

    return app
