# Kazi Jamal and ray. lee. -- Team patient0
# SoftDev pd9
# K18 -- Come Up For Air
# 2020-04-21

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def root():
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
