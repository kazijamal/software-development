'''
TwoFortyNine -- Kazi Jamal, Eric Lau, and Raymond Lee
SoftDev1 pd9
P04 -- Let the Data Speak
2020-05-11
'''

from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
import urllib.request
from covid import Covid
covid = Covid()

app = Flask(__name__)
app.secret_key = os.urandom(32)

# DASHBOARD
@app.route('/')
def root():
    data = covid.get_status_by_country_name("us")
    return render_template('dashboard.html', confirmed="{:,}".format(data['confirmed']), active="{:,}".format(data['active']), recovered="{:,}".format(data['recovered']), deaths="{:,}".format(data['deaths']))

# ABOUT
@app.route('/about')
def about():
    return render_template('about.html')

# SENTIMENT ANALYSIS
@app.route('/sentiment')
def sentiment():
    return render_template('sentiment/sentiment.html')


@app.route('/sentiment/publicmedia')
def publicmedia():
    return render_template('sentiment/publicmedia.html')


@app.route('/sentiment/trumptweets')
def trumptweets():
    return render_template('sentiment/trumptweets.html')


# TRANSPORTATION
@app.route('/transportation')
def transportation():
    return render_template('transportation/transportation.html')


@app.route('/transportation/nycpublic')
def nycpublic():
    return render_template('transportation/nycpublic.html')

# NUMBERS
@app.route('/numbers')
def numbers():
    return render_template('numbers.html')


# DATA TRANSFER
def transfer_csv(file_name):
    csv_file = os.path.dirname(
        os.path.abspath(__file__)) + '/static/data/' + file_name
    return open(csv_file).read()


def request_csv(url):
    req = urllib.request.Request(url)
    req = urllib.request.urlopen(req)
    return req.read().decode('utf8')


@app.route('/data/dashboard/us')
def dashboard_us_transfer():
    '''
    Retrieve US CSV file from the official NY Times COVID-19 repository
    '''
    return request_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')


@app.route('/data/dashboard/states')
def dashboard_states_transfer():
    '''
    Retrieve US states CSV file from the official NY Times COVID-19 repository
    '''
    return request_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')


@app.route('/data/transportation/mta')
def turnstile_transfer():
    '''
    Retrieve the CSV file containing MTA turnstile data
    '''
    return transfer_csv('mta_turnstile.csv')


@app.route('/data/transportation/covid/<file_type>')
def covid_transfer(file_type):
    '''
    Retrieve CSV files from the official NYC Health GitHub repository
    '''
    return request_csv(f'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/{file_type}.csv')


@app.route("/data/sentiment/publicmedia")
def publicMediaData():
    return transfer_csv('num-articles-per-day.csv')


@app.route("/data/sentiment/newsdomainsubjectivities")
def newsDomainSubjectivities():
    return transfer_csv('news-domains-on-average-subjectivity-ranges.csv')


@app.route("/data/sentiment/trumptweetspolarities")
def trumpTweetsPolarities():
    return transfer_csv('trump-tweets-on-polarity-range.csv')


@app.route("/data/sentiment/trumptweetspolaritiesonranges")
def trumpTweetsPolaritiesOnRanges():
    return transfer_csv('trump-tweets-on-polarity-ranges.csv')

@app.route("/data/sentiment/namedentitiesfrequencies")
def namedEntitiesFrequencies():
    return transfer_csv('named-entities-frequencies.csv')


if __name__ == '__main__':
    app.debug = True
    app.run()
