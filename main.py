from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm
from db_setup import conn, curs
from init import app, db
from flask_login import current_user, login_user, logout_user
from db_models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'User': User, 
            'ForumQuestion': ForumQuestion,
            'ForumPost' : ForumPost,
            'Message' : Message,
            'UserPost' : UserPost,
            'Follow' : Follow }

@app.route('/')
@app.route('/splash', methods=['GET', 'POST'])
def splash():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.test_password(form.password.data):
            flash('Username or Password is incorrect')
            return redirect(url_for('splash'))
        user.authenticated = True
        login_user(user)
        return redirect(url_for('home'))
    return render_template('splash.html', form=form)

@app.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('splash'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This is a procedure defining the control flow on the Sign in page of the website.
    A form can be submitted for backend validation and processing.
    :return: An HTML response to the client with the HTML template parameters filled in
    """
    form = SignupForm()
    if form.validate_on_submit():
        if signup_not_empty(form):
            signup_handler(form)
            print('signup verified')
            return redirect('/home')
        else:
            print('signup not verified')
            return redirect('/signup')
    return render_template('signup.html', form=form)


@app.route('/home')
def home():
    """
    This is a procedure defining the control flow on the home page of the website.
    :return: An HTML response to the client
    """
    return render_template('homepage.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    form = SignupForm()
    return render_template('account.html', form=form)


def signup_handler(form):
    """
    Processes the POST request of a sign up form and adds a user to the database
    :param form: a FlaskForm object containing the inputted fields
    :return: Void
    """
    f_name = form.first_name.data
    l_name = form.last_name.data
    username = form.username.data
    password = form.password.data
    password_v = form.password_v.data
    email = form.email.data
    state = form.state.data
    grade = form.grade.data
    school = form.school.data
    new_user = User (first_name = f_name, last_name = l_name,
                     username = username, password = password,
                     email = email, state = state, grade = grade,
                     school = school)
    db.session.add(new_user)
    db.session.commit()

def signup_not_empty(form):
    """
    Determines whether a field in the submitted sign up form is empty.
    :param form: a FlaskForm object containing the inputted fields
    :return: boolean indicating True if valid, False otherwise
    """
    if form.first_name.data and form.last_name.data and form.username.data:
        if form.password.data and form.password_v.data and form.email.data:
            if form.state.data and form.grade.data and form.school.data:
                if form.password.data == form.password_v.data:
                    return True
    return False

