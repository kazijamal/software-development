# Team rslashsoftdev -- Alice Ni and Kazi Jamal
# Softdev pd9
# K10 -- Import/Export Bank
# 

from pymongo import MongoClient
import json
import pprint

client = MongoClient('localhost', 27017)

f = open('all.json', 'r')
dataset = json.loads(f.read())
f.close()

db = client.reddit

posts = db.posts

# clear
posts.delete_many({})
