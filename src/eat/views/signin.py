from flask import redirect
from flask import render_template
from flask_login import current_user, login_user, logout_user

from eat.forms.auth import SignIn


def register_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        if current_user.is_authenticated:
            return redirect('/')
        form = SignIn()
        if form.validate_on_submit():
            login_user(form.get_user())
            return redirect('/')
        return render_template('signin.html', signin_form=form)


    @app.route('/logout')
    @app.route('/signout')
    def logout():
        if current_user:
            logout_user()
        return redirect('/')
