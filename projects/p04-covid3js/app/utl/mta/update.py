import time
import os
import datetime

from process import send_request, process_request, correct_date

start = time.time()

filepath = os.path.dirname(os.path.abspath(__file__))

f = open(f'{filepath}/../../static/data/mta_turnstile.csv', 'a')

date = datetime.datetime(2020, 6, 20)

url_date = correct_date(date)

week_data = send_request(url_date)

process_request(week_data, f)

f.close()
