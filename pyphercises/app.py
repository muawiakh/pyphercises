import requests
import json
import os
import datetime
from flask import Flask, jsonify, request, redirect
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

from pyphercises import version, utils, constants


app = Flask(__name__)
api = Api(app, prefix="/api/{}".format(version._api_version_))


class Info(Resource):
    def get(self):
        resp_dict = {
            "name": "Basic weather app",
            "description": "First cut weather app",
            "weather": "/api/{}/weather".format(version._api_version_),
            "version": "/api/{}/version".format(version._api_version_),
        }
        return jsonify(resp_dict)


class Weather(Resource):
    def get(self):
        APP_ID = os.getenv("WEATHER_APP_ID", None)

        req_parser = RequestParser(bundle_errors=True)
        req_parser.add_argument(
            "city", type=str, default=constants.DEFAULT_CITY, help="Name has to be valid string")
        req_parser.add_argument(
            "country", type=str, default=constants.DEFAULT_COUNTRY, help="Name has to be valid string")
        req_parser.add_argument(
            "lon", type=str, default=constants.DEFAULT_LONGITUDE, help="Name has to be valid string")
        req_parser.add_argument(
            "lat", type=str, default=constants.DEFAULT_LONGITUDE, help="Name has to be valid string")
        req_parser.add_argument(
            "units", type=str, default="metric", help="Name has to be valid string")

        args = req_parser.parse_args()
        if args.units not in constants.POSSIBLE_UNITS:
            print(args.units)
            return json.dumps({'error': 'Invalid unit parameter'}), 400

        r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={},{}&lat={}&lon={}&units={}&appid={}'.format(
            args.city, args.country, args.lat, args.lon, args.units, APP_ID))
        if r.status_code != 200:
            return jsonify(json.loads(r.text))
        forecast_resp = json.loads(r.content)
        return jsonify(utils.create_date_map(forecast_resp))


class VersionInfo(Resource):
    def get(self):
        resp_dict = {
            "version": version._app_version_,
        }
        return jsonify(resp_dict)


api.add_resource(Info, "/")
api.add_resource(Weather, "/weather")
api.add_resource(VersionInfo, "/version")


@app.route("/")
def index():
    return redirect('/api/{}'.format(version._api_version_))

@app.errorhandler(404)
def not_found(e):
    return 'There are no more APIs', 404
