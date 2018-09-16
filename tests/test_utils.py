import os
from nose.tools import *
from pyphercises import utils

def test_file_reading():
    cwd = os.getcwd()
    file_content = utils.read_word_file(f"{cwd}/tests/test_input")
    assert_equal(file_content.split()[0], "testing")

def test_file_does_not_exist():
    assert_raises(NotADirectoryError, utils.read_word_file, "invalidFile")

def test_file_empty_with_map():
    cwd = os.getcwd()
    expected_result = "Word Not Found Error: One or both of the search words not found"
    output = utils.find_shortest_distance_hash_map(f"{cwd}/tests/test_empty_file", "test", "test")
    assert_equal(expected_result, output)

def test_file_empty_without_map():
    cwd = os.getcwd()
    expected_result = "Word Not Found Error: One or both of the search words not found"
    output = utils.find_shortest_distance_hash_map(f"{cwd}/tests/test_empty_file", "test", "test")
    assert_equal(expected_result, output)

def test_search_same_word_with_map():
    cwd = os.getcwd()
    expected_result = "Distance from itself should be Zero"
    output = utils.find_shortest_distance_hash_map(f"{cwd}/tests/test_input", "testing", "testing")
    print(output)
    assert_equal(expected_result, output)

def test_search_same_word_without_map():
    cwd = os.getcwd()
    expected_result = "Word Not Found Error: One or both of the search words not found"
    output = utils.find_shortest_distance(f"{cwd}/tests/test_input", "notValid", "metoo")
    assert_equal(expected_result, output)

def test_word_does_not_exist_with_map():
    cwd = os.getcwd()
    expected_result = "Word Not Found Error: One or both of the search words not found"
    output = utils.find_shortest_distance_hash_map(f"{cwd}/tests/test_input", "notValid", "metoo")
    assert_equal(expected_result, output)

def test_word_does_not_exist_without_map():
    cwd = os.getcwd()
    expected_result = "Word Not Found Error: One or both of the search words not found"
    output = utils.find_shortest_distance(f"{cwd}/tests/test_input", "notValid", "metoo")
    assert_equal(expected_result, output)

def test_distance_with_map():
    cwd = os.getcwd()
    expected_result = 2
    output = utils.find_shortest_distance(f"{cwd}/tests/test_input", "testing", "and")
    assert_equal(expected_result, output)

def test_distance_without_map():
    cwd = os.getcwd()
    expected_result = 2
    output = utils.find_shortest_distance_hash_map(f"{cwd}/tests/test_input", "testing", "and")
    assert_equal(expected_result, output)
    

    
    
