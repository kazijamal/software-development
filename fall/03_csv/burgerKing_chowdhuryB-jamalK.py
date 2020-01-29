# Team Burger King -- Biraj Chowdhury and Kazi Jamal
# SoftDev1 pd9
# K06 -- StI/O: Divine your Destiny!
# 2019-09-17

import random

# opens csv file for reading and formats into data
csv = open("occupations.csv", "r")
data = csv.read().strip('\n').split('\n')

occupations_dict = {}

# initialilzes dictionary with occupations from csv as keys and the percentage of the U.S. workforce they compromise as values


def init_dict():
    for entry in data[1:len(data)-1]:
        # adds occupations containing commas to dictionary
        if entry.count(',') > 1:
            occupation = entry.strip('"').split('"')
            occupations_dict[occupation[0]] = float(occupation[1].strip(','))
        # adds occupations without commas to dictionary
        else:
            occupation = entry.split(',')
            occupations_dict[occupation[0]] = float(occupation[1])


# closes csv file
csv.close()

# returns a randomly selected occupation where the results are weighted by the percentage given


def random_occupation(dict):
    # generates random number within [0, total percentage)
    rand = random.random() * float(data[len(data)-1].split(',')[1])
    sum = 0.0
    for occupation in dict:
        sum += dict[occupation]
        if rand < sum:
            return occupation

# tests the random_occupation(dict) function by calling it 1000 times and keeping track of the frequency of generated occupations


def testing():
    frequency = {}
    for occupation in occupations_dict:
        frequency[occupation] = 0
    for i in range(0, 100000):
        rand = random_occupation(occupations_dict)
        frequency[rand] += 1
    return frequency


init_dict()
print('dictionary of occupations:\n' + str(occupations_dict) + '\n')
print('random occupation: ' + random_occupation(occupations_dict) + '\n')
print('frequencies for testing random occupation with 100000 trials:\n' + str(testing()))
