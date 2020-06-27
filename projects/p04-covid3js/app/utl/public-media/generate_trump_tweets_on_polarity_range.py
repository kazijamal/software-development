#40918 onward
import csv
import sys
from textblob import TextBlob

csv.field_size_limit(sys.maxsize) # Resolves error: _csv.Error: field larger than field limit (131072)

trump_tweets_sentiment_arr = []

filename = "realdonaldtrump.csv"
counter = 0
with open(filename) as csvfile:
  articles = csv.reader(csvfile, delimiter=",")
  next(articles)
  for article in articles:
    trump_tweets_sentiment_arr.append(float(TextBlob(article[2]).sentiment.polarity))
  
trump_tweets_sentiment_range_dict = {-0.8: 0, -0.6: 0, -0.4: 0, -0.2: 0, 0.0: 0, 0.2: 0, 0.4: 0, 0.6: 0, 0.8: 0, 1.0: 0 }

for el in trump_tweets_sentiment_arr:
  for key in trump_tweets_sentiment_range_dict.keys():
    if el <= key:
      trump_tweets_sentiment_range_dict[key] += 1
      break

with open("output1.csv", "w") as output_file:
  output = csv.writer(output_file, delimiter=",")
  output.writerow(["index", "polarity"])
  for idx, el in enumerate(trump_tweets_sentiment_arr):
    output.writerow([idx + 1, el])