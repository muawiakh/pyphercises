import utils

if __name__ == '__main__':
    word_one = str(input("Enter word one to find> ")).lower()
    word_two = str(input("Enter word two to find> ")).lower()
    word_map = utils.create_map()
    print(f"Shortest distance between '{word_one}' and '{word_two}': {utils.find_shortest_distance_hash_map(word_map, word_one, word_two)}")
