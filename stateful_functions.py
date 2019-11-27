from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm
from db_setup import conn, curs
from init import app, db, login
from db_models import *
from flask_login import current_user
from sqlalchemy import desc

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
        if current_user.password != form.new_password.data and form.new_password.data == form.new_password_v.data and len(form.new_password.data) >= 8:
            current_user.password = form.new_password.data
            flash("Password Changed", category="info")
    flash("Account Details Updated", category="info")
    db.session.commit()

def is_distinct_username(uname):
    user = User.query.get(username=uname).first()
    return (user is None)

def get_messages(sender_username, receiver_username):
    return list(db.session.query(Message).filter_by(sender_username=sender_username).filter_by(receiver_username=receiver_username).order_by(desc(Message.id)))