import urllib.request as request
import json

def createTables(c):
    """Creates required tables for users, characters, and trivia in the database."""
    c.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, username TEXT, password TEXT, charID INTEGER, charName TEXT, charImg TEXT, xp INTEGER, strength INTEGER, intelligence INTEGER, luck INTEGER, gold INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS characters (userID, charID INTEGER, charName INTEGER, charImg TEXT)')
    c.execute('DROP TABLE IF EXISTS trivia')
    c.execute('CREATE TABLE IF NOT EXISTS trivia (number INTEGER, questions TEXT, one TEXT, two TEXT, three TEXT, four TEXT)')

def createUser(c, username, password, charID):
    """Creates a user and adds their information into the users and characters tables."""
    image = "https://rickandmortyapi.com/api/character/avatar/"+ charID +".jpeg"
    namejson = request.urlopen("https://rickandmortyapi.com/api/character/"+ charID).read()
    name = json.loads(namejson)['name']
    c.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, 0, 0, 0, 0, 50)', (username, password, int(charID), name, image))
    id = getUserIDByUsername(c,username)
    c.execute('INSERT INTO characters VALUES (?, ?, ?, ?)', (id, int(charID), name,image))

def getUserIDByUsername(c,username):
    """Returns the record in the users table for the provided username."""
    return c.execute("SELECT userID FROM users WHERE username = ?", (username, )).fetchone()[0]

def getUser(c,userID):
    """Returns the record in the users table for the provided userID."""
    return c.execute("SELECT * FROM users WHERE userID = " + userID).fetchone()

def getXP(c, userID):
    """Returns the xp of a user with the provided userID."""
    return c.execute("SELECT xp FROM users WHERE userID = ?", (userID, ))

def levelUp(xp1, xp2):
    """Returns a boolean value of whether the player has leveled up or not given the beginning and ending xp."""
    return (int(xp1/100) + 1) != (int(xp2/100) + 1)

def getImage(c, charID):
    """Returns the url for a characters image provided the character's ID."""
    image = "https://rickandmortyapi.com/api/character/avatar/"+str(charID)+".jpeg"
    return image

def getName(c, charID):
    """Returns the name of a character provided the character's ID."""
    namejson = request.urlopen("https://rickandmortyapi.com/api/character/"+ str(charID)).read()
    name = json.loads(namejson)['name']
    return name

def getCharCount(c):
    """Returns the current number of total characters from the Rick and Morty API."""
    countjson = request.urlopen("https://rickandmortyapi.com/api/character/").read()
    count = json.loads(countjson)['info']['count']
    return count

def addChar(c, userID, charID, charName, charImg):
    """Adds a new character for the provided userID into the characters table."""
    c.execute('INSERT INTO characters VALUES (?, ?, ?, ?)', (userID, charID, charName, charImg))

def switchChar(c, userID, charID, charName, charImg):
    """Switches the current character for the user with the provided userID in the users table."""
    c.execute('UPDATE users SET charID = ?, charName = ?, charImg = ? WHERE userID = ?', (charID, charName, charImg, userID))

def getStats(c, userID):
    """Returns a dictionary of all of a users stats provided their userID."""
    c.execute('SELECT xp, strength, intelligence, luck, gold FROM users WHERE userID = ?', (userID,))
    stats = c.fetchone()
    statDict = {'xp': stats[0], 'strength': stats[1], 'intelligence': stats[2], 'luck': stats[3], 'gold': stats[4]}
    return statDict

def resetStats(c, userID):
    c.execute('UPDATE users SET luck = 0, intelligence = 0, strength = 0 WHERE userID = ?', (userID, ))

def updateStats(c, userID, **stats):
    """Updates the stats of a user with the provided userID.
    If intelligence, strength, or luck exceed 100, they are capped at 100.

    Keyword arguments:
    intelligence, strength, luck, xp, or gold
    """
    currStats = getStats(c, userID)
    for key, value in stats.items():
        newValue = currStats[key] + value
        c.execute('UPDATE users SET {} = ? WHERE userID = ?'.format(key), (newValue, userID))
        newStats = getStats(c, userID)
        if newStats['intelligence'] > 100:
            c.execute('UPDATE users SET intelligence = 100 WHERE userID = ?', (userID, ))
        if newStats['strength'] > 100:
            c.execute('UPDATE users SET strength = 100 WHERE userID = ?', (userID, ))
        if newStats['luck'] > 100:
            c.execute('UPDATE users SET luck = 100 WHERE userID = ?', (userID, ))

def getCharacters(c, userID):
    """Returns a list of tuples of all of a user's characters' images and names provided their userID."""
    c.execute('SELECT charName, charImg, charID FROM characters WHERE userID = ?', (userID,))
    stats = c.fetchall()
    out = []
    for i in stats:
        out.append((i[0], i[1],i[2]))
    return out

def getHeroImage(c, charID):
    """Returns the image of a superhero from the SuperHero API provided their character ID."""
    req = request.Request('https://www.superheroapi.com/api/2503373653110667/'+str(charID), headers={'User-Agent': 'Mozilla/5.0'})
    imagejson = request.urlopen(req).read()
    if json.loads(imagejson)['response'] == 'error':
        return "";
    image = json.loads(imagejson)['image']['url']
    return image

def getHeroName(c, charID):
    """Returns the name of a superhero from the SuperHero API provided their character ID."""
    req = request.Request('https://www.superheroapi.com/api/2503373653110667/'+str(charID), headers={'User-Agent': 'Mozilla/5.0'})
    namejson = request.urlopen(req).read()
    if json.loads(namejson)['response'] == 'error':
        return "";
    name = json.loads(namejson)['name']
    return name

def quest(bank):
    """Makes dictionary from Open Trivia API"""
    q = request.urlopen("https://opentdb.com/api.php?amount=10&category=18&type=multiple").read()
    for i in range(5):
        count = json.loads(q)['results'][i]
        ans = [count['correct_answer']]
        bank[count['question']] = [*ans,*count['incorrect_answers']]
    return bank

def addQuestions(c):
    """Adds questions and choices into the database"""
    og = {}
    og = quest(og)
    for i in range(5):
        ques = list(og)[i]
        c.execute('INSERT INTO trivia VALUES (?, ?, ?, ?, ?, ?)', (i, ques, og[ques][0], og[ques][1], og[ques][2], og[ques][3]))

def getQuestion(c, i):
    """Get the question given the index"""
    return c.execute("SELECT questions, one, two, three, four FROM trivia WHERE number = ?", (i, )).fetchone()

def questBank(c):
    """Returns the dictionary from the stored information"""
    bank = []
    for i in range(5):
        bank.append(getQuestion(c, i))
    bankDic = {}
    for i in range(5):
        bankDic[bank[i][0]] = [bank[i][1], bank[i][2], bank[i][3], bank[i][4]]
    return bankDic

def answerBank(c):
    """Returns the dictionary with the question : [answer]"""
    bank = []
    for i in range(5):
        bank.append(getQuestion(c, i))
    bankDic = {}
    for i in range(5):
        bankDic[bank[i][0]] = [bank[i][1]]
    return bankDic
