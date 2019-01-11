from flask import Flask, jsonify, request
import version
import requests
import json
import datetime
app = Flask(__name__)


@app.route('/')
def root_endpoint():
    resp_dict = {
        "name": "Basic weather app",
        "description": "First cut weather app",
        "version": version.__version__,
    }
    return jsonify(resp_dict)


@app.route('/weather')
def weather_endpoint():
    DATE_MAP = {}
    POSSIBLE_UNITS = ["metric", "imperial"]
    APP_ID = "4055b8a5b1585d71d81af50461cd5257"
    city_name = request.args.get('city', 'Berlin')
    country_name = request.args.get('country', 'de')
    longitude = request.args.get('lon', None)
    latitude = request.args.get('lat', None)
    unit = request.args.get('units', 'metric')
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={},{}&lat={}&lon={}&units={}&appid={}'.format(city_name, country_name, longitude, latitude, unit, APP_ID))
    forecast_resp = json.loads(r.content)

    # Needed because the API returns 5 day forecast
    start_forecast_date = datetime.datetime.now()
    end_forecast_date = start_forecast_date + datetime.timedelta(days=2)
    interation_step = datetime.timedelta(days=1)
    while start_forecast_date <= end_forecast_date:
        start_forecast_date_fmt = start_forecast_date.strftime("%Y-%m-%d")      
        DATE_MAP.setdefault(start_forecast_date_fmt, {})
        for i in range(len(forecast_resp["list"])):
            if start_forecast_date_fmt in forecast_resp["list"][i]["dt_txt"]:
                DATE_MAP[start_forecast_date_fmt].setdefault("temperature", []).append(forecast_resp["list"][i]["main"]["temp"])
                DATE_MAP[start_forecast_date_fmt].setdefault("humidity", []).append(forecast_resp["list"][i]["main"]["humidity"])
                DATE_MAP[start_forecast_date_fmt].setdefault("wind", []).append(forecast_resp["list"][i]["wind"]["speed"])
                if forecast_resp["list"][i]["rain"]:
                    DATE_MAP[start_forecast_date_fmt].setdefault("rain", []).append(forecast_resp["list"][i]["rain"]["3h"])
                if forecast_resp["list"][i]["snow"]:
                    DATE_MAP[start_forecast_date_fmt].setdefault("snow", []).append(forecast_resp["list"][i]["snow"]["3h"])
        start_forecast_date += interation_step


    resp_dict = {}
    # Calculating averages
    for key, value in DATE_MAP.items():
        resp_dict.setdefault(key, {})
        resp_dict[key]["temperature"] = round(sum(DATE_MAP[key]["temperature"]) / len(DATE_MAP[key]["temperature"]), 2)
        resp_dict[key]["humidity"] = round(sum(DATE_MAP[key]["humidity"]) / len(DATE_MAP[key]["humidity"]), 2)
        resp_dict[key]["wind"] = round(sum(DATE_MAP[key]["wind"]) / len(DATE_MAP[key]["wind"]), 2)
        if "rain" in DATE_MAP[key]:
            resp_dict[key].setdefault("precipitation", {})
            resp_dict[key]["precipitation"]["rain"] = round(sum(DATE_MAP[key]["rain"]) / len(DATE_MAP[key]["rain"]), 2)
        if "snow" in DATE_MAP[key]:
            resp_dict[key].setdefault("precipitation", {})
            resp_dict[key]["precipitation"]["snow"] = round(sum(DATE_MAP[key]["snow"]) / len(DATE_MAP[key]["snow"]), 2)

    print(resp_dict)

    resp_dict["city"] = forecast_resp["city"]["name"]
    resp_dict["country"] = forecast_resp["city"]["country"]
    resp_dict["coord"] = {}
    resp_dict["coord"]["lat"] = forecast_resp["city"]["coord"]["lat"]
    resp_dict["coord"]["lon"] = forecast_resp["city"]["coord"]["lon"]
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
