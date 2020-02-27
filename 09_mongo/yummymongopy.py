from pymongo import MongoClient
from bson.json_util import loads

client = MongoClient()

f = open('primer-dataset.json', 'r')
dataset = f.read().split('\n')
f.close()

items = []

for item in dataset:
    items.append(loads(item))
    
db = client.primer

restaurants = db.restaurants

result = restaurants.insert_many(items)

print(result)
