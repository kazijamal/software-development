# Kazi Jamal
# SoftDev1 pd9
# K08 -- Lemme Flask You Sump’n
# 2019-09-19

from flask import Flask
app = Flask(__name__)


@app.route("/")
def home():
    print("path: /")
    print(__name__)
    return "This is the home page"


@app.route("/about")
def about():
    print("path: /about")
    print("about")
    return "This is the about page"


@app.route("/var/<variable>")
def var(variable):
    print("path: /var/" + variable)
    print(variable)
    return "The variable inputted in path was: " + variable


if __name__ == "__main__":
    app.debug = True
    app.run()
