from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import urllib.request as urlrequest
#import urllib.request as request
import json
import sqlite3, os, random, copy
import utl.dbfunctions as dbfunctions
app = Flask(__name__)

#creates secret key for sessions
app.secret_key = os.urandom(32)

#sets up database
DB_FILE = "rammm.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations
dbfunctions.createTables(c)
#decorator that redirects user to login page if not logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "userID" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def root():
    if "userID" in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/login") #login page
def login():
    if "userID" in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

@app.route("/signup") #signup page
def signup():
    if "userID" in session:
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

#creates a new user in the database if provided valid signup information
@app.route("/register", methods=["POST"])
def register():
    if "userID" in session:
        return redirect(url_for('dashboard'))
    #gets user information from POST request
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    character = request.form['starterSelect']
    c.execute("SELECT username FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a != None:
        flash("Account with that username already exists", "error")
        return redirect(url_for('signup'))
    elif password != password2:
        flash("Passwords do not match", "error")
        return redirect(url_for('signup'))
    elif len(password) < 8:
        flash("Password must be at least 8 characters in length", "error")
        return redirect(url_for('signup'))

    else:
        dbfunctions.createUser(c,username,password,character)
        db.commit()
        flash("Successfuly created user", "success")
        return redirect(url_for('login'))

#authenticates user upon a login attempt
@app.route("/auth", methods=["POST"])
def auth():
    if "userID" in session:
        flash("You were already logged in, "+session['username']+".", "error")
        return redirect(url_for('dashboard'))
    # information inputted into the form by the user
    username = request.form['username']
    password = request.form['password']
    # looking for username & password from database
    c.execute("SELECT userID, password FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a == None: # if username not found
        flash("No user found with given username", "error")
        return redirect(url_for('login'))
    elif password != a[1]: # if password is incorrect
        flash("Incorrect password", "error")
        return redirect(url_for('login'))
    else: # hooray! the username and password are both valid
        session['userID'] = a[0]
        session['username'] = username
        flash("Welcome " + username + ". You have been logged in successfully.", "success")
        return redirect(url_for('dashboard'))

#logs out user by deleting info from the session
@app.route("/logout")
def logout():
    if not "userID" in session:
        flash("Already logged out, no need to log out again", "error")
    else:
        session.pop('userID')
        session.pop('username')
        flash("Successfuly logged out", "success")
    return redirect(url_for('root')) # should redirect back to login page

# DASHBOARD

@app.route("/dashboard")
@login_required
def dashboard():
    user = dbfunctions.getUser(c, str(session['userID']))
    return render_template('dashboard.html', name = user[4], image = user[5], xp = user[6], strength = user[7], intelligence = user[8], luck = user[9], gold = user[10], levelUp = False)

@app.route("/dashboard/levelup")
@login_required
def dashboardLevelUp():
    user = dbfunctions.getUser(c, str(session['userID']))
    return render_template('dashboard.html', name = user[4], image = user[5], xp = user[6], strength = user[7], intelligence = user[8], luck = user[9], gold = user[10], levelUp = True)

# UNLOCK NEW CHARACTER IF LEVELED UP AND NEW LEVEL IS MULTIPLE OF FIVE

@app.route("/levelunlock", methods=["POST"])
@login_required
def levelUnlock():
    userID = session['userID']
    charCount = dbfunctions.getCharCount(c)
    charID = random.randint(1, charCount)
    charName = dbfunctions.getName(c, charID)
    charImg = dbfunctions.getImage(c, charID)
    dbfunctions.addChar(c, userID, charID, charName, charImg)
    dbfunctions.switchChar(c, userID, charID, charName, charImg)
    db.commit()
    return render_template("levelunlock.html", charName = charName, charImg = charImg)

#########################################################
#                  TRIVIA MINIGAME                      #
#########################################################

#shuffles the choices up so that the answers are not always the first choice
def shuffle(q):
    selected_keys = []
    i = 0
    while i < len(q):
        if list(q.keys())[i] not in selected_keys:
            selected_keys.append(list(q.keys())[i])
            i += 1
    return selected_keys

@app.route("/trivia")
def trivia():
    dbfunctions.createTables(c)
    dbfunctions.addQuestions(c)
    original_questions = dbfunctions.questBank(c)
    questions_shuffled = shuffle(original_questions)
    for i in original_questions.keys():
        random.shuffle(original_questions[i])
    return render_template('trivia.html', q = questions_shuffled, o = original_questions)

@app.route('/triviaresults', methods=['POST'])
def triviaresults():
    correct = 0;
    userID = session['userID']
    original_questions = dbfunctions.questBank(c)
    answers = dbfunctions.answerBank(c)
    if request.method == 'POST':
        for i in original_questions.keys():
            answered = request.form[i]
            if original_questions[i][0] == answered:
                correct += 1
        original_question = {}
    else:
        return render_template('triviaresults.html', correct = correct, answers = answers)
    dbfunctions.updateStats(c, userID, intelligence = (correct * 3), xp = (correct * 5), gold = (correct * 2)) # each question correct is +3 to intelligence
    stats = dbfunctions.getStats(c, str(userID))
    currXP = stats['xp']
    leveledUp = dbfunctions.levelUp(currXP-(5 * correct), currXP)
    return render_template('triviaresults.html', correct = correct, answers = answers, intelligence = stats['intelligence'], xp = currXP, leveledUp = leveledUp, gold = (correct * 2))

#########################################################
#                  STRENGTH MINIGAME                    #
#########################################################

randHeroID = 0
@app.route("/strength")
@login_required
def strength():
    user = dbfunctions.getUser(c,str(session['userID']))
    global randHeroID
    #generates a random ID for the superhero API.
    randHeroID = random.randint(1, 731)
    hImage = dbfunctions.getHeroImage(c, randHeroID)
    hName = dbfunctions.getHeroName(c, randHeroID)
    return render_template('strength.html', image = user[5], name = user[4], heroImage = hImage, heroName = hName)

@app.route("/strengthresults", methods = ["POST"])
@login_required
def strengthresults():
    userID = session['userID']
    user = dbfunctions.getUser(c,str(userID))
    global randHeroID
    #generates random rpc numbers for the superheroes
    randRPC = random.randint(1, 3)
    #retrieves rpc number from user
    userRPC = int(request.form['rpc'])
    hImage = dbfunctions.getHeroImage(c, randHeroID)
    hName = dbfunctions.getHeroName(c, randHeroID)
    winner = False
    #if statement compares number equivalents of rock paper scissors: 1 is Rock, 2 is Paper, 3 is Scissors.
    #in the case that you win, gold, as well as more strength and xp, are awarded.
    if (userRPC == 1 and randRPC == 3) or (userRPC == 3 and randRPC == 2) or (userRPC == 2 and randRPC == 1):
        dbfunctions.updateStats(c, userID, strength = 3, xp = 25, gold = 5)
        db.commit()
        winner = True
    #when you tie, less gold, strength, and xp are awarded.
    elif userRPC == randRPC:
        dbfunctions.updateStats(c, userID, strength = 2, xp = 15, gold = 2)
        db.commit()
    #when you lose, you only get small boost in strength and xp.
    else:
        dbfunctions.updateStats(c, userID, strength = 1, xp = 10)
        db.commit()
    #checks to see if user has leveled up.
    stats = dbfunctions.getStats(c, str(userID))
    currXP = stats['xp']
    leveledUp = dbfunctions.levelUp(currXP-15, currXP)
    return render_template('strengthresults.html', image = user[5], name = user[4], strength = stats['strength'], xp = stats['xp'], heroImage = hImage, heroName = hName, userResult = userRPC, heroResult = randRPC, isWinner = winner, leveledUp = leveledUp)

#########################################################
#                  LOTTO MINIGAME                       #
#########################################################

# page to begin the lotto minigame
@app.route("/lotto")
@login_required
def lotto():
    return render_template('lotto.html')

# generates the results of the lotto then displays them on a page
@app.route("/lottoresults")
@login_required
def lottoResults():
    userID = session['userID']
    # checks if the user has enough gold to play
    if dbfunctions.getStats(c, userID)['gold'] < 10:
        flash("You do not have enough gold!")
        return redirect(url_for('dashboard'))
    # takes 10 gold from the user
    dbfunctions.updateStats(c, userID, gold = -10)
    db.commit()
    # generates 3 random numbers between that are either 0 and 1 and 3 random characters
    rand1 = random.randint(0, 1)
    rand2 = random.randint(0, 1)
    rand3 = random.randint(0, 1)
    charCount = dbfunctions.getCharCount(c)
    randCharID1 = random.randint(1, charCount)
    randCharID2 = random.randint(1, charCount)
    randCharID3 = random.randint(1, charCount)
    charName = dbfunctions.getName(c, randCharID1)
    # checks if the random numbers are equal, and displays results for if the user won
    if rand1 == rand2 == rand3:
        return render_template('lottoresults.html', charID = randCharID1, charName = charName, img1 = dbfunctions.getImage(c, randCharID1), img2 = dbfunctions.getImage(c, randCharID1), img3 = dbfunctions.getImage(c, randCharID1), isWinner = True)
    # displays results for if the user lost
    else:
        return render_template('lottoresults.html', img1 = dbfunctions.getImage(c, randCharID1), img2 = dbfunctions.getImage(c, randCharID2), img3 = dbfunctions.getImage(c, randCharID3), isWinner = False)

# switches a users character after the lotto, if chosen
@app.route("/lottoswitch", methods=["POST"])
@login_required
def lottoSwitch():
    userID = session['userID']
    charID = request.form['charID']
    charName = request.form['charName']
    charImg = request.form['charImg']
    # adds new character, switches current character, and updates stats of user
    dbfunctions.addChar(c, userID, charID, charName, charImg)
    dbfunctions.switchChar(c, userID, charID, charName, charImg)
    dbfunctions.updateStats(c, userID, luck = 5, xp = 50)
    db.commit()
    # checks if the user leveled up to display level up alert on the dashboard
    stats = dbfunctions.getStats(c, userID)
    currXP = stats['xp']
    leveledUp = dbfunctions.levelUp(currXP-50, currXP)
    return render_template("lottoswitch.html", charName = charName, charImg = charImg, luck = stats['luck'], xp = currXP, leveledUp = leveledUp)

# gives a user gold after the lotto, if chosen
@app.route("/lottogold", methods=["POST"])
@login_required
def lottoGold():
    userID = session['userID']
    # updates stat of user
    dbfunctions.updateStats(c, userID, gold = 50, luck = 5, xp = 50)
    db.commit()
    # checks if the user leveled up to display level up alert on the dashboard
    stats = dbfunctions.getStats(c, userID)
    currXP = stats['xp']
    leveledUp = dbfunctions.levelUp(currXP-50, currXP)
    return render_template("lottogold.html", gold = stats['gold'], luck = stats['luck'], xp = currXP, leveledUp = leveledUp)

#########################################################
#                      COLLECTION                       #
#########################################################
@app.route("/collection")
@login_required
def collection():
    return render_template('collection.html', characters = dbfunctions.getCharacters(c,session['userID']))

# switches a users character
@app.route("/switchcharacter", methods=["POST"])
@login_required
def characterSwitch():
    userID = session['userID']
    charID = request.form['charID']
    charName = request.form['charName']
    charImg = request.form['charImg']
    # switches current character
    dbfunctions.switchChar(c, userID, charID, charName, charImg)
    dbfunctions.resetStats(c,userID)

    db.commit()
    flash("Your character is now " + charName, "success")
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.debug = True
    app.run()

db.commit()
db.close()
