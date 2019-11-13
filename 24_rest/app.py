# Kazi Jamal
# SoftDev1 pd9
# K24 -- A RESTful Journey Skyward
# 2019-11-12

from flask import Flask, render_template
import urllib.request as urllib2
import json
app = Flask(__name__)

@app.route("/")
def root():
    u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=4P58G77ch5wxPDd5lZCCSZHJ7F4grda65M5qTphW")
    response = u.read()
    data = json.loads(response)
    return render_template("index.html", pic = data['url'], explanation = data['explanation'], title = data['title'])

if __name__ == "__main__":
    app.debug = True
    app.run()
