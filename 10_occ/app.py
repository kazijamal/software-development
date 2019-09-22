# Team Konstant Acceleration -- Kazi Jamal and Albert Wan
# SoftDev1 pd9
# K10 -- Jinja Tuning
# 2019-09-24

from flask import Flask, render_template
import random
app = Flask(__name__)


@app.route("/")
def root():
    print(__name__)
    return "this is the root"


def init_dict():
    # opens csv file for reading and formats into data
    csv = open("data/occupations.csv", "r")
    data = csv.read().strip('\n').split('\n')
    occupations_dict = {}

    # initialilzes dictionary with occupations from csv as keys and the percentage of the U.S. workforce they compromise as values
    for entry in data[1:]:
        # adds occupations containing commas to dictionary
        if entry.count(',') > 1:
            occupation = entry.strip('"').split('"')
            occupations_dict[occupation[0]] = float(occupation[1].strip(','))
        # adds occupations without commas to dictionary
        else:
            occupation = entry.split(',')
            occupations_dict[occupation[0]] = float(occupation[1])

    # closes csv and returns dictionary
    csv.close()
    return occupations_dict


def random_occupation(dict):
    # generates random number within [0, total percentage)
    rand = random.random() * float(dict["Total"])
    sum = 0.0
    for occupation in dict:
        sum += dict[occupation]
        if rand < sum:
            return occupation


@app.route("/occupyflaskst")
def occupy():
    print("occupyflaskst")
    occdict = init_dict()
    randocc = random_occupation(occdict)
    return render_template("occupy.html", dict=occdict, rand=randocc)


if __name__ == "__main__":
    app.debug = True
    app.run()
