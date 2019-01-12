# Pyphercises

This repo was created to practice problems in Python. Might not contain magic, dragons or cats.


## Install

Currently, there is nothing much to install but soon this will bloom. If you are believer? Then, welcome to the journey.

```bash

$ Requires Python >= 3.6
$ git clone https://gitlab.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ python setup.py install || pip install .
```


### Problem: Basic Weather App

Simple weather application to get weather forecast for the next 2 days.

#### How to run?

##### Pre-requisites

  - git
  - python >= 3.6
  - flask
  - flask-restful
  - requests

##### Basic usage


For a very basic test:
```bash
$ git clone https://gitlab.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout basic-weather-app
$ python setup.py install || pip install .
$ python run.py
```

###### Install

```bash
$ git clone https://gitlab.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout basic-weather-app
$ python setup.py install || pip install .
```

##### Install using virtualenv
```bash
$ git clone https://gitlab.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout basic-weather-app
$ virtualenv -p python3 testenv
$ source testenv/bin/activate
$ python setup.py install || pip install .
```


##### Run and test
```bash
$ export WEATHER_APP_ID=<APP_ID>
$ python run.py
...
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
$ # Open Browser or in another terminal
$ curl http://localhost:5000 | jq || curl http://localhost:5000
...
{
  "description": "First cut weather app",
  "name": "Basic weather app",
  "version": "/api/v1/version",
  "weather": "/api/v1/weather"
}
$ # CHECK Weather
$ curl http://localhost:5000/api/v1/weather?city=berlin&country=de
```


##### Install and run with Docker
```bash
$ git clone https://gitlab.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout basic-weather-app
$ docker build -t pyphercises/basicweatherapp:latest --build-arg APP_ID=<APP_ID> .
$ docker run -d -p 5000:5000 --name weatherApp pyphercises/basicweatherapp:latest
$ # TO test
$ # Open Browser or in another terminal
$ curl http://localhost:5000 | jq || curl http://localhost:5000

$ # CHECK Weather
$ curl http://localhost:5000/api/v1/weather?city=berlin&country=de
```

##### Install and run with Docker
```bash
$ git clone https://gitlab.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout basic-weather-app
$ export WEATHER_APP_ID=<APP_ID>
$ make build
$ make run
$ # TO test
$ # Open Browser or in another terminal
$ curl http://localhost:5000 | jq || curl http://localhost:5000
$ # CHECK Weather
$ curl http://localhost:5000/api/v1/weather?city=berlin&country=de
$ # If you want to stop the app
$ make stop
$ # OR
$ make test
```

#### API Usage

##### Endpoints

The API currently supports the following endpoints:

```bash
/
/api/v1/
/api/v1/version
/api/v1/weather
```

###### /

