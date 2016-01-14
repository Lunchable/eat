from flask import render_template


def register_routes(app):
    @app.route('/')
    def root():
        return render_template('index.html')
