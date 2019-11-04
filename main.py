from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, SignupForm

from init import app


@app.route('/')
@app.route('/splash', methods=['GET', 'POST'])
def splash():
    form = LoginForm()
    return render_template('splash.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)


@app.route('/home')
def home():
    return render_template('homepage.html')
