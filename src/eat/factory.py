from flask import Flask
from flask_login import LoginManager
from models.session import MongoSessionInterface


def create_app(config=None, environment=None):
    app = Flask(__name__)

    # TODO: Get this from a config file
    app.config["MONGODB_SETTINGS"] = {'DB': "eatdb"}
    app.config[
        "SECRET_KEY"] = "\x1a\xb1\x9d\x1d\xf2\x01\xa1X\xb8g\xed\x1c\xb3\x0f+s\xbce\xf6\x92\x83'\xf2\xbc\x96\xc6\x18\x03`\xc0\x0c("
    app.config["IV"] = '\xe7\x9d\xc7\xbd\x12l\x88\xc7\xe9D\x93!\xa2B\xed\x91'
    app.session_interface = MongoSessionInterface(db=app.config["MONGODB_SETTINGS"]['DB'])

    with app.app_context():
        from models import db
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

        from views import register_routes as register_views

        register_views(app)

    return app
