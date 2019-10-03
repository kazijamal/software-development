# Team Krispy Kreme - Kenneth Chin and Kazi Jamal
# SoftDev1 pd9
# K16 -- Oh yes, perhaps I do...
# 2019-10-04

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
import os

app = Flask(__name__)

# creates secret key for session
app.secret_key = os.urandom(32)

# hardcodes a single username/password combination
testuser = "krispykreme"
testpass = "12345678"

@app.route("/")
def root():
    # redirects to welcome page if user logged in
    if "username" in session:
        return redirect(url_for('welcome'))
    # redirects to login page if no user logged in
    return redirect(url_for('login'))

# has log out button to log out
@app.route("/welcome")
def welcome():
    if "username" not in session:
        return redirect(url_for('root'))
    return render_template("welcome.html")

# login page with form which sends request to /auth route
@app.route("/login")
def login():
    return render_template("login.html")

# handles login request
@app.route("/auth", methods=["POST"])
def auth():
    '''
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.form ***")
    print(request.form)
    print("\n\n\n")
    '''
    user = request.form['username']
    if user == testuser:
        # if correct username/password combination, add username to session and redirect to welcome route
        if request.form['password'] == testpass:
            session['username'] = user
            flash("Welcome " + user + ". You are logged in.")
            return redirect(url_for('welcome'))
        # if invalid password flash error and redirect to login route
        else:
            flash("invalid password")
            return redirect(url_for('login'))
    # if invalid username flash error and redirect to login route
    else:
        flash("invalid username")
        return redirect(url_for('login'))

# removes session data for username
@app.route("/logout")
def logout():
    # print("***DIAG: session ***")
    # print(session)
    session.pop('username')
    # print("***DIAG: session ***")
    # print(session)
    return redirect(url_for('root'))


if __name__ == "__main__":
    app.debug = True
    app.run()
