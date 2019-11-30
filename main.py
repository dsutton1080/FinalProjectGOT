from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm, UpdateAccountForm, PostForm
from db_setup import conn, curs
from init import app, db
from flask_login import current_user, login_user, logout_user
from db_models import *
from stateful_functions import *
from flask_login import current_user, login_user, logout_user, login_required


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'ForumQuestion': ForumQuestion,
            'ForumPost': ForumPost,
            'Message': Message,
            'UserPost': UserPost,
            'Follow': Follow}

@app.route('/', methods=['GET', 'POST'])
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
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('splash.html', form=form)

@app.route('/logout')
@login_required
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
            return redirect('/home')
        else:
            return redirect('/signup')
    return render_template('signup.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    """
    This is a procedure defining the control flow on the home page of the website.
    :return: An HTML response to the client
    """
    form = PostForm()
    if form.validate_on_submit():
        usr = current_user
        new_post = form.content
        add_post(usr, new_post)
    return render_template('homepage.html', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(grade=current_user.grade, state=current_user.state)
    if form.validate_on_submit():
        update_account_handler(form)
        return redirect('/account')
    return render_template('account.html', form=form)


def add_post(user, post):
    if user and post:
        # Add the post to the database
        # Then take them to the new post page
        return redirect(url_for('home'))


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
    new_user = User(first_name=f_name, last_name=l_name,
                    username=username, password=password,
                    email=email, state=state, grade=grade,
                    school=school)
    db.session.add(new_user)
    db.session.commit()

@app.route('/testsuite', methods=['GET', 'POST'])
@login_required
def testsuite():
    pass

@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    form = UpdateAccountForm(grade=current_user.grade, state=current_user.state)
    if form.validate_on_submit():
        update_account_handler(form)
        return redirect('/friends')
    return render_template('friends.html', form=form)

# @app.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():
#     pass

# @app.route('/forums', methods=['GET', 'POST'])
# @login_required
# def forums():
#     pass

# @app.route('/messages', methods=['GET', 'POST'])
# @login_required
# def messages():
#     pass


