from flask import render_template
import signin


def register_routes(app):
    @app.route('/')
    def root():
        return render_template('index.html')

    signin.register_routes(app)
