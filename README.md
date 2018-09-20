# Pyphercises

This repo was created to practice problems in Python. Might not contain magic, dragons or cats.


## Install

Currently, there is nothing much to install but soon this will bloom. If you are believer? Then, welcome to the journey.

```bash

$ Requires Python >= 3.6
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ python setup.py install || pip install .
```


### Problem: Basic app

Simple application to display its current version.

#### How to run?

##### Pre-requisites

  - git
  - python >= 3.6
  - flask

##### Basic usage


For a very basic test:
```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout release-workflow
$ cd pyphercises/
$ python app.py
```

###### Install

```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout release-workflow
$ python setup.py install || pip install .
```

##### Install using virtualenv
```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout release-workflow
$ virtualenv -p python3.6 testenv
$ source testenv/bin/activate
$ python setup.py install || pip install .
```


##### Run and test
```bash
$ python app.py
...
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
$ # Open Browser or in another terminal
$ curl http://localhost:5000 | jq || curl http://localhost:5000
...
{
  "description": "First cut app",
  "name": "BaseApp",
  "version": "2.0.0"
}
```
