from flask import redirect
from flask import render_template
from flask_login import current_user, login_user, logout_user


def register_routes(app):
    @app.route('/svc/eat/v1/name', methods=['GET', 'POST'])
    def api_name():
        return redirect('/')
