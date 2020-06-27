# This should be used in Google Colab

import csv
import os
import sys

csv.field_size_limit(sys.maxsize) # Resolves error: _csv.Error: field larger than field limit (131072)

# These paths are repository-specific, ignore for Colab
# csvDirPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "csv")
# covid19ArticlesFilePath = os.path.join(csvDirPath, "covid19_articles.csv")

numArticlesPerDay = {}

with open("covid19_articles.csv", encoding="utf8") as csvfile:
  articles = csv.reader(csvfile, delimiter=",")
  next(articles) # skips header
  for article in articles:
    date = article[2]
    content = article[6]
    if date in numArticlesPerDay:
      numArticlesPerDay[date] += 1
    else:
      numArticlesPerDay[date] = 1

# numArticlesPerDayFilePath = os.path.join(csvDirPath, "num-articles-per-day.csv")

with open("num-articles-per-day.csv", "w") as output_file:
  output = csv.writer(output_file, delimiter=",")

  for key, val in numArticlesPerDay.items():
    output.writerow([key, val])