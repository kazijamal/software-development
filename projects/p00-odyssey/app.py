from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from utl import dbfunctions, dbeditfunctions, dbcreatefunctions

app = Flask(__name__)

#creates secret key for sessions
app.secret_key = os.urandom(32)

#sets up database
DB_FILE = "odyssey.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations
dbfunctions.createTables(c)

#checks if user is authenticated
def checkAuth():
    if "userID" in session:
        return True
    else:
        return False

@app.route("/")
def root():
    if checkAuth(): #if you've already logged in
        return redirect(url_for('home'))
    else: #if not, redirect to login page
        return redirect(url_for('login'))

@app.route("/login") #login page
def login():
    if checkAuth():
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route("/signup") #signup page
def signup():
    if checkAuth():
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

@app.route("/home")
def home():
    if checkAuth(): # if logged in
        storiesEdited = dbeditfunctions.getStoriesEdited(c,session['userID'])
        return render_template('home.html', storiesEdited=storiesEdited)
    else:
        return redirect(url_for('login'))

#does a search through stories given a keyword from their namesy
@app.route("/search")
def search():
    if checkAuth():
        #gets information from GET request
        query = request.args['query']
        response = dbfunctions.getSearch(c, query)
        #checks if stories have been edited by current user
        storiesEdited = dbeditfunctions.getStoriesEdited(c,session['userID'])
        ids = []
        for story in storiesEdited:
            ids.append(story[0])
        stories = []
        for story in response:
            if story[0] in ids:
                stories.append(story + ("edited",))
            else:
                stories.append(story + ("unedited",))
        #returns search results with either /story or /edit links depending on whether the current user has edited the story
        return render_template('search.html', query=query, stories=stories)
    else:
        return redirect(url_for('login'))

#route for reading a story with a given storyID
@app.route("/story/<storyID>")
def readStory(storyID):
    if checkAuth():
        # if no stories have been created or this story number is too high (not created)
        if dbfunctions.getMaxStoryID(c) == None or int(storyID) < 1 or int(storyID) > dbfunctions.getMaxStoryID(c):
            flash("Invalid story ID")
            return redirect(url_for('home'))
        else:
            if(not dbeditfunctions.hasEdited(c,session['userID'],storyID)):
                flash("You have not edited this story yet")
                return redirect(url_for('home'))
            title = dbfunctions.selectStory(c, storyID)[0]
            edits = dbeditfunctions.getStoryEdits(c, storyID)
            return render_template('story.html', title=title, edits=edits)
    else:
        return redirect(url_for('login'))

#page displaying stories user has not edited yet
@app.route("/uneditedstories", methods=["POST","GET"])
def uneditedStories():
    if checkAuth():
        list = dbeditfunctions.getStoriesNotEdited(c, session['userID'])
        return render_template('uneditedstories.html', storiesNotEdited=list)
    else:
        return redirect(url_for('login'))

#route for editing a story with a given storyID
@app.route("/edit/<storyID>")
def editStory(storyID):
    if checkAuth():
        # if no stories have been created or this story# is too high (not created)
        if dbfunctions.getMaxStoryID(c) == None or int(storyID) < 1 or int(storyID) > dbfunctions.getMaxStoryID(c):
            flash("Invalid story ID")
            return redirect(url_for('home'))
        else:
            # if the user has already edited this story, redirect to home.
            if(dbeditfunctions.hasEdited(c,session['userID'],storyID)):
                flash("Already edited story")
                return redirect(url_for('home'))
            title = dbfunctions.selectStory(c, storyID)[0]
            edit = dbeditfunctions.getLatestStoryEdit(c, storyID)
            return render_template('edit.html', title=title, edit=edit,storyID = storyID)
    else:
        return redirect(url_for('login'))

#adds a contribution to the story if provided valid edit information
@app.route("/auth_edit", methods=["POST"])
def authEdit():
    #gets edit information from POST request
    content = request.form['content']
    storyID = request.form['storyID']
    userID = session['userID']
    username = session['username']
    # if the user has already edited this story, redirect to home.
    # This statement is required to prevent a loophole where a user can create a story
    # on one tab(tab1), sign out, sign back in as another user(set sessions' userID to an ID that's not equal to the author's)
    # this allows the author go to the edit page for the newly created story, and type in their new content.
    # on another tab(tab2), the new user can sign out, and sign back in as the original author (set session's userID to original author's ID)
    # and then on tab1 the person can press submit, which would set this edit as the original author.
    if(dbeditfunctions.hasEdited(c,session['userID'],storyID)):
        flash("Already edited story")
        return redirect(url_for('home'))
    #adds edit to story to the database
    dbeditfunctions.addToStory(c, storyID, userID, username, content)
    db.commit()
    flash("You have contributed to the story successfully.")
    return redirect('/story/'+storyID)

#page for creating a new story
@app.route("/createstory")
def createStory():
    if checkAuth():
        return render_template('createstory.html')
    else:
        return redirect(url_for('login'))

#adds a new story to the database if provided valid new story information 
@app.route("/newstory", methods=['POST'])
def newStory():
    #gets story information from POST request
    title = request.form['title']
    content = request.form['content']
    userID = int(session['userID'])
    username = session['username']
    #determines what storyID to give the new story
    if dbfunctions.getMaxStoryID(c) == None:
        storyID = 1
    else:
        storyID = dbfunctions.getMaxStoryID(c) + 1
    #adds new story to the database
    dbcreatefunctions.createStory(c, storyID, title, userID, username, content)
    db.commit()
    return redirect('/story/{}'.format(storyID))

if __name__ == "__main__":
    app.debug = True
    app.run()

db.commit()
db.close()

#   ____      _
#  / __ \    | |
# | |  | | __| |_   _ ___ ___  ___ _   _
# | |  | |/ _` | | | / __/ __|/ _ \ | | |
# | |__| | (_| | |_| \__ \__ \  __/ |_| |
#  \____/ \__,_|\__, |___/___/\___|\__, |
#                __/ |              __/ |
#               |___/              |___/
#  _             _
# | |           | |
# | |__  _   _  | |_ ___  __ _ _ __ ___
# | '_ \| | | | | __/ _ \/ _` | '_ ` _ \
# | |_) | |_| | | ||  __/ (_| | | | | | |
# |_.__/ \__, |  \__\___|\__,_|_| |_| |_|
#         __/ |
#        |___/
#  _                    _        _____ _
# | |                  | |      / ____| |
# | |__   ___ _ __   __| |_   _| (___ | |_ _ __ __ ___      _____
# | '_ \ / _ \ '_ \ / _` | | | |\___ \| __| '__/ _` \ \ /\ / / __|
# | |_) |  __/ | | | (_| | |_| |____) | |_| | | (_| |\ V  V /\__ \
# |_.__/ \___|_| |_|\__,_|\__, |_____/ \__|_|  \__,_| \_/\_/ |___/
#                          __/ |
#                         |___/
