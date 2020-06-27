from .models import db, Comment

def getComments(postID):
    comments = Comment.query.filter_by(postID=postID).order_by(Comment.timestamp.asc()).all()
    return comments

def createComment(postID, userID, content):
    comment = Comment(postID=postID, userID=userID, content=content)
    db.session.add(comment)
    db.session.commit()

def deleteComment(commentID):
    Comment.query.filter_by(commentID=commentID).first().delete()
    db.session.commit()