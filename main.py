from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import LoginForm, SignupForm, PostForm, SearchForm, UpdateAccountForm, CommentForm, ForumQuestionForm
from db_setup import conn, curs
from init import app, db
from flask_login import current_user, login_user, logout_user
from db_models import load_user
from config import Config
import subprocess
from funcs import *

if app.config['TEST_USER_POPULATED_DB'] == True:
    from create_test_users import run
    run()

app.jinja_env.globals.update(grade_level_string = grade_level_string)
app.jinja_env.globals.update(state_abbrev_to_name = state_abbrev_to_name)
app.jinja_env.globals.update(fst = fst)
app.jinja_env.globals.update(clear_all_tables = clear_all_tables)
app.jinja_env.globals.update(is_mentor = is_mentor)
app.jinja_env.globals.update(is_mentee = is_mentee)
app.jinja_env.globals.update(sorted_reverse_id_order = sorted_reverse_id_order)
app.jinja_env.globals.update(get_following = get_following)
app.jinja_env.globals.update(get_mentees = get_mentees)
app.jinja_env.globals.update(get_general_feed = get_general_feed)
app.jinja_env.globals.update(get_user_feed = get_user_feed)
app.jinja_env.globals.update(get_forum_questions = get_forum_questions)
app.jinja_env.globals.update(get_forum_question_posts = get_forum_question_posts)
app.jinja_env.globals.update(get_user_by_username = get_user_by_username)
app.jinja_env.globals.update(date_to_string = date_to_string)
app.jinja_env.globals.update(id_to_forum_question=id_to_forum_question)
app.jinja_env.globals.update(is_following=is_following)

@app.shell_context_processor
def make_shell_context():
    """
    Used to pass critical application variables to a shell context for testing and debugging.
    :return: None
    """
    return {'curs': curs,
            'conn': conn,
            'db': db,
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
    """
    View function for the splash screen. This page is where you either log in or redirect to the sign up page.
    :return: HTML template or redirect
    """
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
    """
    Ends the current user's session and redirects to the splash screen.
    :return: redirect
    """
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
        content = form.content.data
        post = add_user_post(current_user.username, content)
        return redirect('/home')
    return render_template('homepage.html', form=form)


@app.route('/forums', methods=['GET', 'POST'])
def forums():
    """
    View function for the forums screen. This page shows all the forum questions posted in reverse chronological order.
    :return: HTML template or redirect to forum thread
    """
    form = ForumQuestionForm()
    if form.validate_on_submit():
        content = form.question.data
        user = current_user.username
        forumObj = add_forum_question(current_user.username, content)
        if forumObj is not None:
            return redirect('/thread/{}'.format(forumObj.id))
    # need to pass in a list of all the forums in the database
    return render_template('forums.html', form=form)


@app.route('/account', methods=['GET', 'POST'])
def account():
    """
    View function for the account screen. This page is where you can update account information.
    :return: HTML template or redirect
    """
    form = UpdateAccountForm(grade=current_user.grade, state=current_user.state)
    if form.validate_on_submit():
        update_account_handler(form)
        return redirect('/account')
    return render_template('account.html', form=form)


@app.route('/runtests')
def runtests():
    """
    Navigating to this page signals that the test suite has begun running (writing to a file)
    :return: HTML template
    """
    subprocess.Popen(['python3', 'tests.py'])
    return render_template('testpage.html')


@app.route('/search',methods=['GET', 'POST'])
def search():
    """
    View function for the user search page. This page allows a user to search all other users in the system.
    Allows for filtering by mentor/mentee status.
    :return: HTML template
    """
    form = SearchForm(filt='all')
    if form.validate_on_submit():
        pass
    return render_template('search.html', form=form, results=get_search_results(form.filt.data, form.text.data))

@app.route('/follow/<follower_uname>/<following_uname>')
def follow(follower_uname, following_uname):
    """
    This function is invoked when a user clicks the 'Follow' button on the search users page.
    :param follower_uname: username for a User object - the follower of the the 'Follow' transaction
    :param following_uname: username for a User object - the followee of the the 'Follow' transaction
    :return: redirect back to search page
    """
    if is_valid_user(get_user_by_username(follower_uname)) and is_valid_user(get_user_by_username(following_uname)) and follower_uname != following_uname:
        f = Follow(follower_username=follower_uname, following_username=following_uname)
        db.session.add(f)
        db.session.commit()
    return redirect(redirect_url())


@app.route('/thread/<int:question_id>', methods=['GET', 'POST'])
def thread(question_id):
    """
    This view function represents the thread page of a forum question. Here you can post a response to the thread.
    :param question_id: The identifier for the forum question
    :return: redirect or template
    """
    form = CommentForm()
    if form.validate_on_submit():
        content = form.comment.data
        user = current_user.username
        postObj = add_forum_post(question_id, current_user.username, content)
        if postObj is not None:
            return redirect(url_for('thread', question_id=question_id))
        else:
            return redirect('forums')
    return render_template('thread.html', form=form, question_id=question_id)


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
    add_user(new_user)
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
    """
    This method verifies account update information, then writes the changes to the current user object.
    :param form: The form with the posted update data
    :return: void
    """
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

def redirect_url(default='home'):
    """
    This is a helper function to automatically redirect to the last URL
    :param default: The default page to redirect to
    :return: URL string
    """
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)