# Team rslashsoftdev -- Alice Ni and Kazi Jamal
# Softdev pd9
# K10 -- Import/Export Bank
# 2020-03-04

"""
name of dataset: Reddit /r/all
description of its contents: Contains posts from the Reddit subreddit /r/all
hyperlink to where raw data is hosted: https://www.reddit.com/r/all.json
brief summary of import mechanism:
read the json file
load the data as a json
find the posts in a children array that is within the data object
use insert_many to add the children array to the posts collection in our database 
"""

from pymongo import MongoClient
import json
import pprint

client = MongoClient('localhost', 27017)

db = client.rslashsoftdev
posts = db['posts']
posts.delete_many({})

f = open('all.json', 'r')
content = f.read()
f.close()
dataset = json.loads(content)
children = dataset['data']['children']
posts.insert_many(children)

def findSubreddit(subreddit):
    print('----- found posts in r/' + subreddit + '\n')
    for post in posts.find({'data.subreddit': subreddit}):
        print(post['data']['title'] + '\n')

def findGreaterScore(score):
    print('----- found posts with score greater than ' + str(score) + '\n')
    for post in posts.find({'data.score': {'$gt': score}}):
        print(post['data']['title'] + ': ' + str(post['data']['score']) + '\n')

def findLessCrossPosts(crossposts):
    print('----- found posts with less than ' + str(crossposts) + ' crossposts\n')
    for post in posts.find({'data.num_crossposts': {'$lt': crossposts}}):
        print(post['data']['title'] + ': ' + str(post['data']['num_crossposts']) + '\n')

def findGreaterEqualComments(comments):
    print('----- found posts with greater than or equal to ' + str(comments) + ' comments\n')
    for post in posts.find({'data.num_comments': {'$gte': comments}}):
        print(post['data']['title'] + ': ' + str(post['data']['num_comments']) + '\n')

def findGreaterScoreComments(score, comments):
    print('----- found posts with greater than ' + str(score) + ' score and ' + str(comments) + ' comments\n')
    for post in posts.find({'data.score': {'$gt': score}, 'data.num_comments': {'$gt': comments}}):
        print(post['data']['title'] + ': ' + str(post['data']['score']) + ' score and ' + str(post['data']['num_comments']) + ' comments\n')
        
findSubreddit('Coronavirus')
findGreaterScore(40000)
findLessCrossPosts(1)
findGreaterEqualComments(1046)
findGreaterScoreComments(40000, 1046)
            
client.close()
