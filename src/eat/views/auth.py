from flask import redirect
from flask import render_template
from flask_login import current_user, login_user, logout_user

from eat.forms.auth import SignIn, SignUp
from eat.models.user import User


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


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect('/')
        form = SignUp()
        if form.validate_on_submit():
            user = User(email=form.email.data)
            user.password = form.password.data
            user.save()
            login_user(user)
            return redirect('/')
        return render_template('signup.html', signup_form=form)
    
    @app.route('/snap_tanf_dfpir', methods=['GET', 'POST'])
    def snap_tanf_dfpir(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('snap_tanf_dfpir.html')

    @app.route('/child_new', methods=['GET', 'POST'])
    def child_new(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('child_new.html')

    @app.route('/ssn', methods=['GET', 'POST'])
    def ssn(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('ssn.html')

    @app.route('/child_Income', methods=['GET', 'POST'])
    def child_Income(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('child_Income.html')

    @app.route('/enterAnotherChild', methods=['GET', 'POST'])
    def enterAnotherChild(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('enterAnotherChild.html')

    @app.route('/self_income_types', methods=['GET', 'POST'])
    def self_income_types(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('self_income_types.html')    

    @app.route('/enterChildInfo', methods=['GET', 'POST'])
    def enterChildInfo(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('enterChildInfo.html')

    @app.route('/self_income', methods=['GET', 'POST'])
    def self_income(): 
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('self_income.html')
    

    # foster parent redirect
    @app.route('/foster', methods=['GET', 'POST'])
    def foster():
        return render_template('foster.html')

    # nav-menu
    @app.route('/faq', methods=['GET', 'POST'])
    def faq():
        return render_template('faq.html')
    
    @app.route('/languages', methods=['GET', 'POST'])
    def languages():
        return render_template('languages.html')

    @app.route('/reset', methods=['GET', 'POST'])
    def reset():
        return render_template('reset.html')

    # footer
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        return render_template('contact.html')

    @app.route('/Terms', methods=['GET', 'POST'])
    def terms():
        return render_template('terms.html')


    # form
    @app.route('/self', methods=['GET', 'POST'])
    def self():
        return render_template('self.html')

    @app.route('/income', methods=['GET', 'POST'])
    def income():
        return render_template('income.html')

    @app.route('/logout')
    @app.route('/signout')
    def logout():
        if current_user:
            logout_user()
        return redirect('/')

    @app.route('/foobar')
    def foobar():
        return render_template()