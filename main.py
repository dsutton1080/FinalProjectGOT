from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
@app.route("splashScreen")
def home():
    return "<h1>At Splash Screen</h1>"

@app.route("/home")
def home():
    return "<h1>At Home Page</h1>"

@app.route("/login")
def login():
    return "<h1>At Login Page</h1>"

@app.route("/signup")
def signup():
    return "<h1>At Signup Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)
