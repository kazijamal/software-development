from itertools import islice
import spacy
import csv
import sys
from operator import itemgetter 

csv.field_size_limit(sys.maxsize) # Resolves error: _csv.Error: field larger than field limit (131072)

filename = "covid19_articles.csv"

texts = []

with open(filename) as csvfile:
  articles = csv.reader(csvfile, delimiter=",")
  next(articles)
  for article in articles:
    texts.append(article[6])

print(len(texts))

nlp = spacy.load('en')
doc = nlp()

named_entities = {}
for doc in nlp.pipe(texts):
    for ent in doc.ents:
      text = ent.text
      print(text)
      if text not in named_entities:
        named_entities[text] = 0
      else:
        named_entities[text] += 1

  
# Initialize N  
N = 1000
  
# N largest values in dictionary 
# Using sorted() + itemgetter() + items() 
res = dict(sorted(named_entities.items(), key = itemgetter(1), reverse = True)[:N]) 

with open("named-entity-frequencies.csv", "w") as output_file:
  output = csv.writer(output_file, delimiter=",")
  output.writerow(["namedEntity", "frequency"])
  for key, val in res.items():
    output.writerow([key, val])