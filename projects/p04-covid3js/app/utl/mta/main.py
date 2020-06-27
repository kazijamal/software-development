import datetime
import time
import os

from process import send_request, process_request, correct_date

'''
This file makes HTTP requests to the data files located here: http://web.mta.info/developers/turnstile.html
MTA turnstile data is reported on every Saturday.

The data is organized in the follow CSV manner:

C/A,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS

C/A and UNIT represent the control areas the turnstiles are under
SCP represents the turnstile ID
STATION is the name of the station
LINENAME contains all of the lines that serve the STATION
DIVISON represents the outdated divisions in the MTA from the 20th century
DATE represents the day that the data is from
TIME represents the timestamp during which the audit event occured
ENTRIES and EXITS represent the cumulative number of entries and exits at a turnstile at TIMESTAMP on DATE

Note that the timestamps are taken every four hours, starting at midnight. The entry and exit data taken from
the timestamp represent the number of entries and exits in the four hours leading up to the audit event.
For this reason, we need to make sure that the first datapoint from the next day is counted in the previous day

For example:

A002,R051,02-00-00,59 ST,NQR456W,BMT,04/19/2020,00:00:00,REGULAR,0007414835,0002517678

is a datapoint from the 19th of April, 2020 but it contains data about the 18th of April. Therefore, we need to
make sure it is counted in the correct date.

Note that some stop stations do repeat their names, and for this reason, we need to use the control values as a
pseudo-id. Note that turnstile identifiers repeat for different stations so they do not serve as a good id.
Note that the entries and exits are cumulative and thus we need to track daily ridership ourselves.

Because the data can be unexpected and there is simply too much data to go over with a fine-tooth comb, we cannot
guarantee that our daily ridership is generating correct data.

What does this script do?
We are querying for all ridership data reported since January 05, 2019 to present. We cannot download all of the files
in any feasible way because each file is 26 MB. There are 69 weeks worth of data, putting the total at 1.7 GB.

In each query, we go through every line of data to find the total number of entries and exits in every turnstile
at every station every day. After we retrieve data for each turnstile, we then compress the data to represent total
daily entries and exits per station.

After getting the data for each day, we then have to match the names from our generated dictionary to the names from
another official MTA file which contains location and borough data. After that, we write the data to a file in
CSV format. This new file will be returned as text in a Flask route, which will be queried by our frontend JavaScript.

Unsurprisingly, the turnstile data the MTA provides is not well organized or reliable enough to simply read from, so
there are a number of checks to ensure that the numbers aren't wonky.
'''


start = time.time()

date = datetime.datetime(2019, 1, 5)
last_date = datetime.datetime(2020, 4, 25)

f = open('../../static/data/mta_turnstile.csv', 'w')
f.write('station,date,borough,enter,exit\n')

while(date <= last_date):
    # e.g. '200425'
    url_date = correct_date(date)

    week_data = send_request(url_date)

    process_request(week_data, f)

    date += datetime.timedelta(days=7)

f.close()

print(time.time() - start)
