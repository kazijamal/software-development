from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)

testuser = "krispykreme"
testpass = "12345678"

@app.route("/")
def root():
    if request.args("username") == testuser:
        if request.args("password") == testpass:
            session["username"] = username
    if session["username"] == testuser and session["password"] == testpass:
        redirect(url_for(welcome))
    else:
        redirect(url_for(login))

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
