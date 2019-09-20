# Team Konstant Acceleration -- Kazi Jamal and Albert Wan
# SoftDev1 pd9
# K10 -- Jinja Tuning
# 2019-09-24

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def root():
    print(__name__)
    return "this is the root"

@app.route("/occupyflaskst")
def occupy():
    print("occupyflaskst")
    return render_template("occupy.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
