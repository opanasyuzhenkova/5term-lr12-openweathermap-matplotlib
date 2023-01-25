import datetime
import time
import numpy as np
import matplotlib.pyplot as pplt
import pandas as pd
import json
import requests

key = "26f1cc6b039373fdded0b5855a718b65"
def get_data(i):
    today = datetime.datetime.today()
    one_day = datetime.timedelta(days=i)
    date = today - one_day
    unix_date = '%.0f' % time.mktime(date.timetuple())
    return unix_date


def get_weather(api_key=None) -> str:

    city, lat, lon = "Saint Petersburg, RU", 59.57, 30.19
    result = dict()
    for i in range(5, 0, -1):
        if api_key:
            req = requests.get(
                f'http://api.openweathermap.org/data/2.5/'
                f'onecall/timemachine?lat={lat}&lon={lon}&dt={str(get_data(i))}&'
                f'appid={api_key}&lang=ru&units=metric')
            req_obj = json.loads(req.text)
            measures = [{"dt": str(measure['dt']), "temp": str(measure['temp'])} for measure in req_obj['hourly']]
            result[str(get_data(i))] = measures
    json_obj = json.dumps(result, indent=4)
    with open('weather.json', 'w') as outfile:
        outfile.write(json_obj)
    return json_obj


weather_data_json = get_weather(key)


def visualise_data(json_data=''):
    if json_data:
        data = pd.read_json(json_data)
        pplt.figure(figsize=(12, 14))
        pplt.subplot(2, 1, 1)
        pplt.title('Weather changes in Saint-Petersburg')
        pplt.xlabel('Time')
        pplt.ylabel('Temperatures[Celsius]')
        dates_lbls = [datetime.datetime.utcfromtimestamp(int(_d['dt'])).strftime('%H:%M') for _d in data.iloc[:, 0]][:]
        pplt.xticks(np.arange(24), dates_lbls, rotation=45, fontsize=8)
        dates = [_d['dt'] for _d in data.iloc[:, 0]][:]
        av_temps = []
        for i in range(0, 5):
            temp = np.array([_t['temp'] for _t in data.iloc[:, i]][:])
            y = list(map(float, temp))
            pplt.scatter(dates, y)
            av_temps.append(sum(y)/len(temp))
        pplt.legend([column.strftime('%d.%m.%Y') for column in data])

        dates, temps = [[column.strftime('%d.%m.%Y') for column in data], av_temps]
        pplt.subplot(2, 1, 2)
        pplt.title('Average temperature last 5 days')
        pplt.xlabel('Date')
        pplt.ylabel('Temperatures[Celsius]')
        pplt.plot(dates, temps, linestyle='--', color='#808080')
        pplt.show()


visualise_data(weather_data_json)