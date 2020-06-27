# Oikos by theyputhiminapeach
## Roster and Role:
- Jude Rizzo: Project Manager, Director of Authentication 
- Kevin Cai: Groups and Post Builder
- Kazi Jamal: Messages and Friend Manager
- Ahmed Sultan: Dashboard and Feed Developer

## Project Description
Our project aims to create a Stuyvesant-centered social media web application, replacing previous means of communication (i.e. Facebook) and providing an experience catered to Stuyvesant students.

## APIs Utilized
- MetaWeather API: https://docs.google.com/document/d/18uyXB5XPFQoGFJpoa2yQvRPhevc3HaBU4kO-OYN-ieY/edit
  - Provides the weather for the next five days for locations using their woeid
  - Used to display weather for the current date in New York City on the dashboard page
- News API: https://docs.google.com/document/d/1sLb7KpsBcx1_dCzuLicWvnSaQJRepZ1YM12tMxbj2RA/edit
  - Provides access to live data on trending and articles on the web from various news sources
  - Used to display three trending news articles with images linking to the original source on the dashboard page
  
## Video Demo
[video demo here](https://youtu.be/iXZoJQ586lI)

## Launch Codes
### News API
1) Visit https://newsapi.org/
2) Press the Get API Key button
3) Fill out and submit information required to register for an API key
4) Once registration is complete copy the provided API key
5) Open the `apikeys.json` file located in the `utl` folder of our project
6) Replace `YOUR_API_KEY_HERE` for the `NEWS_API_KEY` with the API key you copied earlier

## How to Run the Project:
- We are assuming that the user has installed Python3 and pip in their environment
- If not, install Python3 from https://www.python.org/downloads/
- pip comes installed with Python by default

#### To clone the project: 
```bash
$ git clone git@github.com:juderzzo/inpeach.git
```

#### To create a virtual environment and install all packages in the virtual environment:
```bash
$ python3 -m venv <name of virtual environment>
$ . ~/<name of virtual environment>/bin/activate  
(venv)$ cd <name of cloned directory>
(venv)/<name of cloned directory>$ pip3 install -r doc/requirements.txt
```

#### To run the project: 
```bash
$ cd <name of cloned directory>
/<name of cloned directory>$ python3 app.py 
```

View the webpage by opening a web browser and visiting: http://127.0.0.1:5000/

---
© Copyright 2020 Team theyputhiminapeach -- Jude Rizzo, Kevin Cai, Kazi Jamal, Ahmed Sultan
