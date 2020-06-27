import csv

numArticlesPerDay = {}

with open("../static/csv/num-articles-per-day.csv") as num_articles_per_day_csv:
  data = csv.reader(num_articles_per_day_csv, delimiter=",")
  next(data) # skips header

  for day in data:
    date = day[0]
    numArticles = day[1]
    numArticlesPerDay[date] = int(numArticles)

print(numArticlesPerDay)