from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utl import models, comments, posts
from utl import api
from utl import communities as communitiesfunctions
from utl import friends as friendsfunctions
from utl import messages as messagesfunctions
from utl import users as usersfunctions
from utl import posts as postsfunctions
from utl import comments as commentsfunctions
from utl import feed as feedfunctions
import os
#most of these imports are from our own other files, the only new one is SQLAlchemy

db = models.db
app = Flask(__name__)
app.config.from_object(Config)
#creates secret key for sessions
app.secret_key = os.urandom(32)

#decorator that redirects user to login page if not logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "userID" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#home directoyy, forces you to log in if you didn't
@app.route("/")
def root():
    if "userID" in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

#our secret easteregg
@app.route("/snake")
@login_required
def snake():
    return render_template("snake.html")

#first page you see at login
@app.route("/dashboard")
@login_required
def dashboard():
    #shows the news and weather, pulls from the api lists
    news = api.getNewsArticles()
    if news == "Invalid API Key":
        return render_template("error.html", error=news)
    return render_template("dashboard.html",
        user=session['firstName'],
        today=api.getTodayWeather(),
        tomorrow=api.getTomorrowWeather(),
        news=news,
        xkcd=api.xkcd())

#feed page as shown on the top of the webbrowser
@app.route("/feed")
@login_required
def feed():
    communitypost_data = feedfunctions.getCommunityPosts(session['userID'])
    communityposts = {}
    #just gets recent posts from communities you are in
    for post in communitypost_data:
        communityposts[post] = []
        communityposts[post].append(postsfunctions.getCreator(post.postID))
        communityposts[post].append(communitiesfunctions.getCommunity(post.communityID))
    timelinepost_data = feedfunctions.getTimelinePosts(session['userID'])
    timelineposts = {}
    #this is the oredering of the community posts and showing which community its in
    for post in timelinepost_data:
        timelineposts[post] = postsfunctions.getCreator(post.postID)
    return render_template("feed.html", communityposts=communityposts, timelineposts=timelineposts)

@app.route("/friends")
#requesting freinds page
@login_required
def friends():
    userID = session['userID']
    friendslist = friendsfunctions.getFriends(userID)
    users = []
    #adding all the freinds in the database to the webpage
    for friend in friendslist:
        users.append(usersfunctions.getUser(friend.friendID))
    reqs = friendsfunctions.getFriendRequests(userID)
    friendrequests = {}
    #if requested or if you request update the page to shothat
    for req in reqs:
        friendrequests[req] = usersfunctions.getUser(req.senderID)
    preqs = friendsfunctions.getPendingFriendRequests(userID)
    pendingfriendrequests = {}
    for preq in preqs:
        pendingfriendrequests[preq] = usersfunctions.getUser(preq.receiverID)
    print(pendingfriendrequests)
    return render_template("friends.html", users=users, friendrequests=friendrequests, pendingfriendrequests=pendingfriendrequests)

@app.route("/searchfriends", methods=["POST"])
@login_required
def searchfriends():
    #searchfunction in the webpage
    userID = session['userID']
    query = request.form['query']
    users = usersfunctions.searchUsers(query)
    reqs = friendsfunctions.getFriendRequests(userID)
    #looks through the entire doc to match ur search queary, no AI used to autofill or anythign fance
    friendrequests = {}
    for req in reqs:
        friendrequests[req] = usersfunctions.getUser(req.senderID)
    preqs = friendsfunctions.getPendingFriendRequests(userID)
    pendingfriendrequests = {}
    for preq in preqs:
        pendingfriendrequests[preq] = usersfunctions.getUser(preq.receiverID)
        #also showing if a request is pending under each frtiends
    #print(pendingfriendrequests)
    return render_template("friends.html", users=users, friendrequests=friendrequests, pendingfriendrequests=pendingfriendrequests)

