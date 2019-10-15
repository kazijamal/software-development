# Team Terminal Kangaroos - Tammy Chen and Kazi Jamal
# SoftDev1 pd9
# K18 -- Average
# 2019-10-15

import sqlite3 # enable control of an sqlite database
import csv # faciliate CSV I/O

DB_FILE = "school.db"

db = sqlite3.connect(DB_FILE) # open if file exists, otherwise create
c = db.cursor() # facilitate db ops

gradesDict = {}
avgDict = {}

# initializes grades and average dictionaries with empty lists and 0.0 respectively
def initDict():
    q = "SELECT id FROM students;"
    a = c.execute(q)
    for line in a:
        gradesDict[line[0]] = [];
        avgDict[line[0]] = 0.0;

# looks up each students grades and adds to grades dictionary
def studentsGrades():
    q = "SELECT name, students.id, mark FROM students, courses WHERE students.id = courses.id;"
    a = c.execute(q)
    # adds grades to grades dictionary with id as key and current grade is appended to the value
    for line in a:
        gradesDict[line[1]].append(line[2])

# computes each students averages and adds to averages dictionary
def studentsAverages():
    for key in gradesDict:
        count = 0;
        # adds grades to average dictionary with id as key and grade gets added to the value
        for grade in gradesDict[key]:
            avgDict[key] += grade
            count += 1
        # the value for the current id in the average dictionary is divided by the number of grades to get the average
        avgDict[key] /= count

# prints each students name, id, and average
def printAverages():
    q = "SELECT name, id FROM students;"
    a = c.execute(q)
    # prints each student, their id, and their average
    for line in a:
        ans = "student: {}, id: {}, average: {}".format(line[0], line[1], avgDict[line[1]])
        print(ans)

# creates table of IDs and associated averages, named "stu_avg"
def createAvgTable():
    # creates stu_avg table in sqlite database
    createCommand = "CREATE TABLE stu_avg (id INTEGER PRIMARY KEY, avg REAL);"
    c.execute(createCommand)
    # adds id and average as records in stu_avg table
    for key in avgDict:
        insertCommand = "INSERT INTO stu_avg VALUES ({}, {});".format(key, avgDict[key])
        c.execute(insertCommand)

# function to faciliate adding rows to the courses table
def addCourses(code, id, mark):
    # adds a new row given the parameters code (string), id (integer), and mark (integer)
    c.execute('INSERT INTO courses VALUES(?,?,?)', (code, id, mark))
    c.execute('SELECT * FROM courses')

addCourses("health", 12, 1)
initDict()
studentsGrades()
studentsAverages()
printAverages()
createAvgTable()

db.commit() # save changes
db.close() # close database
