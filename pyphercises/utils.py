import os
import functools
import time

WORD_MAP = {}

# Decorator to time the functions for perf comparison
def timer(func):
    @functools.wraps(func)
    def wrapper_time(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_time

@timer
def find_shortest_distance(file_path, word_one, word_two):
    """
    Problem Statement: You have a file containing a long list of words. Write a
    function that, given any two words, finds the shortest distance between them
    in terms of numbers of words in between. For example, if this was the content of the file:
    “We do value and reward motivation in our development team. Development is a key skill for a DevOp.”
    The value of find_shortest_distance(‘motivation’, ‘development’) should be 2 (“in our”).
    It can be case insensitive. 

    :param word_one: First of two search word
    :param word_two: Second of two search word
    :type word_one: str
    :type word_two: str
    :return: Shortest distance between the words or Error message if both words not found
    :rtype: str
    """
    # TODO: There is a slight contradiction in the problem statement and base case
    # Problem statement says: "...file containing long list of 'WORDS'"
    # Sample: "... development 'team.'..." '.' is not a valid word
    # This requires handling punctuation characters while parsing
    file_content = read_word_file(file_path)
    word_one_index = None
    word_two_index = None
    min_distance = None

    if not word_one or not word_two:
        return "Invalid input: Search words cannot be empty strings"

    word_list = file_content.split()

    # go over the list
    for index, word in enumerate(word_list):
        if word.lower() == word_one:
            word_one_index = index
        if word.lower() == word_two:
            word_two_index = index
        # Only if both words are found
        if word_one_index is not None and word_two_index is not None:
            # get absolute value from the subtraction
            tmp_distance = abs(word_one_index - word_two_index)
            # Check if another occurence returns a smaller distance
            if (not min_distance or min_distance > tmp_distance):
                min_distance = tmp_distance

    # minus 1 because of problem statement
    if min_distance:
        return min_distance - 1
    elif min_distance == 0:
        return "Distance from itself should be Zero"
    else:
        return "Word Not Found Error: One or both of the search words not found"

@timer
def find_shortest_distance_hash_map(file_path, word_one, word_two):
    """
    Problem Statement: You have a file containing a long list of words. Write a
    function that, given any two words, finds the shortest distance between them
    in terms of numbers of words in between. For example, if this was the content of the file:
    “We do value and reward motivation in our development team. Development is a key skill for a DevOp.”
    The value of find_shortest_distance(‘motivation’, ‘development’) should be 2 (“in our”).
    It can be case insensitive. 

    :param word_one: First of two search word
    :param word_two: Second of two search word
    :type word_one: str
    :type word_two: str
    :return: Shortest distance between the words or Error message if both words not found
    :rtype: str
    """
    # TODO: There is a slight contradiction in the problem statement and base case
    # Problem statement says: "...file containing long list of 'WORDS'"
    # Sample: "... development 'team.'..." '.' is not a valid word
    # This requires handling punctuation characters while parsing
    word_one_index = 0
    word_two_index = 0
    min_distance = None
    create_map(read_word_file(file_path))

    if not word_one or not word_two:
        return "Invalid input: Search words cannot be empty strings"

    list_index_w1 = WORD_MAP.get(word_one)
    list_index_w2 = WORD_MAP.get(word_two)

    if ((list_index_w1 and list_index_w2) and 
        len(list_index_w1) and len(list_index_w2)):
        # Base condition so we don't go out of index when going over
        # occurences of each word
        while (word_one_index < len(list_index_w1) and word_two_index < len(list_index_w2)):
            # tmp_index_* used to loop over closer occurences
            tmp_index_w1 = list_index_w1[int(word_one_index)]
            tmp_index_w2 = list_index_w2[int(word_two_index)]

            # get absolute value from the subtraction
            tmp_distance = abs(tmp_index_w1 - tmp_index_w2)
            # Check if another occurence returns a smaller distance
            if (not min_distance or min_distance > tmp_distance):
                min_distance = tmp_distance

            # Get next occurence of the word to check if it effects min distance
            if tmp_index_w1 < tmp_index_w2:
                word_one_index += 1
            else:
                word_two_index += 1

        # minus 1 because of problem statement
        if min_distance == 0:
            return "Distance from itself should be Zero"
        else:
            return min_distance - 1
    else:
        return "Word Not Found Error: One or both of the search words not found"
                             
def create_map(words):
    # Make a list of words from string only based on <space>
    word_list = words.split()
    for index, word in enumerate(word_list):
        WORD_MAP.setdefault(word.lower(), []).append(index)

def read_word_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path) as word_file:
            # Reading entire file for proper indexing
            return word_file.read()
    else:
        raise NotADirectoryError(f"File: '{file_path}' does not exist.")
