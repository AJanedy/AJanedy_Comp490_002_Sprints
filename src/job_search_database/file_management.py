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
from pathlib import Path
from src.job_search_database.data_normalization import process_json_array, process_json_object


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
    source_file = None
    normalized_file_path_obj = None

    if not is_test:
        # os.path.abspath() gets the absolute path of its argument
        # os.path.dirname() gets the directory of its argument
        # __file__ is a built-in variable representing the path of the current script
        project_directory = os.path.abspath(os.path.dirname(__file__))
        json_folder = os.path.join(project_directory, "json_files")

        source_file = Path(os.path.join(json_folder, file))
        normalized_file_path_obj = Path(os.path.join(json_folder, build_path_object(source_file)))

    if is_test:
        # Get the absolute path to the root directory
        root_directory = os.path.dirname(os.path.dirname
                                         (os.path.dirname(os.path.abspath(__file__))))
        test_directory = os.path.join(
            root_directory, "tests", "test_job_search_database")

        source_file = Path(os.path.join(test_directory, file))
        normalized_file_path_obj = Path(os.path.join
                                        (test_directory, build_path_object(source_file)))

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



