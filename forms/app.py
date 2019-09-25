from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def root():
    print(app)
    return __name__

@app.route("/foo.html")
def foo():
    return render_template("foo.html")

@app.route("/auth")
def auth():
    print(app)
    print(request)
    print(request.args)
    return "aaaaa"

if __name__ == "__main__":
    app.debug = True
    app.run()
