from utl import dbcreatefunctions, dbfunctions


# returns all story edits, sorted by date, where the first item would be the oldest entry.
def getStoryEdits(c, storyID):
    c.execute('SELECT * FROM story_edits WHERE storyID = ? ORDER BY datetime(timestamp) ASC', (storyID,))
    return c.fetchall()

# returns story's latest update. - a tuple
# It does so by first getting all story edits, sorted ascending by date, and taking the latest one.
def getLatestStoryEdit(c, storyID):
    edits = getStoryEdits(c, storyID)
    return edits[-1]

# edits a story by asking for all the information in an entry, and inserts it into the story_edits table.
def addToStory(c, storyID, userID, username, content,):
    c.execute("INSERT INTO story_edits VALUES (?, ?, ?, ?, datetime('now'))", (storyID, userID, username, content))

# returns all the stories this user has edited (can Read)
# does this by selecting all stories where its' id is in the (list of stories that the user has edited)
def getStoriesEdited(c, userID):
    c.execute('SELECT * FROM stories where storyID IN (SELECT storyID FROM story_edits WHERE userID = ?)', (userID, ))
    return c.fetchall()

# returns all the stories this user has not edited (cannot Read)
# does this by selecting all stories where its' id is not in the (list of stories that the user has edited)
def getStoriesNotEdited(c, userID):
    c.execute('SELECT * FROM stories where storyID NOT IN (SELECT storyID FROM story_edits WHERE userID = ?)', (userID, ))
    return c.fetchall()

# checks if a user has edited a story
def hasEdited(c, userID, storyID):
    c.execute('SELECT * FROM story_edits WHERE userID = ? AND storyID = ?', (userID, storyID))
    return c.fetchone() != None

# debug function to test if databse funcitons are working
def debugAdd(c):
    dbfunctions.dropTables(c)
    dbfunctions.createTables(c)
    dbcreatefunctions.createStory(c, 1, 'HelloWorld', 0, 'StrawBerry', 'hi',)
    dbcreatefunctions.createStory(c, 2, 'HelloWorxd', 0, 'StrawBerry', 'test',)
    addToStory(c, 1, 5, 'TheLastStraw', ' world')
    dbfunctions.debugPrintSelect(c, 'story_edits')
    dbfunctions.debugPrintSelect(c, 'stories')
    print (str(getStoriesEdited(c, 5)))
    print (str(getStoriesNotEdited(c, 5)))
    print (hasEdited(c, 5, 1))
