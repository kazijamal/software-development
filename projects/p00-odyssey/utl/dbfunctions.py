# used to debug databases (ie. tables)
def createTables(c):
    c.execute('CREATE TABLE IF NOT EXISTS stories (storyID INTEGER PRIMARY KEY, name TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS story_edits (storyID INTEGER, userID INTEGER, username STRING, content TEXT, timestamp DATETIME)')

    c.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, username TEXT, password TEXT)')

# used to debug !
def dropTables(c):
    c.execute('DROP TABLE IF EXISTS stories')
    c.execute('DROP TABLE IF EXISTS story_edits')
    c.execute('DROP TABLE IF EXISTS users')

# looks through stories to see if any of them contain the words from the search input
def getSearch(c, query):
    c.execute("SELECT * FROM stories WHERE name LIKE '%" + query + "%'")
    return c.fetchall()

# returns an array with all values from a given story's row in table.
# find this story by its id
def selectStory(c, storyID):
    c.execute('SELECT name FROM stories WHERE storyID = ?', (storyID, ))
    return c.fetchone()

# returns a tuple with all story names
def returnStoryNames(c):
    c.execute('SELECT name FROM stories')
    return c.fetchall()

# returns an array with entire table as data.
def getTable(c, table):
    c.execute('SELECT * FROM ' + table)
    return c.fetchall()

# returns the latest story ID (ie. use for read, creating & editing stories to make sure the story exists)
def getMaxStoryID(c):
    c.execute('SELECT MAX(storyID) FROM stories')
    return c.fetchone()[0]

# returns the username
def getUsername(c, userID):
    c.execute('SELECT username FROM users WHERE userID = ' + userID)
    return c.fetchone()[1]

# for debugging
def debugPrintSelect(c, table):
    c.execute('SELECT * FROM ' + table)
    print (str(c.fetchall()) + '\n')
