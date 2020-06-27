import urllib.request
import json
import datetime
import os


def fix(d, wrong, correct):
    d[correct] = d.pop(wrong)
    return d


def correct(d):
    d = fix(d, '4 Av', '4AV-9 ST')
    d = fix(d, 'Whitehall St', 'WHITEHALL S-FRY')
    d = fix(d, 'Essex St', 'DELANCEY/ESSEX')
    d = fix(d, 'Park Pl', 'PARK PLACE')
    d = fix(d, 'Beverley Rd', 'BEVERLEY ROAD')
    d = fix(d, 'Jay St - MetroTech', 'JAY ST-METROTEC')
    d = fix(d, 'Atlantic Av - Barclays Ctr', 'ATL AV-BARCLAY')
    d = fix(d, 'Roosevelt Island', 'ROOSEVELT ISLND')
    d = fix(d, 'Fort Hamilton Pkwy', 'FT HAMILTON PKY')
    d = fix(d, 'Coney Island - Stillwell Av', 'CONEY IS-STILLW')
    d = fix(d, 'W 8 St - NY Aquarium', 'W 8 ST-AQUARIUM')
    d = fix(d, 'Myrtle - Wyckoff Avs', 'MYRTLE-WYCKOFF')
    d = fix(d, 'Bushwick Av - Aberdeen St', 'BUSHWICK AV')
    d = fix(d, 'E 105 St', 'EAST 105 ST')
    d = fix(d, 'Canarsie - Rockaway Pkwy', 'CANARSIE-ROCKAW')
    d = fix(d, 'Howard Beach - JFK Airport', 'HOWARD BCH JFK')
    d = fix(d, '75 St', '75 ST-ELDERTS')
    d = fix(d, '85 St - Forest Pkwy', '85 ST-FOREST PK')
    d = fix(d, 'Knickerbocker Av', 'KNICKERBOCKER')
    d = fix(d, 'Seneca Av', 'SENECA AVE')
    d = fix(d, 'Forest Av', 'FOREST AVE')
    d = fix(d, '163 St - Amsterdam Av', '163 ST-AMSTERDM')
    d = fix(d, '81 St - Museum of Natural History', '81 ST-MUSEUM')
    d = fix(d, '59 St - Columbus Circle', '59 ST COLUMBUS')
    d = fix(d, '42 St - Port Authority Bus Terminal', '42 ST-PORT AUTH')
    d = fix(d, '34 St - Penn Station', '34 ST-PENN STA')
    d = fix(d, 'W 4 St', 'W 4 ST-WASH SQ')
    d = fix(d, 'World Trade Center', 'WORLD TRADE CTR')
    d = fix(d, 'Hoyt - Schermerhorn Sts', 'HOYT-SCHER')
    d = fix(d, 'Clinton - Washington Avs', 'CLINTON-WASH AV')
    d = fix(d, 'Kingston - Throop Avs', 'KINGSTON-THROOP')
    d = fix(d, 'Ozone Park - Lefferts Blvd', 'OZONE PK LEFFRT')
    d = fix(d, 'Aqueduct - N Conduit Av', 'AQUEDUCT N.COND')
    d = fix(d, 'Aqueduct Racetrack', 'AQUEDUCT RACETR')
    d = fix(d, 'Rockaway Park - Beach 116 St', 'ROCKAWAY PARK B')
    d = fix(d, 'Far Rockaway - Mott Av', 'FAR ROCKAWAY')
    d = fix(d, '161 St - Yankee Stadium', '161/YANKEE STAD')
    d = fix(d, 'Bedford Park Blvd', 'BEDFORD PK BLVD')
    d = fix(d, 'Norwood - 205 St', 'NORWOOD 205 ST')
    d = fix(d, 'Lexington Av/53 St', 'LEXINGTON AV/53')
    d = fix(d, 'Jackson Hts - Roosevelt Av', 'JKSN HT-ROOSVLT')
    d = fix(d, 'Grand Av - Newtown', 'GRAND-NEWTOWN')
    d = fix(d, 'Forest Hills - 71 Av', 'FOREST HILLS 71')
    d = fix(d, 'Kew Gardens - Union Tpke', 'KEW GARDENS')
    d = fix(d, 'Briarwood - Van Wyck Blvd', 'BRIARWOOD')
    d = fix(d, 'Jamaica - 179 St', 'JAMAICA 179 ST')
    d = fix(d, 'Myrtle - Willoughby Avs', 'MYRTLE-WILLOUGH')
    d = fix(d, 'Bedford - Nostrand Avs', 'BEDFORD-NOSTRAN')
    d = fix(d, '47-50 Sts - Rockefeller Ctr', '47-50 STS ROCK')
    d = fix(d, 'Broadway-Lafayette St', 'B\'WAY-LAFAYETTE')
    d = fix(d, 'Smith - 9 Sts', 'SMITH-9 ST')
    d = fix(d, '15 St - Prospect Park', '15 ST-PROSPECT')
    d = fix(d, 'Lexington Av/63 St', 'LEXINGTON AV/63')
    d = fix(d, '21 St - Queensbridge', '21 ST-QNSBRIDGE')
    d = fix(d, 'Jamaica - Van Wyck', 'JAMAICA VAN WK')
    d = fix(d, 'Sutphin Blvd - Archer Av - JFK Airport', 'SUTPHIN-ARCHER')
    d = fix(d, 'Jamaica Center - Parsons/Archer', 'JAMAICA CENTER')
    d = fix(d, 'Christopher St - Sheridan Sq', 'CHRISTOPHER ST')
    d = fix(d, '9 St', '9TH STREET')
    d = fix(d, 'WTC Cortlandt', 'WTC-CORTLANDT')
    d = fix(d, '66 St - Lincoln Center', '66 ST-LINCOLN')
    d = fix(d, '116 St - Columbia University', '116 ST-COLUMBIA')
    d = fix(d, '137 St - City College', '137 ST CITY COL')
    d = fix(d, 'Marble Hill - 225 St', 'MARBLE HILL-225')
    d = fix(d, 'Van Cortlandt Park - 242 St', 'V.CORTLANDT PK')
    d = fix(d, 'Brooklyn Bridge - City Hall', 'BROOKLYN BRIDGE')
    d = fix(d, 'Grand Central - 42 St', 'GRD CNTRL-42 ST')
    d = fix(d, '68 St - Hunter College', '68ST-HUNTER CO')
    d = fix(d, '138 St - Grand Concourse', '138/GRAND CONC')
    d = fix(d, '149 St - Grand Concourse', '149/GRAND CONC')
    d = fix(d, 'Central Park North (110 St)', 'CENTRAL PK N110')
    d = fix(d, 'Harlem - 148 St', 'HARLEM 148 ST')
    d = fix(d, 'West Farms Sq - E Tremont Av', 'WEST FARMS SQ')
    d = fix(d, 'Wakefield - 241 St', 'WAKEFIELD/241')
    d = fix(d, '3 Av - 138 St', '3 AV 138 ST')
    d = fix(d, 'E 143 St - St Mary\'s St', 'E 143/ST MARY\'S')
    d = fix(d, 'Morrison Av- Sound View', 'MORISN AV/SNDVW')
    d = fix(d, 'Westchester Sq - E Tremont Av', 'WESTCHESTER SQ')
    d = fix(d, '5 Av', '5 AVE')
    d = fix(d, 'Vernon Blvd - Jackson Av', 'VERNON-JACKSON')
    d = fix(d, 'Hunters Point Av', 'HUNTERS PT AV')
    d = fix(d, 'Queensboro Plaza', 'QUEENSBORO PLZ')
    d = fix(d, 'Astoria - Ditmars Blvd', 'ASTORIA DITMARS')
    d = fix(d, '40 St', '40 ST LOWERY ST')
    d = fix(d, 'Woodside - 61 St', '61 ST WOODSIDE')
    d = fix(d, '82 St - Jackson Hts', '82 ST-JACKSON H')
    d = fix(d, '90 St - Elmhurst Av', '90 ST-ELMHURST')
    d = fix(d, '103 St - Corona Plaza', '103 ST-CORONA')
    d = fix(d, 'Mets - Willets Point', 'METS-WILLETS PT')
    d = fix(d, 'Flushing - Main St', 'FLUSHING-MAIN')
    d = fix(d, 'Grand Army Plaza', 'GRAND ARMY PLAZ')
    d = fix(d, 'Eastern Pkwy - Brooklyn Museum', 'EASTN PKWY-MUSM')
    d = fix(d, 'Crown Hts - Utica Av', 'CROWN HTS-UTICA')
    d = fix(d, 'Sutter Av - Rutland Rd', 'SUTTER AV-RUTLD')
    d = fix(d, 'Flatbush Av - Brooklyn College', 'FLATBUSH AV-B.C')
    d = fix(d, 'Eastchester - Dyre Av', 'EASTCHSTER/DYRE')
    d = fix(d, 'St George', 'ST. GEORGE')
    d = fix(d, 'New Lots Av', 'NEW LOTS AV')
    for stop in list(d.keys()):
        name = stop
        if ' - ' in name:
            name = name.replace(' - ', '-')
        name = name.upper()
        d[name] = d.pop(stop)
    return d


