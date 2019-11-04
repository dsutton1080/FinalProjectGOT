from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/')
@app.route('/splash')
def splash():
    render_template('splash.html')
    username = request.form['username']
    password = request.form['password']
    login_form(username, password)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('homepage.html')


def login_form(user, password):
    # Check if username and password are in database NEED TO ADD THIS LOGIC
    return render_template('homepage.html')


def signup_form():
    return 1;