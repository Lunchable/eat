from flask import render_template, redirect
import auth
import api
import formdemo


def register_routes(app):
    @app.route('/')
    def root():
        return redirect('/application',code=301)

    auth.register_routes(app)
    api.register_routes(app)
    formdemo.register_routes(app)
