import csv
import sys
from textblob import TextBlob

csv.field_size_limit(sys.maxsize) # Resolves error: _csv.Error: field larger than field limit (131072)

sentiment_dict = {}

filename = "covid19_articles.csv"

import csv
import sys

csv.field_size_limit(sys.maxsize) # Resolves error: _csv.Error: field larger than field limit (131072)

domains = {}

with open(filename) as csvfile:
  articles = csv.reader(csvfile, delimiter=",")
  next(articles)
  for article in articles:
    domain = article[4]
    if domain in domains:
      domains[domain] += 1
    else:
      domains[domain] = 1

counter = 0
with open(filename) as csvfile:
  articles = csv.reader(csvfile, delimiter=",")
  next(articles)
  for article in articles:
    domain = article[4]
    if domain in sentiment_dict:
      sentiment_dict[domain] += float(TextBlob(article[6]).sentiment.subjectivity)
    else:
      sentiment_dict[domain] = float(TextBlob(article[6]).sentiment.subjectivity)

average_polarity_dict = {}
for key, val in sentiment_dict.items():
  average_polarity_dict[key] = val / domains[key]

with open("output.csv", "w") as output_file:
  output = csv.writer(output_file, delimiter=",")

  for key, val in average_polarity_dict.items():
    output.writerow([key, val])

    0.0