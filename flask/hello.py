from flask import Flask
app = Flask(__name__)  # create instance of class Flask


@app.route("/")  # assign following fxn to run when root route requested
def hello_world():
    print(__name__)  # where will this go?
    return "No hablo queso!"

@app.route("/about")
def about():
    print("path: /about")
    print("about")
    return "This is a flask app"

@app.route("/var/<variable>")
def var(variable):
    print("path: /var/" + variable)
    print(variable)
    return "Variable inputted in path was: " + variable

if __name__ == "__main__":
    app.debug = True
    app.run()
