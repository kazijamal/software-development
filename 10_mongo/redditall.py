# Team rslashsoftdev -- Alice Ni and Kazi Jamal
# Softdev pd9
# K10 -- Import/Export Bank
# 2020-03-04

from pymongo import MongoClient
import json
import pprint

client = MongoClient('localhost', 27017)

db = client.reddit
col = db['children']
col.delete_many({})

if (col.count_documents({}) == 0):
    f = open('all.json', 'r')
    content = f.read()
    f.close()
    dataset = json.loads(content)
    children = dataset['data']['children']
    for child in children:
        pprint.pprint(child)
    col.insert_many(children)
