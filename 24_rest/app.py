from flask import Flask, render_template
import urllib2, json
app = Flask(__name__)

@app.route("/")
def root():
    u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=VLDCOQP6GcKTIqjBvRfwS8LvAAERQlx0n9f0Hwz5")
    response = u.read()
    data = json.loads(response)
    return render_template("index.html", pic = data['url'], explanation = data['explanation'])

if __name__ == "__main__":
    app.debug = True
    app.run()