**Note** Any request to the root endpoint will be redirected to */api/v1/*

**API Call**

http://<API/URL>:5000/

**Response code:** *302*

**Example Response**
```json
{
    "description": "First cut weather app",
    "name": "Basic weather app",
    "version": "/api/v1/version",
    "weather": "/api/v1/weather"
}
```

###### /api/v1/

**API Call**

http://<API/URL>:5000/api/v1/

**Response code:** *200*

**Example Response**
```json
{
    "description": "First cut weather app",
    "name": "Basic weather app",
    "version": "/api/v1/version",
    "weather": "/api/v1/weather"
}
```

###### /api/v1/version

**API Call**

http://<API/URL>:5000/api/v1/version

**Response code:** *200*

**Example Response**
```json
{
    "version": "1.0.0"
}
```

###### /api/v1/weather

**API Call: By City and Country**

http://<API/URL>:5000/api/v1/weather?city=Berlin&country=de

**Response code:** *200*

**Example Response**
```json
{
    "2019-01-11": {
        "humidity": 93.5,
        "precipitation": {
            "rain": 0.07
        },
        "temperature": 2.88,
        "wind": 6.09
    },
    "2019-01-12": {
        "humidity": 95.12,
        "precipitation": {
            "rain": 0.42,
            "snow": 0.0
        },
        "temperature": 3.01,
        "wind": 6.67
    },
    "2019-01-13": {
        "humidity": 96.0,
        "precipitation": {
            "rain": 0.94
        },
        "temperature": 5.64,
        "wind": 9.28
    },
    "city": "Berlin",
    "coord": {
        "lat": 52.517,
        "lon": 13.3889
    },
    "country": "DE"
}
```

**API Call: By Longitude and Latitude**

http://<API/URL>:5000/api/v1/weather?lon=13.3889&lat=52.517

**Response code:** *200*

**Example Response**
```json
{
    "2019-01-12": {
        "humidity": 96.2,
        "precipitation": {
            "rain": 0.58,
            "snow": 0
        },
        "temperature": 6.17,
        "wind": 7.35
    },
    "2019-01-13": {
        "humidity": 96,
        "precipitation": {
            "rain": 0.94
        },
        "temperature": 5.64,
        "wind": 9.28
    },
    "2019-01-14": {
        "humidity": 90.38,
        "precipitation": {
            "rain": 0.16,
            "snow": 0.19
        },
        "temperature": 2.07,
        "wind": 10.09
    },
    "city": "Berlin Mitte",
    "coord": {
        "lat": 52.52,
        "lon": 13.4049
    },
    "country": "DE"
}
```

**API Call: By City only**

http://<API/URL>:5000/api/v1/weather?city=Berlin

**Response code:** *400*

**Example Response**
```json
{
    "error": "Too few parameters, specify City and Country"
}
```

**API Call: By Country only**

http://<API/URL>:5000/api/v1/weather?country=de

**Response code:** *400*

**Example Response**
```json
{
    "error": "Too few parameters, specify City and Country"
}
```

**API Call: By Latitude only**

http://<API/URL>:5000/api/v1/weather?lat=123

**Response code:** *400*

**Example Response**
```json
{
    "error": "Too few parameters, specify Longitude and Latitude"
}
```

**API Call: By Longitude only**

http://<API/URL>:5000/api/v1/weather?lon=123

**Response code:** *400*

**Example Response**
```json
{
    "error": "Too few parameters, specify Longitude and Latitude"
}
```

**API Call: By invalid units**

http://<API/URL>:5000/api/v1/weather?units=random

**Response code:** *400*

**Example Response**
```json
{
    "error": "Invalid unit parameter, choose: [metric, imperial]"
}
```

**API Call: By metric units**

http://<API/URL>:5000/api/v1/weather?city=berlin&country=de&units=metric

**Response code:** *200*

**Example Response**
```json
{
    "2019-01-12": {
        "humidity": 96.2,
        "precipitation": {
            "rain": 0.58,
            "snow": 0
        },
        "temperature": 6.17,
        "wind": 7.35
    },
    "2019-01-13": {
        "humidity": 96,
        "precipitation": {
            "rain": 0.94
        },
        "temperature": 5.64,
        "wind": 9.28
    },
    "2019-01-14": {
        "humidity": 90.38,
        "precipitation": {
            "rain": 0.16,
            "snow": 0.19
        },
        "temperature": 2.07,
        "wind": 10.09
    },
    "city": "Berlin",
    "coord": {
        "lat": 52.517,
        "lon": 13.3889
    },
    "country": "DE"
}
```

**API Call: By imperial units**

http://<API/URL>:5000/api/v1/weather?city=berlin&country=de&units=imperial

**Response code:** *200*

**Example Response**
```json
{
    "2019-01-12": {
        "humidity": 96.2,
        "precipitation": {
            "rain": 0.58,
            "snow": 0
        },
        "temperature": 43.11,
        "wind": 16.45
    },
    "2019-01-13": {
        "humidity": 96,
        "precipitation": {
            "rain": 0.94
        },
        "temperature": 42.16,
        "wind": 20.77
    },
    "2019-01-14": {
        "humidity": 90.38,
        "precipitation": {
            "rain": 0.16,
            "snow": 0.19
        },
        "temperature": 35.71,
        "wind": 22.58
    },
    "city": "Berlin",
    "coord": {
        "lat": 52.517,
        "lon": 13.3889
    },
    "country": "DE"
}
```






