from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os

app = Flask(__name__)

#creates secret key for sessions
app.secret_key = os.urandom(32)

#sets up database
DB_FILE = "odyssey.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations

@app.route("/")
def root():
    if "userID" in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route("/login") #login page
def login():
    if "userID" in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route("/signup") #signup page
def signup():
    if "userID" in session:
        return redirect(url_for('home'))
    return render_template('signup.html')

#creates a new user in the database if provided valid signup information
@app.route("/register", methods=["POST"])
def register():
    #gets user information from POST request
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    c.execute("SELECT username FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a != None:
        flash("Account with that username already exists")
        return redirect(url_for('signup'))
    elif password != password2:
        flash("Passwords do not match")
        return redirect(url_for('signup'))
    elif len(password) < 8:
        flash("Password must be at least 8 characters in length")
        return redirect(url_for('signup'))

    else:
        c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
        db.commit()
        flash("Successfuly created user")
        return redirect(url_for('login'))

#authenticates user upon a login attempt
@app.route("/auth", methods=["POST"])
def auth():
    # information inputted into the form by the user
    username = request.form['username']
    password = request.form['password']
    # looking for username & password from database
    c.execute("SELECT userID, password FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a == None: # if username not found
        flash("No user found with given username")
        return redirect(url_for('login'))
    elif password != a[1]: # if password is incorrect
        flash("Incorrect password")
        return redirect(url_for('login'))
    else: # hooray! the username and password are both valid
        session['userID'] = a[0]
        session['username'] = username
        flash("Welcome " + username + ". You have been logged in successfully.")
        return redirect(url_for('home'))

#logs out user by deleting info from the session
@app.route("/logout")
def logout():
    session.pop('userID')
    session.pop('username')
    return redirect(url_for('root')) # should redirect back to login page

@app.route("/dashboard")
def dashboard():
    if "userID" in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.debug = True
    app.run()

db.commit()
db.close()
