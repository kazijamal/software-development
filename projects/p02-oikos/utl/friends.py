from .models import db, Friend, FriendRequest, User

def getFriends(userID):
    friends = Friend.query.filter_by(userID=userID).order_by(Friend.displayName.asc()).all()
    return friends

def getFriendRequests(userID):
    friendrequests = FriendRequest.query.filter_by(receiverID=userID).order_by(FriendRequest.timestamp.desc()).all()
    return friendrequests

def getPendingFriendRequests(userID):
    friendrequests = FriendRequest.query.filter_by(senderID=userID).order_by(FriendRequest.timestamp.desc()).all()
    return friendrequests

def sendFriendRequest(senderID, receiverID):
    friendrequest = FriendRequest(senderID=senderID, receiverID=receiverID)
    db.session.add(friendrequest)
    db.session.commit()

def acceptFriendRequest(requestID):
    friendrequest = FriendRequest.query.filter_by(requestID=requestID).first()
    user = User.query.filter_by(userID=friendrequest.receiverID).first()
    frienduser = User.query.filter_by(userID=friendrequest.senderID).first()
    friend1 = Friend(userID=user.userID, friendID=frienduser.userID, displayName=frienduser.displayName)
    friend2 = Friend(userID=frienduser.userID, friendID=user.userID, displayName=user.displayName)
    db.session.delete(friendrequest)
    db.session.add(friend1)
    db.session.add(friend2)
    db.session.commit()

def declineFriendRequest(requestID):
    friendrequest = FriendRequest.query.filter_by(requestID=requestID).first()
    db.session.delete(friendrequest)
    db.session.commit()

def isFriend(userID, friendID):
    friend = Friend.query.filter_by(userID=userID, friendID=friendID).first()
    return friend != None
