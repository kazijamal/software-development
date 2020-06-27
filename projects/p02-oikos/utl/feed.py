from .models import db, User, Community, Post, Member, Friend

def getCommunityPosts(userID):
    members = Member.query.filter_by(userID=userID).all()
    communityID = []
    for member in members:
        communityID.append(member.communityID)
    posts = Post.query.filter(Post.communityID.in_(communityID)).order_by(Post.timestamp.desc())
    return posts

def getTimelinePosts(userID):
    friends = Friend.query.filter_by(userID=userID)
    friendID = []
    for friend in friends:
        friendID.append(friend.friendID)
    posts = Post.query.filter(Post.communityID==None, Post.userID.in_(friendID)).order_by(Post.timestamp.desc())
    return posts