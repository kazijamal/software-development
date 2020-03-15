# Team rslashsoftdev -- Kazi Jamal Taejoon Kim
# Softdev pd9
# K11 -- Ay Mon Go Git It From Yer Flask
# 2020-03-17

from flask import Flask, render_template, request
from pymongo import MongoClient
import json

app = Flask(__name__)

# set up mongo database
client = MongoClient('localhost', 27017)
client.drop_database('rslashsoftdev')
db = client.rslashsoftdev
posts = db['posts']

# insert data into database from json
f = open('static/all.json', 'r')
content = f.read()
f.close()
dataset = json.loads(content)
children = dataset['data']['children']
subreddits = [child['data']['subreddit'] for child in children]
posts.insert_many(children)

@app.route("/")
def root():
    return render_template('index.html', subreddits=subreddits);

# search for posts from a subreddit
@app.route("/searchsubreddit", methods=['POST'])
def searchSubreddit():
    subreddit = request.form.get('subreddit')
    res = posts.find({'data.subreddit': subreddit})
    return render_template('posts.html', posts=res)

# search for posts with score greater than some score
@app.route("/searchgreaterscore")
def searchGreaterScore():
    score = request.args['score']
    res = posts.find({'data.score': {'$gt': score}})
    return render_template('posts.html', posts=res)

# search for posts with number of crossposts less than some number of scrossposts
@app.route("/searchlesscrossposts")
def searchLessCrossPosts():
    crossposts = request.args['crossposts']
    res = posts.find({'data.num_crossposts': {'$lt': crossposts}})
    return render_template('posts.html', posts=res)

# search for posts with number of comments greater than or equal to some number of comments
@app.route("/searchgreaterequalcomments")
def searchGreaterEqualComments():
    comments = request.args['comments']
    res = posts.find({'data.num_comments': {'$gte': comments}})
    return render_template('posts.html', posts=res)

# search for posts with score and number of comments greater than some score and number of comments
@app.route("/searchgreaterscorecomments")
def searchGreaterScoreComments():
    score = request.args['score']
    comments = request.args['comments']
    res = posts.find({'data.score': {'$gt': score}, 'data.num_comments': {'$gt': comments}})
    return render_template('posts.html', posts=res)

# search for posts by title
@app.route("/searchtitle")
def searchTitle():
    title = request.args['title']
    res = posts.find({'data.title': {'$regex': title, '$options': 'i'}})
    return render_template('posts.html', posts=res)

if __name__ == "__main__":
    app.debug = True
    app.run()