def mta_corrections(file):
    '''
    Set up dictionary for name corrections and borough match
    '''
    json_file = open(file)
    mta_json = json.load(json_file)

    mta_json = mta_json['objects']['subway_stops']['geometries']
    mta_info = dict()

    for stop in mta_json:
        borough = stop['properties']['namelsad']
        name = stop['properties']['stop_name']
        dict_s = mta_info[name] = dict()
        dict_s['borough'] = borough
        dict_s['name'] = name

    return mta_info


def merge_stations(stations, s0, s1):

    d0 = stations[s0]
    d1 = stations[s1]

    for date in list(d0.keys()):
        if date in d1:
            d0[date]['enter'] += d1[date]['enter']
            d0[date]['exit'] += d1[date]['exit']

    stations.pop(s1)

    return stations


def send_request(date):

    req = urllib.request.Request(BASE_URL + date + TXT)
    req = urllib.request.urlopen(req)
    print(BASE_URL + date + TXT, req.status)
    res = req.read().decode('utf8').strip('\n').split('\n')

    # res = open('turnstile_200425.txt').read().strip('\n').split('\n')

    res = [line.rstrip() for line in res][1:]

    stations = dict()

    for i in range(0, len(res)):
        event = res[i].split(',')

        date = [int(t) for t in event[6].split('/')]
        date = datetime.datetime(date[2], date[0], date[1])

        name = event[3]
        control, turnstile = event[0] + event[1], event[2]
        _enter, _exit = int(event[9]), int(event[10])

        if not name in stations:
            stations[name] = dict()

        _station = stations[name]
        if not date in _station:
            _station[date] = dict()

        _date = _station[date]
        if not control in _date:
            _date[control] = dict()

        _control = _date[control]
        if not turnstile in _control:
            _control[turnstile] = dict()
            _turnstile = _control[turnstile]

            _turnstile['enter'], _turnstile['exit'] = 0, 0

            '''
                Handle putting data into the previous day for midnight datapoint
                If the turnstile is not yet in the day, we know that the current timestamp
                is at midnight. Knowing this, we can go back in time one day and check to
                see if the current turnstile is also represented on that day. If it is, then
                we add the last 4 hours of data to that day's data.
            '''
            d_date = datetime.timedelta(days=1)
            prev = date - d_date
            if prev in _station and control in _station[prev] and turnstile in _station[prev][control]:
                prev = _station[prev][control][turnstile]
                d_enter = _enter - prev['c_enter']
                d_exit = _exit - prev['c_exit']
                if _enter > prev['c_enter'] and d_enter < 100000:
                    prev['enter'] += d_enter
                if _exit > prev['c_exit'] and d_exit < 100000:
                    prev['exit'] += d_exit

        else:
            _turnstile = _control[turnstile]

            '''
                Increment the amount of change in entries and exits
            '''
            d_enter = _enter - _turnstile['c_enter']
            d_exit = _exit - _turnstile['c_exit']
            if(_enter > _turnstile['c_enter'] and d_enter < 100000):
                _turnstile['enter'] += d_enter
            if(_exit > _turnstile['c_exit'] and d_exit < 100000):
                _turnstile['exit'] += d_exit

        _turnstile['c_enter'], _turnstile['c_exit'] = _enter, _exit

    '''
        Remove stations witohut proper location data
    '''
    stations.pop('NEWARK BM BW')
    stations.pop('NEWARK C')
    stations.pop('NEWARK HM HE')
    stations.pop('PATH WTC 2')
    stations.pop('PATH NEW WTC')
    stations.pop('NEWARK HW BMEBE')
    stations.pop('HARRISON')
    stations.pop('JOURNAL SQUARE')
    stations.pop('GROVE STREET')
    stations.pop('EXCHANGE PLACE')
    stations.pop('PAVONIA/NEWPORT')
    stations.pop('CITY / BUS')
    stations.pop('LACKAWANNA')
    stations.pop('THIRTY ST')
    stations.pop('RIT-MANHATTAN')
    stations.pop('RIT-ROOSEVELT')
    stations.pop('34 ST-HUDSON YD')

    '''
        Compress turnstile data into station data
    '''
    for station in stations.keys():
        for date in stations[station]:
            _date = stations[station][date]
            day_enter, day_exit = 0, 0
            keys = list(_date.keys())
            for control in keys:
                turnstiles = list(_date[control].keys())
                for turnstile in turnstiles:
                    day_enter += _date[control][turnstile]['enter']
                    day_exit += _date[control][turnstile]['exit']
                    _date[control].pop(turnstile)
                _date.pop(control)
            _date['enter'] = day_enter
            _date['exit'] = day_exit

    '''
        Merge stations with similar names
    '''
    stations = merge_stations(stations, 'NEW LOTS AV', 'NEW LOTS')
    stations = merge_stations(stations, '33 ST', '33 ST-RAWSON ST')
    stations = merge_stations(stations, '46 ST', '46 ST BLISS ST')
    stations = merge_stations(stations, '14 ST', '14TH STREET')
    stations = merge_stations(stations, '23 ST', 'TWENTY THIRD ST')
    stations = merge_stations(stations, '33 ST', 'THIRTY THIRD ST')
    stations = merge_stations(stations, '72 ST', '72 ST-2 AVE')
    stations = merge_stations(stations, '86 ST', '86 ST-2 AVE')
    stations = merge_stations(stations, '96 ST', '96 ST-2 AVE')
    stations = merge_stations(stations, 'COURT SQ', 'COURT SQ-23 ST')
    stations = merge_stations(stations, 'VAN SICLEN AV', 'VAN SICLEN AVE')
    stations = merge_stations(stations, '4AV-9 ST', '4 AV-9 ST')
    stations = merge_stations(stations, 'HOWARD BCH JFK', 'JFK JAMAICA CT1')

    return stations


def process_request(week_data, f):
    for station in week_data.keys():
        if not station in name_dict:
            continue

        name = name_dict[station]['name']
        borough = name_dict[station]['borough']

        data = week_data[station]
        for _date in data.keys():
            day = _date.date().isoformat()
            _enter = data[_date]['enter']
            _exit = data[_date]['exit']
            f.write(f'{name},{day},{borough},{_enter},{_exit}\n')


def correct_date(date):
    # e.g. ['2020', '04', '25']
    date_list = date.date().isoformat().split('-')

    return date_list[0][2:] + date_list[1] + date_list[2]


BASE_URL, TXT = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_', '.txt'

json_file = os.path.dirname(os.path.abspath(
    __file__)) + '/../../static/json/subway_stops.json'

name_dict = correct(mta_corrections(json_file))
