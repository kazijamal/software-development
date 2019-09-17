from flask import Flask, render_template
app = Flask(__name__)  # create instance of class Flask


@app.route("/")  # assign following fxn to run when root route requested
def hello_world():
    print(__name__)  # where will this go?
    return "No hablo queso!"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == "__main__":
    app.debug = True
    app.run()
