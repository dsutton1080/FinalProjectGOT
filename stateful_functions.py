from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm
from db_setup import conn, curs
from init import app, db, login
from db_models import *
from flask_login import current_user, login_user
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
    if grade[:3] == "col":
        user_type = "Mentor"
    else:
        user_type = "Mentee"
    school = form.school.data
    new_user = User (first_name=f_name, last_name=l_name,
                     username=username, password=password,
                     email=email, state=state, grade=grade,
                     user_type=user_type, school=school)
    db.session.add(new_user)
    db.session.commit()
    new_user.authenticated = True
    login_user(new_user)


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
    if form.grade.data[:3] == "col":
        current_user.user_type = "Mentor"
    else:
        current_user.user_type = "Mentee"
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