from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    firstName = db.Column(db.Text, nullable=False)
    lastName = db.Column(db.Text, nullable=False)
    displayName = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Text, nullable=False)

class Community(db.Model):
    communityID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Member(db.Model):
    memberID = db.Column(db.Integer, primary_key=True)
    communityID = db.Column(db.Integer, nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    displayName = db.Column(db.Integer, nullable=False)

class Post(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    communityID = db.Column(db.Integer, nullable=True)
    userID = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    postID = db.Column(db.Integer, nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class FriendRequest(db.Model):
    requestID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, nullable=False)
    receiverID = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Friend(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    friendID = db.Column(db.Integer, nullable=False)
    displayName = db.Column(db.Integer, nullable=False)

class Message(db.Model):
    messageID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, nullable=False)
    receiverID = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)