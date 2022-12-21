from datetime import datetime
import numpy as np
import matplotlib.pyplot as pplt
import pandas as pd


key = "26f1cc6b039373fdded0b5855a718b65"


def get_weather(api_key=None) -> str:
    import json
    import requests
    city, lat, lon = "Saint Petersburg, RU", 59.57, 30.19

    # dt = 1671555323

    if api_key:
        result = dict()
        # 17.12.2022
        req = requests.get(
            f'http://api.openweathermap.org/data/2.5/'
            f'onecall/timemachine?lat={lat}&lon={lon}&dt={1671254117}&'
            f'appid={api_key}&lang=ru&units=metric')

        req_obj = json.loads(req.text)
        result['city'] = city
        measures = [{"dt": str(measure['dt']), "temp": str(measure['temp'])} for measure in req_obj["hourly"]]
        result['1671254117'] = measures


        # 18.12.2022
        req = requests.get(
            f'http://api.openweathermap.org/data/2.5/'
            f'onecall/timemachine?lat={lat}&lon={lon}&dt={1671340517}&'
            f'appid={api_key}&lang=ru&units=metric')

        req_obj = json.loads(req.text)
        measures = [{"dt": str(measure['dt']), "temp": str(measure['temp'])}for measure in req_obj["hourly"]]
        result['1671340517'] = measures

        # 19.12.2022
        req = requests.get(
            f'http://api.openweathermap.org/data/2.5/'
            f'onecall/timemachine?lat={lat}&lon={lon}&dt={1671426917}&'
            f'appid={api_key}&lang=ru&units=metric')

        req_obj = json.loads(req.text)
        measures = [{"dt": str(measure['dt']), "temp": str(measure['temp'])} for measure in req_obj["hourly"]]
        result['1671426917'] = measures


        # 20.12.2022
        req = requests.get(
            f'http://api.openweathermap.org/data/2.5/'
            f'onecall/timemachine?lat={lat}&lon={lon}&dt={1671513317}&'
            f'appid={api_key}&lang=ru&units=metric')

        req_obj = json.loads(req.text)
        measures = [{"dt": str(measure['dt']), "temp": str(measure['temp'])} for measure in req_obj["hourly"]]
        result['1671513317'] = measures

        # # 21.12.2022
        # req = requests.get(
        #     f'http://api.openweathermap.org/data/2.5/'
        #     f'onecall/timemachine?lat={lat}&lon={lon}&dt={1671599717}&'
        #     f'appid={api_key}&lang=ru&units=metric')
        #
        # req_obj = json.loads(req.text)
        # measures = [{"dt": str(measure['dt']), "temp": str(measure['temp'])} for measure in req_obj["hourly"]]
        # result['1671599717'] = measures

    json_obj = json.dumps(result, indent=4)

    with open('weather.json', 'w') as outfile:
        # json.dump(result, outfile, indent=4)
        outfile.write(json_obj)

    return json.dumps(result)


weather_data_json = get_weather(key)


def visualise_data(json_data=''):
    if json_data:
        data = pd.read_json(json_data)
        city_name = data['city']
        dates = [_d['dt'] for _d in data['1671254117'][:]]
        temps_17 = np.array([_t['temp'] for _t in data['1671254117'][:]])
        y1 = list(map(float, temps_17))
        pplt.figure(figsize=(12, 14))
        pplt.subplot(2, 1, 1)
        weather17 = pplt.scatter(dates, y1)
        pplt.title('Weather changes in Saint-Petersburg (17.12.22 - 21.12.22)')
        pplt.xlabel('Times[Last 5 days]');
        pplt.ylabel('Temperatures[Celsius]');
        dates_lbls = [datetime.utcfromtimestamp(int(_d['dt'])).strftime('%H:%M') for _d in data['1671254117'][:]]
        pplt.xticks(np.arange(24), dates_lbls, rotation=45, fontsize=8)

        temps_18 = np.array([_t['temp'] for _t in data["1671340517"][:]])
        y2 = list(map(float, temps_18))
        weather18 = pplt.scatter(dates, y2)

        temps_19 = np.array([_t['temp'] for _t in data["1671426917"][:]])
        y3 = list(map(float, temps_19))
        weather19 = pplt.scatter(dates, y3)

        temps_20 = np.array([_t['temp'] for _t in data["1671513317"][:]])
        y4 = list(map(float, temps_20))
        weather20 = pplt.scatter(dates, y4)

        pplt.legend((weather17, weather18, weather19, weather20),
                   ('17.12.2022', '18.12.2022', '19.12.2022', '20.12.2022'),
                   scatterpoints=1,
                   ncol=1,
                   fontsize=8,
                    bbox_to_anchor = (1 , 1))

        # temps_21 = np.array([_t['temp'] for _t in data["1671599717"][:]])
        # y5 = list(map(float, temps_21))
        # pplt.scatter(dates, y5)
        # pplt.show()

        dates, temps = ['17.12.2022', '18.12.2022', '19.12.2022', '20.12.2022'], [sum(y1)/len(temps_17),
                                                              sum(y2)/len(temps_18),
                                                              sum(y3)/len(temps_19),
                                                              sum(y4)/len(temps_20)]
        pplt.subplot(2, 1, 2)
        pplt.title('Average temperature (17.12.22 - 21.12.22)')
        pplt.xlabel('Date');
        pplt.ylabel('Temperatures[Celsius]');
        pplt.plot(dates, temps, linestyle='--', color='#808080')
        pplt.show()


visualise_data(weather_data_json)
