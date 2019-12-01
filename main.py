from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import LoginForm, SignupForm, PostForm, SearchForm, UpdateAccountForm, CommentForm,NewForumQuestion
from db_setup import conn, curs
from init import app, db
from flask_login import current_user, login_user, logout_user
from db_models import *
from config import Config
import subprocess
from funcs import *

if app.config['TEST_USER_POPULATED_DB'] == True:
    from create_test_users import run

    run()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'app': app,
            'User': User,
            'ForumQuestion': ForumQuestion,
            'ForumPost': ForumPost,
            'Message': Message,
            'UserPost': UserPost,
            'Follow': Follow}


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
            user = signup_handler(form)
            user.authenticated = True
            login_user(user)
            print('signup verified')
            return redirect('/home')
        else:
            print('signup not verified')
            return redirect('/signup')
    return render_template('signup.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    This is a procedure defining the control flow on the home page of the website.
    :return: An HTML response to the client
    """
    form = PostForm()
    if form.validate_on_submit():
        new_post = form.content.data
        add_post(new_post)
        return redirect('/home')
    return render_template('homepage.html', form=form)


@app.route('/forums', methods=['GET', 'POST'])
def forums():
    form = NewForumQuestion()
    lis = "This will be the list that is passed in containing the forums"
    if form.validate_on_submit():
        question = form.question.data
        add_forum(question)
        return redirect('/thread')
    # need to pass in a list of all the forums in the database
    return render_template('forums.html', form=form, list=lis)


@app.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm(grade=current_user.grade, state=current_user.state)
    if form.validate_on_submit():
        update_account_handler(form)
        return redirect('/account')
    return render_template('account.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    searchform = SearchForm(request.form)
    if request.method == 'POST':
        return redirect((url_for('search_results', query=searchform.search.data)))
    return render_template('search.html', form=searchform)


@app.route('/runtests')
def runtests():
    subprocess.Popen(['python3', 'tests.py'])
    return render_template('testpage.html')


# @app.route('/search',methods=['GET', 'POST'])
# def search_results(query):
#     results = []
#     search_string = search.data['search']
#     results1 = Searchable.query.all()
#     return render_template('search', query=query,results=results1)
#     """
#     if search.data['search'] == '':
#         qry = db_session.query(Searchable)
#         results = qry.all()

#     if not results:
#         flash('No results found!')
#         return redirect('/search')
#     if search_string ==
#     else:

#         return render_template('search.html#results', results=results)
#         """


@app.route('/thread')
def thread():
    form = CommentForm()
    question = session['question']
    time = session['time']
    return render_template('thread.html', form=form, q=question, first=current_user.first_name, last=current_user.last_name, time=time)


def add_post(post):
    if post:
        session['post'] = post
        session['time'] = "6:01 PM"
        # Add the post to the database


def add_forum(question):
    if question:
        session['question'] = question
        session['time'] = "4:04 PM"
        # Add the post to the database


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
    return new_user


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


def update_account_handler(form):
    if current_user.first_name != form.first_name.data:
        current_user.first_name = form.first_name.data
    if current_user.last_name != form.last_name.data:
        current_user.last_name = form.last_name.data
    if current_user.email != form.email.data:
        current_user.email = form.email.data
    if current_user.school != form.school.data:
        current_user.school = form.school.data
    if current_user.grade != form.grade.data:
        current_user.grade = form.grade.data
    if current_user.state != form.state.data:
        current_user.state = form.state.data
    if form.new_password.data is not None:
        if current_user.password != form.new_password.data and form.new_password.data == form.new_password_v.data and len(
                form.new_password.data) >= 8:
            current_user.password = form.new_password.data
            flash("Password Changed", category="info")
    flash("Account Details Updated", category="info")
    db.session.commit()
