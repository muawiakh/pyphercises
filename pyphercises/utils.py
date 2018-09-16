def find_shortest_distance(word_one, word_two):
    """
    Problem Statement: You have a file containing a long list of words. Write a
    function that, given any two words, finds the shortest distance between them
    in terms of numbers of words in between. For example, if this was the content of the file:
    "find the shortest distance between two words" -> Difference between `find` and `distance` should be `2`
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
    # Which is not part of the solution


    base_string = "We do value and reward motivation in our development team. Development is a key skill for a DevOp."
    word_one_index = None
    word_two_index = None
    min_distance = None

    if not word_one or not word_two:
        return "Invalid input: Search words cannot be empty strings"

    # Make a list of words from string only based on <space>
    base_string_list = base_string.split()

    # go over the list
    for index, word in enumerate(base_string_list):
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

    if min_distance:
        # minus one because of requirements of the problem
        return str(min_distance - 1)
    else:
        return "Word Not Found Error: One or both of the search words not found"
