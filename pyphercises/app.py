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
        """API endpoint to get info about the app

        Return:
            A JSON containing the info
        """
        app.logger.info("GET /api/v1 called")
        resp_dict = {
            "name": "Basic weather app",
            "description": "First cut weather app",
            "weather": "/api/{}/weather".format(version._api_version_),
            "version": "/api/{}/version".format(version._api_version_),
        }
        return jsonify(resp_dict)


class Weather(Resource):
    def get(self):
        """API endpoint to get weather forecast for today
        and the next two days.

        Return:
            A JSON containing the weather data.
        """
        app.logger.info("GET /api/v1/weather called")
        APP_ID = os.getenv("WEATHER_APP_ID", None)

        req_parser = RequestParser(bundle_errors=True)
        req_parser.add_argument(
            "city", type=str, default="", help="Name has to be valid string")
        req_parser.add_argument(
            "country", type=str, default="", help="Name has to be valid string")
        req_parser.add_argument(
            "lon", type=str, default="", help="Name has to be valid string")
        req_parser.add_argument(
            "lat", type=str, default="", help="Name has to be valid string")
        req_parser.add_argument(
            "units", type=str, default="metric", help="Name has to be valid string")

        args = req_parser.parse_args()
        if args.units not in constants.POSSIBLE_UNITS:
            return {'error': 'Invalid unit parameter, choose: [metric, imperial]'}, 400

        if (args.city and not args.country) or (args.country and not args.city):
            return {'error': 'Too few parameters, specify City and Country'}, 400
        elif not args.city and not args.country:
            city_query = ""
        else:
            city_query = "q={},{}".format(args.city, args.country)

        if (args.lat and not args.lon) or (args.lon and not args.lat):
            return {'error': 'Too few parameters, specify Longitude and Latitude'}, 400
        if (not args.city and not args.country and not args.lat and not args.lon):
            return {'error': 'Too few parameters'}, 400


        app.logger.info('http://api.openweathermap.org/data/2.5/forecast?{}&lat={}&lon={}&units={}&appid={}'.format(
            city_query, args.lat, args.lon, args.units, APP_ID))
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast?{}&lat={}&lon={}&units={}&appid={}'.format(
            city_query, args.lat, args.lon, args.units, APP_ID))
        if r.status_code != 200:
            return jsonify(json.loads(r.text))
        forecast_resp = json.loads(r.content)
        print("************")
        print(forecast_resp["city"]["name"])
        return jsonify(utils.create_date_map(forecast_resp))


class VersionInfo(Resource):
    def get(self):
        """API endpoint to get version of the app

        Return:
            A JSON containing the version.
        """
        app.logger.info("GET /api/v1/version called")
        resp_dict = {
            "version": version._app_version_,
        }
        return jsonify(resp_dict)

class Health(Resource):
    def get(self):
        resp_dict = {
            "Health": "I am healthy"
        }
        return jsonify(resp_dict)


api.add_resource(Info, "/")
api.add_resource(Weather, "/weather")
api.add_resource(VersionInfo, "/version")
api.add_resource(Health, "/health")


@app.route("/")
def index():
    app.logger.info("Root index / called")
    return redirect('/api/{}'.format(version._api_version_))

@app.errorhandler(404)
def not_found(e):
    app.logger.info("Invalid URL called :/")
    return 'There are no more APIs', 404
