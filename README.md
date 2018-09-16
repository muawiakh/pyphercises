# Pyphercises

This repo was created to practice problems in Python. Might not contain magic, dragons or cats.


## Install

Currently, there is nothing much to install but soon this will bloom. If you are believer? Then, welcome to the journey.

```bash

$ Requires Python >= 3.6
$ git clone https://github.com/muawiakh/pyphercises.git
$ python setup.py install
```


### Problem: Shortest distance between words

You have a file containing a long list of words. Write a function that, given any two words, finds the shortest distance
between them in terms of numbers of words in between. e.g.
"find the shortest distance between two words" -> Difference between `find` and `distance` should be `2`
It can be case insensitive.

#### How to run?

##### Pre-requisites

  - git
  - nose
  - python >= 3.6

##### Basic usage


For a very basic test:
```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout shortest_distance_words
$ cd pyphercises/
$ python3 pyphercises.py
.. Enter absolute path of file containing list of words> <absolute_path_to_word_file>
.. Enter word one to find> "<input1>"
.. Enter word two to find> "<input2>"
.. Shortest distance between 'input1' and 'input2': <shortest-distance>
```

###### Install

```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout shortest_distance_words
$ python setup.py install
```

##### Install using virtualenv
```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout shortest_distance_words
$ virtualenv -p python3.6 testenv
$ source testenv/bin/activate
$ python setup.py install
```

##### Run tests
```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout shortest_distance_words
$ # You can skip virtualenv if everything pre-installed
$ virtualenv -p python3.6 testenv
$ source testenv/bin/activate
$ python setup.py install
$ nosetests -v
```



