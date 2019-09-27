# Team Konstant Acceleration II - Kazi Jamal and Ahmed Sultan
# SoftDev1 pd9
# K12 -- Echo Echo Echo
# 2019-09-27

from flask import Flask
from flask import render_template
from flask import request
from utl import ants

app = Flask(__name__)

@app.route("/")
def root():
    print(ants.add("test"," ants.add"))
    print(ants.add(1,2))
    return render_template("landing.html")

@app.route("/auth")
def auth():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.args ***")
    print(request.args)
    print("***DIAG: request.args['username'] ***")
    print(request.args["username"])
    print("***DIAG: request.headers ***")
    print(request.headers)
    return render_template(
        "response.html",
        username=request.args["username"],
        reqmethod=request.method
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
