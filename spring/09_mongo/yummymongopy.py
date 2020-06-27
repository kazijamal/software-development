from pymongo import MongoClient
from bson.json_util import loads
import pprint

client = MongoClient('localhost', 27017)

f = open('primer-dataset.json', 'r')
dataset = f.read().split('\n')
f.close()

items = []

for item in dataset:
    items.append(loads(item))

db = client.primer

restaurants = db.restaurants

result = restaurants.insert_many(items)

# find restaurants by BOROUGH
def findBorough(borough):
    for restaurant in restaurants.find({'borough': borough}):
        pprint.pprint(restaurant)

# find restaurants by ZIPCODE
def findZipcode(zipcode):
    for restaurant in restaurants.find({'address.zipcode': zipcode}):
        pprint.pprint(restaurant)

# find restaurants by ZIPCODE and =GRADE 
def findZipcodeGrade(zipcode, grade):
     for restaurant in restaurants.find({'address.zipcode': zipcode, 'grades': {'$elemMatch': {'grade': grade}}}):
          pprint.pprint(restaurant)

# find restaurants by ZIPCODE and <SCORE
def findZipcodeScoreBelow(zipcode, score):
     for restaurant in restaurants.find({'address.zipcode': zipcode, 'grades': {'$elemMatch': {'score': {'$lt': score}}}}):
          pprint.pprint(restaurant)

# ~creative~: find restaurants by BOROUGH, CUISINE and >=SCORE
def findBoroughCuisineScore(borough, cuisine, score):
     for restaurant in restaurants.find({'borough': borough, 'cuisine': cuisine, 'grades': {'$elemMatch': {'score': {'$gte': score}}}}):
          pprint.pprint(restaurant)

# clear
restaurants.delete_many({})
