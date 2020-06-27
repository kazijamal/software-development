from .models import db, User

def registerUser(email, password, firstName, lastName, grade):
    displayName = firstName + ' ' + lastName
    user = User(email=email, password=password, firstName=firstName, lastName=lastName, displayName=displayName, grade=grade)
    db.session.add(user)
    db.session.commit()

def authenticateUser(email, password):
    user = User.query.filter_by(email=email, password=password).first()
    if user == None:
        return False
    return True
def getUserByEmail(email):
    user = User.query.filter_by(email=email).first()
    return user

def getUser(userID):
    user = User.query.filter_by(userID=userID).first()
    return user

def getAllUsers():
    users = User.query.order_by(User.displayName.asc())
    return users

def searchUsers(query):
    users = User.query.filter(User.displayName.like('%' + query + '%'))
    return users