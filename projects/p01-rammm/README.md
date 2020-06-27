# Rick and Morty's Minigame Madness by Team qafee 
## Roster and Role:
- Kevin Cai (Project Manager, Director of Authentication)
- Tammy Chen (Intelligence Trivia Agent)
- Kazi Jamal (Lucky Lotto Manager)
- Taejoon Kim (Strength Arena Builder)

## What our website does:
- The overall goal of the project is to create a fun and addictive game for users to play while increasing their stats and building a collection of characters from the television show Rick and Morty. There are multiple minigames to increase stats, including:
  - Intelligence Trivia
  - Lucky Lotto
  - Strength Arena

## APIs utilized:
[The Rick and Morty API](https://docs.google.com/document/d/1oK0klhp__LHP9kxb3D70cbbI46i1mMnmDMI4y1XS3B4/)
  - We use this API to get the images and names of our characters for our Dashboard page and Lucky Lotto minigame.

[The Open Trivia API](https://docs.google.com/document/d/1yp2nicOExDYlrEfdvqspD17Kz5c-xMSWHudfmNjJgQ4/)
  - We use this API to get trivia questions for our Intelligence Trivia minigame.
  
[The SuperHero API](https://docs.google.com/document/d/1C6-MBqUFIsfcOkAEePMlcC7ywP8SoCNd4RhlKG4zMjk/)
  - We use this API to get the images and names of enemy characters for our Strength Arena minigame.
  
## How to Run the Project:
- We are assuming that the user has installed Python3 and pip in their environment
- If not, install Python3 from https://www.python.org/downloads/
- pip comes installed with Python by default

#### To clone the project: 
```bash
$ git clone git@github.com:kevin16777216/qafee__caiK-chenT-jamalK-kimT.git
```

#### To create a virtual environment and install all packages in the virtual environment:
```bash
$ python3 -m venv <name of virtual environment>
$ . ~/<name of virtual environment>/bin/activate  
(venv)$ cd <name of cloned directory>
(venv)/<name of cloned directory>$ pip3 install -r doc/requirements.txt
```

#### To run the project: 
Note: No API keys are needed for this project to run, so this should run without any issues.
```bash
$ cd <name of cloned directory>
/<name of cloned directory>$ python3 app.py 
```

View the webpage by opening a web browser and visiting: http://127.0.0.1:5000/

---
© Copyright 2019 Team qafee -- Kevin Cai, Tammy Chen, Kazi Jamal & Taejoon Kim
