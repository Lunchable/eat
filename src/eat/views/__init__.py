from flask import render_template
import auth
import api


def register_routes(app):
    @app.route('/')
    def root():
        return render_template('index.html')

    auth.register_routes(app)
    api.register_routes(app)
