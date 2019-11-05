from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm

from init import app, db
from models import User


@app.route('/')
@app.route('/splash', methods=['GET', 'POST'])
def splash():
    """
    This is a procedure defining the control flow on the splash (default) page of the website.
    A form can be submitted for backend validation and processing.
    :return: An HTML response to the client with the HTML template parameters filled in
    """
    form = LoginForm()
    if form.validate_on_submit():
        if login(form):
            return redirect('/home')
        else:
            return redirect('/splash')
    return render_template('splash.html', form=form)


def login(form):
    """
    This function matches inputted Login data with backend
    :param form: A FlaskForm object containing a set of inputted fields
    :return: boolean indicating whether the login was successful
    """
    username = form.username.data
    password = form.password.data
    if username == 'kuedu' and password == 'jayhawks':
        return True
    return False


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