@app.route("/allusers")
@login_required
def allusers():
    userID = session['userID']
    users = usersfunctions.getAllUsers()
    reqs = friendsfunctions.getFriendRequests(userID)
    friendrequests = {}
    for req in reqs:
        #gewtting all the userts for the searchfriends functions
        friendrequests[req] = usersfunctions.getUser(req.senderID)
    preqs = friendsfunctions.getPendingFriendRequests(userID)
    pendingfriendrequests = {}
    for preq in preqs:
        pendingfriendrequests[preq] = usersfunctions.getUser(preq.receiverID)
    print(pendingfriendrequests)
    return render_template("friends.html", users=users, friendrequests=friendrequests, pendingfriendrequests=pendingfriendrequests)

@app.route("/sendfriendrequest/<receiverID>")
@login_required
def sendfriendrequest(receiverID):
    friendsfunctions.sendFriendRequest(session['userID'], receiverID)
    #send those freindrequests
    return redirect(url_for('friends'))

@app.route("/acceptfriendrequest/<requestID>")
@login_required
def acceptfriendrequest(requestID):
    friendsfunctions.acceptFriendRequest(requestID)
    #acceot the friendrequests
    return redirect(url_for('friends'))

@app.route("/declinefriendrequest/<requestID>")
@login_required
def declinefriendrequest(requestID):
    #decline the weirdos
    friendsfunctions.declineFriendRequest(requestID)
    return redirect(url_for('friends'))

@app.route("/profile/<userID>")
@login_required
def profile(userID):
    currentuserID = session['userID']
    if currentuserID == int(userID):
        return redirect(url_for('myfeed'))
        #custom vs standard feed
    else:
        user = usersfunctions.getUser(userID)
        isFriend = friendsfunctions.isFriend(currentuserID, userID)
        posts = postsfunctions.getUserPosts(user.userID)
        return render_template("profile.html", user=user, isFriend=isFriend, posts=posts)

@app.route("/communities")
@login_required
def communities():
    community_data = communitiesfunctions.getAllCommunities()
    #community data getiting pulled to see where ur in
    #make a dict with all the communities
    communities = {}
    for community in community_data:
        if communitiesfunctions.inCommunity(session['userID'], community.communityID):
            communities[community] = True
        else:
            #only shows the ones ur in to be the ones ur in
            communities[community] = False
    return render_template("communities.html", communities=communities)

@app.route("/newcommunity", methods = ["POST"])
@login_required
def newcommunity():
    #makes a new community and logs in on the database
    userID = session['userID']
    name = request.form['name']
    description = request.form['description']
    if communitiesfunctions.getCommunityByName(name) != None:
        flash('Community with that name already exists', 'error')
        return redirect(url_for("communities"))
    communitiesfunctions.createCommunity(name, description)
    community = communitiesfunctions.getCommunityByName(name)
    communitiesfunctions.joinCommunity(userID, community.communityID)
    return redirect(url_for('community', communityID = community.communityID))


@app.route("/joincommunity/<communityID>")
@login_required
def joincommunity(communityID):
    communitiesfunctions.joinCommunity(session['userID'], communityID)
    return redirect(url_for("community", communityID=communityID, ))
    #JOIN button

@app.route("/leavecommunity/<communityID>")
@login_required
def leavecommunity(communityID):
    communitiesfunctions.leaveCommunity(session['userID'], communityID)
    return redirect(url_for("communities"))
    #leave button

@app.route("/community/<communityID>")
@login_required
def community(communityID):
    #community page for each one
    community = communitiesfunctions.getCommunity(communityID)
    incommunity = communitiesfunctions.inCommunity(session['userID'], communityID)
    post_data = postsfunctions.getCommunityPosts(communityID)
    posts = {}
    for post in post_data:
        posts[post] = postsfunctions.getCreator(post.postID)
    return render_template("community.html", community=community, incommunity=incommunity, posts=posts)
    #shows all the posts in chronological order ^^^

@app.route("/community/<communityID>/members")
@login_required
def communitymembers(communityID):
    community = communitiesfunctions.getCommunity(communityID)
    members = communitiesfunctions.getMembers(communityID)
    return render_template("communitymembers.html", community=community, members=members)
    #show the members in each community

@app.route("/game")
@login_required
def game():
    return render_template("game.html")
    #snake

@app.route("/messages/")
@login_required
def messages():
    friendslist = friendsfunctions.getFriends(session['userID'])
    return render_template("messages.html", friends=friendslist)

    #messages page, showing list of friends and stuff

