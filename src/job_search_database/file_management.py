"""
A module to normalize data between two differently formatted json files

Module file_management.py enters at normalize_file().  normalize_file()
first creates a path object to represent a new file for the normalized
data of the original file, it will then pass both original file (Path)
and new file (Path) into the read_and_write_files() method where the
source file is read and normalized, then written to the new, normalized
file location.
"""
import os
import json
from pathlib import Path
from typing import TextIO


def normalize_file(file: str, is_test: bool):
    """
    Normalizes each file of JSON objects into a standardized data structure

    normalize_file() accepts the string name of a file, converts it to a
    Path object, creates a Path object to represent the file that will
    hold the normalized data from the original file (using the
    build_path_object() method), and then uses the read_and_write_files()
    method to read in the original file and convert it to a normalized
    format, so it can be written to the new file.

    :param is_test:
    :param file: The name of a json file (as string) containing job listings
    :return normalized_file_path_obj: A path object representing the new
        file containing normalized data.
    """
    if not is_test:
        # os.path.abspath() gets the absolute path of its argument
        # os.path.dirname() gets the directory of its argument
        # __file__ is a built-in variable representing the path of the current script
        project_directory = os.path.abspath(os.path.dirname(__file__))
        json_folder = os.path.join(project_directory, "json_files")

        source_file = Path(os.path.join(json_folder, file))
        normalized_file_path_obj = Path(os.path.join(json_folder, build_path_object(source_file)))
        read_and_write_files(source_file, normalized_file_path_obj)

        return normalized_file_path_obj

    if is_test:
        # Get the absolute path to the root directory
        root_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        test_directory = os.path.join(root_directory, "tests", "test_job_search_database")

        source_file = Path(os.path.join(test_directory, file))
        normalized_file_path_obj = Path(os.path.join(test_directory, build_path_object(source_file)))

        read_and_write_files(source_file, normalized_file_path_obj)

        return normalized_file_path_obj


def read_and_write_files(input_file: Path, normalized_file_path_obj: Path):
    """
    A method that opens a json file that may require normalization and creates
    and opens another json file to hold the normalized data.

    read_and_write_files() first opens the input file for reading, then creates
    and opens the output (normalized file) for writing.  This method will then
    determine the format of the input file and will send it through the
    appropriate method (either process_json_array() or process_json_object())
    for normalization.

    :param input_file: Path object representing one of the original json files
    :param normalized_file_path_obj: Path object representing a file containing
        the normalized data of the input file.
    :return:
    """
    with open(input_file, "r", encoding="utf-8") as read_file:  # Open input file
        # Create and open output file
        with open(normalized_file_path_obj, "w", encoding="utf-8") as write_file:
            for line in read_file:
                line = line.strip()
                # If each line is an list of JSON objects: [{json obj}, {json obj}, {json obj}]
                if line.startswith("[") and line.endswith("]"):
                    process_json_array(input_file, line, write_file)
                else:
                    process_json_object(input_file, line, write_file)


def build_path_object(source_file: Path):
    """
    A method to create a file (and file name) that represents the
    normalized data of a source json file.

    build_path_object() takes the Path of a source json file, concatenates
    "_normalized" to the end of the file name ("source.json" becomes
    "source_normalized.json") then returns that new file name as a Path
    object.

    :param source_file: A Path object representing a source json file
    :return normalized_file: A path object representing a file containing
        the normalized data of the input file
    """
    normalized_file = Path(source_file.stem + "_normalized" + source_file.suffix)
    return normalized_file


def process_json_array(source_file: Path, line: str, output_file: TextIO):
    """
    A method for extracting individual json objects from a line (string) containing a
    list of json objects.

    process_json_array() leverages the json.loads() method to create a list of json
    objects from a single line (a string obtained from a source json file), the method
    then iterates through this list, passing each json object into the
    normalize_json_object() method where keys are normalized between sources where
    applicable.  json.dumps() then formats the json object into a string to be written
    to the new, normalized file

    :param source_file: A Path object that represents a source json file
    :param line: A string containing the contents of one line from the source json file.
    :param output_file: A TextIO wrapper representing the output file for the
        normalized json data
    :return:
    """
    try:
        json_objects = json.loads(line)  # Parse the JSON array from the line into a list.

        for json_object in json_objects:
            json_object = normalize_json_object(json_object)
            # Write each JSON object to the new file, one per line
            output_file.write(json.dumps(json_object) + "\n")

    except json.JSONDecodeError as e:
        print(f"Error parsing line in {source_file}: {e}")


def process_json_object(source_file: Path, line: str, output_file: TextIO):
    """
    A method for extracting individual json objects from a line (string) that
    represents a single json object

    process_json_array() leverages the json.loads() method to create a json objects
    from a single line (a string obtained from a source json file), the method
    then passes this object into the normalize_json_object() method where keys are
    normalized between sources where applicable.  json.dumps() then formats the json
    object into a string to be written to the new, normalized file.

    :param source_file: A Path object that represents a source json file
    :param line: A string containing the contents of one line from the source json file.
    :param output_file: A TextIO wrapper representing the output file for the
        normalized json data
    :return:
    """
    try:
        json_objects = json.loads(line)
        json_object = normalize_json_object(json_objects)
        output_file.write(json.dumps(json_object) + "\n")

    except json.JSONDecodeError as e:
        print(f"Error parsing line in {source_file}: {e}")


def normalize_json_object(json_obj: dict):
    """
    A method for normalizing json objects with similar attributes
    of different names for future database manipulation

    :param json_obj: Dictionary/json object
    :return json_obj: Dictionary/json object
    """
    if "salaryRange" in json_obj:
        json_obj["compensation"] = json_obj.pop("salaryRange")
    if "jobProviders" in json_obj:
        json_obj["job_providers"] = json_obj.pop("jobProviders")
    if "employmentType" in json_obj:
        json_obj["employment_type"] = json_obj.pop("employmentType")
    if "datePosted" in json_obj:
        json_obj["date_posted"] = json_obj.pop("datePosted")
    if "interval" not in json_obj:
        json_obj["interval"] = "yearly"
    if "min_amount" in json_obj:
        json_obj["compensation"] = f"{json_obj['min_amount']} - {json_obj['max_amount']}"
        del json_obj["min_amount"]
        del json_obj["max_amount"]
    if "company_addresses" in json_obj:
        json_obj["location"] = json_obj.pop("company_addresses")
    if "job_type" in json_obj:
        json_obj["employment_type"] = json_obj.pop("job_type")
    if "image" in json_obj:
        json_obj["company_logo"] = json_obj.pop("image")
    if "job_url" not in json_obj:
        json_obj["job_url"] = ""
    return json_obj
