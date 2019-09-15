# Team Burger King - Biraj Chowdhury and Kazi Jamal
# SoftDev 1 pd9
# K #06: StI/O: Divine your Destiny!
# 2019-09-17

import csv
import random

occupations_dict = {}
occupations_list = []


def init_dict(dict, filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        line_count = 0
        for line in reader:
            if (line_count == 0):
                line_count += 1
                continue
            dict[line[0]] = float(line[1])
            line_count += 1


def rand_occupation(dict, list):
    occupation_count = 0
    for occupation in dict:
        if (occupation_count == len(dict)-1):
            break
        occupation_freq = int(dict[occupation] * 10)
        for i in range(0, occupation_freq):
            list.append(occupation)
        occupation_count += 1
    return random.choice(occupations_list)


init_dict(occupations_dict, "occupations.csv")
print(rand_occupation(occupations_dict, occupations_list))
