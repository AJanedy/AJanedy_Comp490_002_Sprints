"""
Test functions for job_seach_database
"""
import json
import os
import sqlite3
from contextlib import redirect_stdout
from pathlib import Path
from src.job_search_database.file_management import build_path_object, normalize_file
from src.job_search_database.database_management import create_database, populate_database

# Get directory of the script with os.path.dirname(__file__)
# Converts path to an absolute path with os.path.abspath()
test_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)))
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def test_1_build_path_object():
    """Test that build_path_object() correctly renames a file"""
    source_file = Path("json_file.json")
    expected_new_file = Path("json_file_normalized.json")
    assert build_path_object(source_file) == expected_new_file


def test_2_normalize_file():
    """
    Test to ensure that normalize_file():
        * Returns the expected path object
        * Creates a file with the expected path name
            * That the new file contains the expected number of lines
            * That each line in the new file is a valid json object
            * That json data has been normalized

    The test concludes by deleting the file created for testing, then
    tests to ensure that the file has been deleted.
    """

    source_file = Path(os.path.join(test_directory, "json_list_test_file.json"))
    expected_new_file = Path(os.path.join(test_directory, Path("json_list_test_file_normalized.json")))
    expected_new_file_line_count = 10

    # Logic for suppressing the print statements of the method
    # being tested obtained from Google Gemini AI.  os.devnull
    # represents a special file that simply discards anything
    # written to it, then redirect_stdout redirects standard
    # output.  As long as the with block is active, anything
    # normally printed to the console is effectively discarded.
    with open(os.devnull, 'w', encoding='utf-8') as trash_file, redirect_stdout(trash_file):
        # Ensure normalize_file returns the expected path object
        assert normalize_file(source_file.name, True).name == expected_new_file.name

    # Ensure that a file has been created using that Path name
    assert expected_new_file.exists()

    # Open new file and count lines
    with open(expected_new_file, "r", encoding='utf-8') as file:
        lines = file.readlines()  # Read all lines into a list
        new_file_line_count_actual = len(lines)  # Determine length of list (line count)

        # Ensure that the new file contains the expected number of lines
        assert new_file_line_count_actual == expected_new_file_line_count

        file.seek(0)  # Move pointer back to beginning of file
        for line in file:
            try:
                json_object = json.loads(line)
                # Ensures that each line is a valid json object
                assert isinstance(json_object, dict)
                # Ensures data is properly normalized
                assert "compensation" in json_object
                assert "job_providers" in json_object
                assert "employment_type" in json_object
                assert "date_posted" in json_object
                assert "interval" in json_object
                assert "location" in json_object
                assert "employment_type" in json_object
                assert "company_logo" in json_object
                assert "job_url" in json_object

            except json.JSONDecodeError as error:
                assert False, f"Line is not valid json: {error}"


def test_3_create_database():
    """
    Tests to ensure that create_database:
        * Properly creates a database with a predetermined file name
        * Creates the tables required for data insertion
    """
    # Create mock database for testing
    test_database = "test_database.db"

    # Logic for suppressing the print statements of the method
    # being tested obtained from Google Gemini AI.  os.devnull
    # represents a special file that simply discards anything
    # written to it, then redirect_stdout redirects standard
    # output.  As long as the with block is active, anything
    # normally printed to the console is effectively discarded.
    with open(os.devnull, 'w', encoding='utf-8') as trash_file, redirect_stdout(trash_file):
        create_database(test_database)

    # Convert name (str) to Path object and test its existence
    test_database = Path(test_database)
    assert test_database.exists

    # Establish connection to the test database
    connection = sqlite3.connect(test_database)
    cursor = connection.cursor()

    # Query the database to create a set containing the table names
    # A set allows comparison of tables regardless of their order
    # in the data structure
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Creates a set of the tables in the database
    tables = {row[0] for row in cursor.fetchall()}

    expected_tables = {"job_listings", "rapid_results_unique_data"}
    assert tables == expected_tables

    connection.commit()
    connection.close()


def test_4_populate_database():
    """
        Tests to ensure that populate_database properly populates
        the database with the fixed test data.
    """
    test_database = "test_database.db"
    json_files = [Path(os.path.join(test_directory, "json_list_test_file_normalized.json"))]

    # Logic for suppressing the print statements of the method
    # being tested obtained from Google Gemini AI.  os.devnull
    # represents a special file that simply discards anything
    # written to it, then redirect_stdout redirects standard
    # output.  As long as the with block is active, anything
    # normally printed to the console is effectively discarded.
    with open(os.devnull, 'w', encoding='utf-8') as trash_file, redirect_stdout(trash_file):
        populate_database(test_database, json_files)

    # Establish connection to the test database
    connection = sqlite3.connect(test_database)
    cursor = connection.cursor()

    # Query the database to get all titles from job_listings table
    cursor.execute("SELECT title FROM job_listings")
    # Creates a list of all the titles from job_listings table
    job_titles = [row[0] for row in cursor.fetchall()]

    expected_job_titles = ["Staff Software Engineer, Risk", "Software Developer",
                           "Software Engineer", "Software Engineer",
                           "Senior Software Development Engineer", "Software Developer",
                           "Engineer II Software Engineering - US Based Remote",
                           "Cloud Infrastructure Software Developer",
                           "Software Developer - Item Assist product",
                           "Sr. Software Developer"]

    assert job_titles == expected_job_titles

    # Query the database to get all companies from job_listings table
    cursor.execute("SELECT company FROM job_listings")
    # Creates a list of all the companies from job_listings table
    companies = [row[0] for row in cursor.fetchall()]

    expected_companies = ["WEXWEXUS", "Bio-Rad Laboratories, Inc.", "Epic", "Actalent",
                          "Adobe", "ALTA IT Services", "Anywhere Real Estate",
                          "Apple", "Pearson", "Stanford University"]

    assert expected_companies == companies

    connection.commit()
    connection.close()


def test_5_file_and_database_deletion():
    """
    A method to delete the files created during the testing process
    :return:
    """
    test_file = Path(os.path.join(test_directory, "json_list_test_file_normalized.json"))
    test_file.unlink()  # Delete the file
    assert not test_file.exists()  # Ensure file has been deleted

    test_database = Path(os.path.join(test_directory, "test_database.db"))
    if test_database.exists():
        test_database.unlink()
        assert not test_database.exists()
    test_database = Path(os.path.join(root_directory, "test_database.db"))
    if test_database.exists():
        test_database.unlink()
        assert not test_database.exists()
