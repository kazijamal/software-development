# Team Burger King - Biraj Chowdhury and Kazi Jamal
# SoftDev 1 pd9
# K #06: StI/O: Divine your Destiny!
# 2019-09-17

import random

csv = open("occupations.csv", "r")
data = csv.read().strip('\n').split('\n')

occupations_dict = {}


def init_dict():
    for entry in data[1:len(data)-1]:
        if entry.count(',') > 1:
            occupation = entry.strip('"').split('"')
            occupations_dict[occupation[0]] = float(occupation[1].strip(','))
        else:
            occupation = entry.split(',')
            occupations_dict[occupation[0]] = float(occupation[1])


csv.close()


def random_occupation(dict):
    rand = random.random() * float(data[len(data)-1].split(',')[1])
    sum = 0.0
    for occupation in dict:
        sum += dict[occupation]
        if rand < sum:
            return occupation


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
