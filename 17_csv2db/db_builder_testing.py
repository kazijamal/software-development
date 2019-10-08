# Kazi Jamal
# SoftDev1 pd9
# K17 -- No Trouble
# 2019-10-09

import sqlite3  # enable control of an sqlite database
import csv      # facilitate CSV I/O

DB_FILE="school.db"

db = sqlite3.connect(DB_FILE)   # open if file exists, otherwise create
c = db.cursor()                 # facilitate db ops

#=======================================================================

# < < < INSERT YOUR POPULATE-THE-DB CODE HERE > > > 

# students table

with open('students.csv') as studentscsv:
    studentsReader = csv.DictReader(studentscsv)
    createCommand = "CREATE TABLE students (name TEXT, age INTEGER, id INTEGER PRIMARY KEY);"
    c.execute(createCommand)
    for row in studentsReader:
        insertCommand = "INSERT INTO students VALUES (\"{}\", {}, {});".format(row['name'], row['age'], row['id'])
        c.execute(insertCommand)

# courses table

with open('courses.csv') as coursescsv:
    coursesReader = csv.DictReader(coursescsv)
    createCommand = "CREATE TABLE courses (code TEXT, mark INTEGER, id);"
    c.execute(createCommand)
    for row in coursesReader:
        insertCommand = "INSERT INTO courses VALUES (\"{}\", {}, {})".format(row['code'], row['mark'], row['id'])
        c.execute(insertCommand)

#=======================================================================

db.commit() # save changes
db.close()  # close database