@app.route("/messages/<contactID>")
@login_required
def chat(contactID):
    contact = usersfunctions.getUser(contactID)
    chat = messagesfunctions.getMessages(session['userID'], contactID)
    return render_template("chat.html", userID = session['userID'], contact=contact, messages=chat)
    #chatting to an individual person, showin all past messages

@app.route("/sendmessage/<contactID>", methods=["POST"])
@login_required
def sendmessage(contactID):
    content = request.form['content']
    messagesfunctions.sendMessage(session['userID'], contactID, content)
    return redirect(url_for('chat', contactID=contactID))
    #send a message and put it on the database

@app.route("/me")
@login_required
def myfeed():
    userID = session['userID']
    user = usersfunctions.getUser(userID)
    posts = postsfunctions.getUserPosts(userID)
    return render_template("me.html", user=user, posts=posts)
    #the personal feed mentioned earlier, with the custom html that says Welcome, Name.

@app.route("/community/<communityID>/post", methods=["POST"])
@login_required
def communitypost(communityID):
    content = request.form['content']
    title = request.form['title']
    postsfunctions.createPost(communityID, session['userID'], title, content)
    return redirect(url_for("community", communityID=communityID))
    #same posting mechanism as in blog, request forms and upload them as strings
    #on a db for communities

@app.route("/post", methods=["POST"])
@login_required
def timelinepost():
    content = request.form['content']
    title = request.form['title']
    postsfunctions.createPost(None, session['userID'], title, content)
    return redirect(url_for("myfeed"))
    #these are gonna be a persons timelinepost
    #equivalent to facebooks

@app.route("/post/<postID>")
@login_required
def viewpost(postID):
    post = postsfunctions.getPost(postID)
    creator = postsfunctions.getCreator(postID)
    comment_data = commentsfunctions.getComments(postID)
    comments = {}
    for comment in comment_data:
        comments[comment] = usersfunctions.getUser(comment.userID)
    return render_template("post.html", post=post, creator=creator, comments=comments)

@app.route("/writecomment/<postID>", methods=["POST"])
@login_required
def writecomment(postID):
    content = request.form['content']
    commentsfunctions.createComment(postID, session['userID'], content)
    return redirect(url_for("viewpost", postID=postID))


#STANDARD LOGIN FROM OTHER PROJECTS BELOW (little comments cuz its ez now)
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register", methods=["POST"])
def register():
    if "userID" in session:
        return redirect(url_for('feed'))
    email = request.form['email']
    pass1 = request.form['password']
    pass2 = request.form['confpassword']
    if usersfunctions.getUserByEmail(email) != None:
        flash("Account with that email already exsists", "error")
        return redirect(url_for('signup'))
    if pass1 != pass2 :
        flash("Passwords do not match", "error")
        return redirect(url_for('signup'))
    flash("Account created successfuly. Please sign in", "success")
    usersfunctions.registerUser(email,pass1,request.form['first'],request.form['last'],request.form['grade'])
    return redirect(url_for('login'))

@app.route("/auth", methods=["POST"])
def auth():
    if "userID" in session:
        flash("You were already logged in, "+session['displayName']+".", "error")
        return redirect(url_for('dashboard'))
    # information inputted into the form by the user
    user = usersfunctions.getUserByEmail(request.form['email'])
    if user == None: # if email not found
        flash("No user found with given email", "error")
        return redirect(url_for('login'))
    elif request.form['password'] != user.password: # if password is incorrect
        flash("Incorrect password", "error")
        return redirect(url_for('login'))
    else: # hooray! the email and password are both valid
        session['userID'] = user.userID
        session['firstName'] = user.firstName
        session['lastName'] = user.lastName
        session['displayName'] = user.firstName + ' ' + user.lastName
        return redirect(url_for('dashboard'))

@app.route("/logout")
def logout():
    if not "userID" in session:
        flash("Already logged out, no need to log out again", "error")
    else:
        session.pop('userID')
        session.pop('firstName')
        session.pop('lastName')
        session.pop('displayName')
        flash("Successfuly logged out", "success")
    return redirect(url_for('root')) # should redirect back to login

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()
