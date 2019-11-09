from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm
from db_setup import conn, curs
from init import app, db
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
    form = LoginForm()
    if form.validate_on_submit():
        if login(form):
            return redirect('/home')
        else:
            return redirect('/splash')
    return render_template('splash.html', form=form)


def login(form):
    username = form.username.data
    password = form.password.data
    if username == 'kuedu' and password == 'jayhawks':
        return True
    return False


@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
    return render_template('homepage.html')


def signup_handler(form):
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
    if form.first_name.data and form.last_name.data and form.username.data:
        if form.password.data and form.password_v.data and form.email.data:
            if form.state.data and form.grade.data and form.school.data:
                if form.password.data == form.password_v.data:
                    return True
    return False

