# Team Night Knight - Kazi Jamal and Nahi Khan
# SoftDev1 pd9
# K17 -- No Trouble
# 2019-10-10

import sqlite3  # enable control of an sqlite database
import csv      # facilitate CSV I/O

DB_FILE="school.db"

db = sqlite3.connect(DB_FILE)   # open if file exists, otherwise create
c = db.cursor()                 # facilitate db ops

#=======================================================================

# students table

with open('students.csv') as studentscsv:
    studentsReader = csv.DictReader(studentscsv)
    # creates students table
    createCommand = "CREATE TABLE students (name TEXT, age INTEGER, id INTEGER PRIMARY KEY);"
    c.execute(createCommand)
    # iterates through rows in csv as dictionaries
    for row in studentsReader:
        # inserts data from the current row into the students table
        insertCommand = "INSERT INTO students VALUES (\"{}\", {}, {});".format(row['name'], row['age'], row['id'])
        c.execute(insertCommand)

# courses table

with open('courses.csv') as coursescsv:
    coursesReader = csv.DictReader(coursescsv)
    # creates courses table
    createCommand = "CREATE TABLE courses (code TEXT, mark INTEGER, id);"
    c.execute(createCommand)
    # iterates through rows in csv as dictionaries
    for row in coursesReader:
        # inserts data from the current row into the courses table
        insertCommand = "INSERT INTO courses VALUES (\"{}\", {}, {})".format(row['code'], row['mark'], row['id'])
        c.execute(insertCommand)

q = "SELECT name, students.id, mark FROM students, courses WHERE students.id = courses.id;"

foo = c.execute(q)

print(foo)

for bar in foo:
    print(bar)

#=======================================================================

db.commit() # save changes
db.close()  # close database
