import utils

if __name__ == '__main__':
    file_path = input("Enter absolute path of file containing list of words> ")
    word_one = input("Enter word one to find> ").lower()
    word_two = input("Enter word two to find> ").lower()
    
    print(f"Shortest distance between '{word_one}' and '{word_two}': {utils.find_shortest_distance(file_path, word_one, word_two)}")
    print(f"Shortest distance between '{word_one}' and '{word_two}' using Hashmap: {utils.find_shortest_distance_hash_map(file_path, word_one, word_two)}")
