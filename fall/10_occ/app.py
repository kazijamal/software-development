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
    return "go to <a href=\"/occupyflaskst\">/occupyflaskst</a> route for occupations data"


def init_dict():
    # opens csv file for reading and formats into data
    csv = open("data/occupations.csv", "r")
    data = csv.read().strip('\n').split('\n')
    # removes csv header from data list
    data.pop(0)
    occupations_dict = {}

    # initialilzes dictionary with occupations from csv as keys and the percentage of the U.S. workforce they compromise as values
    for entry in data:
        print(entry)
        # adds occupations containing quotations to dictionary
        if entry.count(',') > 2:
            occupation = entry.strip('"').split('"')
            info = occupation[1].strip(',').split(',')
            occupations_dict[occupation[0]] = [float(info[0]), info[1]]
        # adds occupations without quotations to dictionary
        else:
            occupation = entry.split(',')
            occupations_dict[occupation[0]] = [
                float(occupation[1]), occupation[2]]

    # closes csv and returns dictionary
    csv.close()
    return occupations_dict


def random_occupation(dict):
    # generates random number within [0, total percentage)
    rand = random.random() * float(dict["Total"][0])
    bar = 0.0
    for occupation in dict:
        # adds current occupation weight to total sum
        bar += dict[occupation][0]
        # if random number is within current range which is [bar-dict[occupation],bar) return the current occupation
        if rand < bar:
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
