# Team rslashsoftdev -- Alice Ni and Kazi Jamal
# Softdev pd9
# K10 -- Import/Export Bank
# 2020-03-04

"""
name of dataset: Reddit /r/all
description of its contents: Contains posts from the Reddit subreddit /r/all
hyperlink to where raw data is hosted: https://www.reddit.com/r/all.json
brief summary of import mechanism: 
"""

from pymongo import MongoClient
import json
import pprint

client = MongoClient('localhost', 27017)

db = client.rslashsoftdev
posts = db['posts']
posts.delete_many({})

if (posts.count_documents({}) == 0):
    f = open('all.json', 'r')
    content = f.read()
    f.close()
    dataset = json.loads(content)
    children = dataset['data']['children']
    for child in children:
        pprint.pprint(child)
    posts.insert_many(children)

client.close()
