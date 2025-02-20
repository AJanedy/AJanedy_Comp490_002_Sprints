"""
A module for extracting keys from normalized json files and comparing them
against each other.

compare_keys() is the entry point for this module, it will start with a list
of json files (as path), use helper functions extract_keys() and
build_json_key_set() to build a dictionary with the format of
{"source_json_file": set[json_keys]}, then leverage set operations to find
keys unique to each json file as well as shared keys.
"""
import json
from pathlib import Path


def compare_keys(files: list):
    """
    Compares keys to find shared attributes as well as unique attributes of json
    files containing job listings.

    compare_keys() takes a list of json files, uses the extract_keys() function
    to obtain a dictionary wherein the keys name the source file, and the values
    are each a set containing the distinct keys of the corresponding json file.
    compare_keys then uses the .intersection method to find shared json keys and
    the difference operator (-) to find json keys unique to each file.

    :param files: A list of json files
    :return:
    """
    json_keys = extract_keys(files)  # Dictionary: {"source_json_file": set[json_keys]}
    keys_list = list(json_keys.values())  # List[set[json_keys]] extracted from dictionary
    shared_keys = set.intersection(*keys_list)  # Set of keys shared between all json files

    """
    THIS CODE IS USED TO COMPARE KEYS FOR NORMALIZATION OF FILES
    AND CAN BE UNCOMMENTED FOR FURTHER ADJUSTMENTS
    """
    # print(f"\nShared Keys: {shared_keys}")
    # print("\nUnique Keys: ")
    # for key, values in json_keys.items():
    #     unique_keys = values - shared_keys
    #     print(f"\t{key}: {unique_keys}")


def extract_keys(files: list):
    """
    Helper function to extract keys from all JSON objects in the file.

    extract_keys takes a list of json files, creates a dictionary to hold
    {"source_json_file": set[json_keys]} and then iterates through the list
    of files, creating the previously defined key-value pair, and adds it to a
    dictionary to be returned at the completion of the method

    :param files: A list of json files
    :return object_keys: A dictionary with format {"source_json_file": set[json_keys]}
    """
    object_keys: dict[str, set[str]] = {}  # Dictionary to store sets of keys

    for file in files:
        object_keys[file.name] = set()  # Create a new set for each file in dictionary
        build_json_key_set(Path(file), object_keys)  # Add each unique key to the set

    return object_keys


def build_json_key_set(file: Path, object_keys: dict):
    """
        Helper function to build the dictionary {"source_json_file": set[json_keys]}

        build_json_key_set takes the path to a json file and a reference to a
        dictionary that holds the previously described key-value pairs.  This
        method will open each file and add each unique key to the set associated
        with each file in the dictionary.

        :param file: Path to a json file
        :param object_keys: A dictionary with format {"source_json_file": set[json_keys]}
        :return:
        """
    try:
        with open(file, "r", encoding="utf-8") as source_file:
            for line in source_file:
                line = line.strip()
                try:
                    json_object = json.loads(line)
                    for key in json_object:
                        # Add each unique key from the json file to the set
                        # associated with that file name
                        object_keys[file.name].add(key)
                except json.JSONDecodeError:
                    print(f"Invalid format: {line} is not a dict")
    except FileNotFoundError:
        print(f"{file} not found")
