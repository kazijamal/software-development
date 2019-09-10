import random

KREWES = {'orpheus':['john','jeff'],'rex':['ashley','jake'],'endymion':['david','dan']}

def randStudent(dict):
    return random.choice(dict[random.choice(dict.keys())])

print(randStudent(KREWES))
