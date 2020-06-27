# Team HanSolo -- Kazi Jamal
# SoftDev1 pd9
# K25 -- Getting More REST
# 2019-11-14

from flask import Flask, render_template
import urllib.request as urllib2
import json

app = Flask(__name__)

@app.route("/")
def root():

    # IP Location
    ip_api = urllib2.urlopen("http://ip-api.com/json/")
    ip_response = ip_api.read()
    ip_data = json.loads(ip_response)
 
    # SpaceX
    spacex_api = urllib2.urlopen("https://api.spacexdata.com/v3/launches/latest")
    spacex_response = spacex_api.read()
    spacex_data = json.loads(spacex_response)

    # New York Times
    nyt_api = urllib2.urlopen("https://api.nytimes.com/svc/topstories/v2/home.json?api-key=91JvL9mutOEgQyP1ZgVlvPw4Ur0TDVAS")
    nyt_response = nyt_api.read()
    nyt_data = json.loads(nyt_response)
    
    return render_template("index.html", ip = ip_data, spacex = spacex_data, nyt = nyt_data['results'][0])

if __name__ == "__main__":
    app.debug = True
    app.run()
