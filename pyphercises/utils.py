def find_shortest_distance_hash_map(word_map, word_one, word_two):
    """
    Problem Statement: You have a file containing a long list of words. Write a
    function that, given any two words, finds the shortest distance between them
    in terms of numbers of words in between. For example, if this was the content of the file:
    “We do value and reward motivation in our development team. Development is a key skill for a DevOp.”
    The value of find_shortest_distance(‘motivation’, ‘development’) should be 2 (“in our”).
    It can be case insensitive. 
    

    :param word_map: Hashmap of all the words in input
    :param word_one: First of two search word
    :param word_two: Second of two search word
    :type word_map: dict 
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

    if not word_one or not word_two:
        return "Invalid input: Search words cannot be empty strings"

    list_index_w1 = word_map.get(word_one)
    list_index_w2 = word_map.get(word_two)
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
            print(tmp_distance)
            # Check if another occurence returns a smaller distance
            if (not min_distance or min_distance > tmp_distance):
                min_distance = tmp_distance

            # Get next occurence of the word to check if it effects min distance
            if tmp_index_w1 < tmp_index_w2:
                word_one_index += 1
            else:
                word_two_index += 1
        if min_distance - 1 == -1:
            return "Distance from itself should be Zero"
        else:
            return min_distance - 1
    else:
        return "Word Not Found Error: One or both of the search words not found"
                             
def create_map():
    word_map = {}
    base_string = "We do value and reward motivation in our development team. Development is a key skill for a DevOp."
    # Make a list of words from string only based on <space>
    base_string_list = base_string.split()
    for index, word in enumerate(base_string_list):
        word_map.setdefault(word.lower(), []).append(index)

    return word_map
