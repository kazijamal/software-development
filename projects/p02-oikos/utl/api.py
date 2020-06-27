import urllib.request as request
import os
import json

apikeys_file = os.path.dirname(os.path.abspath(__file__)) + '/apikeys.json'

with open(apikeys_file, 'r') as read_file:
    apikeys = json.load(read_file)

NEWS_API_KEY = apikeys['NEWS_API_KEY']

def getTodayWeather():
    weatherlink = "https://www.metaweather.com/api/location/2459115/"
    weatherjson = request.urlopen(weatherlink).read()
    weather = json.loads(weatherjson)['consolidated_weather'][0]
    weather['min_temp'] = int(weather['min_temp'] * 9.0 / 5.0 + 32)
    weather['max_temp'] = int(weather['max_temp'] * 9.0 / 5.0 + 32)
    weather['the_temp'] = int(weather['the_temp'] * 9.0 / 5.0 + 32)
    return weather

def getTomorrowWeather():
    weatherlink = "https://www.metaweather.com/api/location/2459115/"
    weatherjson = request.urlopen(weatherlink).read()
    weather = json.loads(weatherjson)['consolidated_weather'][1]
    weather['min_temp'] = int(weather['min_temp'] * 9.0 / 5.0 + 32)
    weather['max_temp'] = int(weather['max_temp'] * 9.0 / 5.0 + 32)
    weather['the_temp'] = int(weather['the_temp'] * 9.0 / 5.0 + 32)
    return weather

def getNewsArticles():
    newslink = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + NEWS_API_KEY
    try: 
        newsjson = request.urlopen(newslink).read()
        news = json.loads(newsjson)['articles']
        return news
    except:
        return("Invalid API Key")

def xkcd():
    xkcdlink = "https://xkcd.com/info.0.json"
    xkcdjson = request.urlopen(xkcdlink).read()
    xkcd = json.loads(xkcdjson)
    return xkcd

