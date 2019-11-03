from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/splash')
def splash():
    return render_template('splash.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')
