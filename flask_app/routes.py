from flask import Flask, render_template, redirect, url_for, flash
from flask_app import app, db
from flask_app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from flask_app.models import User
from flask_app.forms import RegistrationForm

@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/prompts')
# @login_required
def prompts():
    return render_template('prompts.html', title='Question Prompts')

@app.route('/prompts/strangers')
# @login_required
def strangers():
    return render_template('prompts_strangers.html', title='Question Prompts - Stranger')

@app.route('/prompts/acquaintances')
# @login_required
def acquaintances():
    return render_template('prompts_acquaintances.html', title='Question Prompts - Acquaintances')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)