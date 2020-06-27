from .models import db, Community, Member, User

def getCommunityByName(name):
    community = Community.query.filter_by(name=name).first()
    return community

def getCommunity(communityID):
    community = Community.query.filter_by(communityID=communityID).first()
    return community

def getAllCommunities():
    communities = Community.query.all()
    return communities

def getCommunities(userID):
    members = Member.query.filter_by(userID=userID).all()
    communities = []
    for member in members:
        community = Community.query.filter_by(communityID=member.communityID).first()
        communities.append(community)
    return community

def inCommunity(userID, communityID):
    member = Member.query.filter_by(userID=userID, communityID=communityID).first()
    if member == None:
        return False
    return True

def getMembers(communityID):
    members = Member.query.filter_by(communityID=communityID).all()
    users = []
    for member in members:
        users.append(User.query.filter_by(userID=member.userID).first())
    return users

def createCommunity(name, description):
    community = Community(name=name, description=description)
    db.session.add(community)
    db.session.commit()

def joinCommunity(userID, communityID):
    user = User.query.filter_by(userID=userID).first()
    member = Member(communityID=communityID, userID=userID, displayName=user.displayName)
    db.session.add(member)
    db.session.commit()

def leaveCommunity(userID, communityID):
    Member.query.filter_by(userID=userID, communityID=communityID).delete()
    db.session.commit()
