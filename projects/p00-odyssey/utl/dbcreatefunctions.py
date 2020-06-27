from utl import dbeditfunctions

# function that takes the given parameters to create a story & add it to the database
def createStory(c, storyID, title, userID, username, content,):
    c.execute('INSERT INTO stories VALUES (NULL, ?)', (title, ))
    dbeditfunctions.addToStory(c, storyID, userID, username, content)
