from flask import Flask, jsonify, request
import version
import requests
import json
import datetime
app = Flask(__name__)


POSSIBLE_UNITS = ["metric", "imperial"]
DEFAULT_CITY = "berlin"
DEFAULT_COUNTRY = "de"
DEFAULT_LONGITUDE = None
DEFAULT_LATITUDE = None
FORECAST_DELTA = 2

def calculate_list_average(data):
    return round(sum(data) / len(data), 2)

def create_date_map(res):
    DATE_MAP = {}
    # Needed because the API returns 5 day forecast
    start_forecast_date = datetime.datetime.now()
    end_forecast_date = start_forecast_date + datetime.timedelta(days=FORECAST_DELTA)
    interation_step = datetime.timedelta(days=1)
    while start_forecast_date <= end_forecast_date:
        start_forecast_date_fmt = start_forecast_date.strftime("%Y-%m-%d")      
        DATE_MAP.setdefault(start_forecast_date_fmt, {})
        for i in range(len(res["list"])):
            if start_forecast_date_fmt in res["list"][i]["dt_txt"]:
                DATE_MAP[start_forecast_date_fmt].setdefault("temperature", []).append(res["list"][i]["main"]["temp"])
                DATE_MAP[start_forecast_date_fmt].setdefault("humidity", []).append(res["list"][i]["main"]["humidity"])
                DATE_MAP[start_forecast_date_fmt].setdefault("wind", []).append(res["list"][i]["wind"]["speed"])
                if "rain" in res["list"][i] and res["list"][i]["rain"]:
                    DATE_MAP[start_forecast_date_fmt].setdefault("rain", []).append(res["list"][i]["rain"]["3h"])
                if "snow" in res["list"][i] and res["list"][i]["snow"]:
                    DATE_MAP[start_forecast_date_fmt].setdefault("snow", []).append(res["list"][i]["snow"]["3h"])
        start_forecast_date += interation_step

    return create_resp_dict(DATE_MAP, res)


def create_resp_dict(dmap, res):
    resp_dict = {}
    # Calculating averages
    for key, value in dmap.items():
        resp_dict.setdefault(key, {})
        resp_dict[key]["temperature"] = calculate_list_average(dmap[key]["temperature"])
        resp_dict[key]["humidity"] = calculate_list_average(dmap[key]["humidity"])
        resp_dict[key]["wind"] = calculate_list_average(dmap[key]["wind"])
        if "rain" in dmap[key]:
            resp_dict[key].setdefault("precipitation", {})
            resp_dict[key]["precipitation"]["rain"] = calculate_list_average(dmap[key]["rain"])
        if "snow" in dmap[key]:
            resp_dict[key].setdefault("precipitation", {})
            resp_dict[key]["precipitation"]["snow"] = calculate_list_average(dmap[key]["snow"])
    resp_dict["city"] = res["city"]["name"]
    resp_dict["country"] = res["city"]["country"]
    resp_dict["coord"] = {}
    resp_dict["coord"]["lat"] = res["city"]["coord"]["lat"]
    resp_dict["coord"]["lon"] = res["city"]["coord"]["lon"]
    return resp_dict



@app.route('/')
def root_endpoint():
    resp_dict = {
        "name": "Basic weather app",
        "description": "First cut weather app",
        "weather_endpoint": "/weather", 
        "version_endpoint": "/version",
    }
    return jsonify(resp_dict)


@app.route('/weather')
def weather_endpoint():
    APP_ID = "4055b8a5b1585d71d81af50461cd5257"
    city_name = request.args.get('city', DEFAULT_CITY)
    country_name = request.args.get('country', DEFAULT_COUNTRY)
    longitude = request.args.get('lon', DEFAULT_LONGITUDE)
    latitude = request.args.get('lat', DEFAULT_LATITUDE)
    unit = request.args.get('units', 'metric')
    if unit not in POSSIBLE_UNITS:
        return jsonify({'error': 'Invalid unit parameter'}, 400)
    print('http://api.openweathermap.org/data/2.5/forecast?q={},{}&lat={}&lon={}&units={}&appid={}'.format(city_name, country_name, latitude, longitude, unit, APP_ID))
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={},{}&lat={}&lon={}&units={}&appid={}'.format(city_name, country_name, latitude, longitude, unit, APP_ID))
    if r.status_code != 200:
        return jsonify(json.loads(r.text))
    forecast_resp = json.loads(r.content)
    resp_dict = create_date_map(forecast_resp)
    return jsonify(resp_dict)


@app.route('/version')
def version_endpoint():
    resp_dict = {
        "version": version.__version__,
    }
    return jsonify(resp_dict)

@app.errorhandler(404)
def not_found(e):
    return 'There are no more APIs', 404

if __name__ == "__main__":
    app.run(host="0.0.0.0")
