from flask import Flask
app = Flask(__name__)

@app.route("/")
def root():
    print(__name__)
    return "this is the root"

coll = [0,1,1,2,3,5,8]

@app.route("/my_foist_template")
def first_template():
    print("my_foist_template")
    return "my_first_template.html"

if __name__ == "__main__":
    app.debug = True
    app.run()
