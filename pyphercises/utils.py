import datetime
from pyphercises import constants

# Util functions


def calculate_list_average(data):
    return round(sum(data) / len(data), 2)


def create_date_map(res):
    DATE_MAP = {}
    # Needed because the API returns 5 day forecast
    start_forecast_date = datetime.datetime.now()
    end_forecast_date = start_forecast_date + \
        datetime.timedelta(days=constants.FORECAST_DELTA)
    interation_step = datetime.timedelta(days=1)
    while start_forecast_date <= end_forecast_date:
        start_forecast_date_fmt = start_forecast_date.strftime("%Y-%m-%d")
        DATE_MAP.setdefault(start_forecast_date_fmt, {})
        for i in range(len(res["list"])):
            if start_forecast_date_fmt in res["list"][i]["dt_txt"]:
                DATE_MAP[start_forecast_date_fmt].setdefault(
                    "temperature", []).append(res["list"][i]["main"]["temp"])
                DATE_MAP[start_forecast_date_fmt].setdefault(
                    "humidity", []).append(res["list"][i]["main"]["humidity"])
                DATE_MAP[start_forecast_date_fmt].setdefault(
                    "wind", []).append(res["list"][i]["wind"]["speed"])
                if "rain" in res["list"][i] and res["list"][i]["rain"]:
                    DATE_MAP[start_forecast_date_fmt].setdefault(
                        "rain", []).append(res["list"][i]["rain"]["3h"])
                if "snow" in res["list"][i] and res["list"][i]["snow"]:
                    DATE_MAP[start_forecast_date_fmt].setdefault(
                        "snow", []).append(res["list"][i]["snow"]["3h"])
        start_forecast_date += interation_step

    return create_resp_dict(DATE_MAP, res)


def create_resp_dict(dmap, res):
    resp_dict = {}
    # Calculating averages
    for key, value in dmap.items():
        resp_dict.setdefault(key, {})
        resp_dict[key]["temperature"] = calculate_list_average(
            dmap[key]["temperature"])
        resp_dict[key]["humidity"] = calculate_list_average(
            dmap[key]["humidity"])
        resp_dict[key]["wind"] = calculate_list_average(dmap[key]["wind"])
        if "rain" in dmap[key]:
            resp_dict[key].setdefault("precipitation", {})
            resp_dict[key]["precipitation"]["rain"] = calculate_list_average(
                dmap[key]["rain"])
        if "snow" in dmap[key]:
            resp_dict[key].setdefault("precipitation", {})
            resp_dict[key]["precipitation"]["snow"] = calculate_list_average(
                dmap[key]["snow"])
    try:
        resp_dict["city"] = res["city"]["name"]
        resp_dict["country"] = res["city"]["country"]
        resp_dict["coord"] = {}
        resp_dict["coord"]["lat"] = res["city"]["coord"]["lat"]
        resp_dict["coord"]["lon"] = res["city"]["coord"]["lon"]
    except KeyError:
        # passing intentionally
        pass
    return resp_dict
