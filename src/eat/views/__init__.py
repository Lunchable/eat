from flask import render_template
import auth


def register_routes(app):
    @app.route('/')
    def root():
        return render_template('index.html')

    auth.register_routes(app)
