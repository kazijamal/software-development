from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import os

app = Flask(__name__)

# creates secret key for session
app.secret_key = os.urandom(32)

# hardcodes a single username/password combination
testuser = "krispykreme"
testpass = "12345678"

# redirects to login page if no user logged in
# redirects to welcome page if user logged in
@app.route("/")
def root():
    if "username" in session:
        return redirect(url_for('welcome'))
    return redirect(url_for('login'))

# has logout button to log out
@app.route("/welcome")
def welcome():
    if "username" not in session:
        return redirect(url_for('root'))
    return render_template("welcome.html")

# login page with form which sends request to /auth route
@app.route("/login")
def login():
    return render_template("login.html")

# handles login request and redirects to welcome after adding username to session or returns an error
@app.route("/auth", methods=["POST"])
def auth():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.form ***")
    print(request.form)
    print("\n\n\n")
    if request.form['username'] == testuser:
        if request.form['password'] == testpass:
            session['username'] = request.form['username']
            return redirect(url_for('welcome'))
        else:
            print("invalid password")
            return error("Invalid Password")
            # return redirect(url_for('login'))
    else:
        print("invalid username")
        return error("Invalid Username")
        # return redirect(url_for('login'))

# returns a page with provided error message
def error(message):
    return render_template("error.html", error=message)

# removes session data for username
@app.route("/logout")
def logout():
    session.pop('username')
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.debug = True
    app.run()
