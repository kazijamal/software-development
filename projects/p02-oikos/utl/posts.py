from .models import db, Post, User

def getUserPosts(userID):
    posts = Post.query.filter_by(communityID=None, userID=userID).order_by(Post.timestamp.desc())
    return posts

def getCommunityPosts(communityID):
    posts = Post.query.filter_by(communityID=communityID).order_by(Post.timestamp.desc())
    return posts

def createPost(communityID, userID, title, content):
    if communityID == None:
        post = Post(userID=userID, title=title, content=content)
    else:
        post = Post(communityID=communityID, userID=userID, title=title, content=content)
    db.session.add(post)
    db.session.commit()

def deletePost(postID):
    Post.query.filter_by(postID=postID).delete()
    db.session.commit()

def getPost(postID):
    post = Post.query.filter_by(postID=postID).first()
    return post

def getCreator(postID):
    post = Post.query.filter_by(postID=postID).first()
    userID = post.userID
    user = User.query.filter_by(userID=userID).first()
    return user