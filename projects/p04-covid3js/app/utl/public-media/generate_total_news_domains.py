# This should be used in Google Colab

import csv
import sys

csv.field_size_limit(sys.maxsize) # Resolves error: _csv.Error: field larger than field limit (131072)

filename = "covid19_articles.csv"

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

with open("total-news-domains.csv", "w") as output_file:
  output = csv.writer(output_file, delimiter=",")

  for key, val in domains.items():
    output.writerow([key, val])