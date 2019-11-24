from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm
from db_setup import conn, curs
from init import app, db, login
from db_models import *

@login.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

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

def is_distinct_username(uname):
    user = User.query.get(username=uname).first()
    return (user is None)
