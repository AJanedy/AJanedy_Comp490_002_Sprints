"""
Author: Andrew Janedy
February 2025

A program to read json files containing job postings and normalize
the json data for insertion into a SQL database.

This program reads from a list containing two files of json data
from online job postings.  This program is designed to handle the
two included files, wherein one file only contains one json object
per line, and the other file contains a list of multiple json files
per line.  Alterations to program logic would need to be implemented
if more files or files of differing formats were introduced.

This program begins by reading in each file and normalizing their
data, then creates new files analogous with the source files,
each containing the normalized data.  This process begins with
the normalize_file() method found in file_management.py

After normalization, the shared and unique keys for each json object
will be printed to the screen, this is merely a remnant of
normalization process.  Key comparison begins with the compare_keys()
method found in key_comparison.py

The program will then create a database containing two tables, one
to hold the shared attributes of both files, and the other to hold
the unique attributes from rapid_results_normalized.json.
A third table to hold the unique attributes for
rapid_jobs2_normalized.json is not created as there is only one
remaining unique attribute that is not exceptionally relevant. This
process begins with the create_database() method found in
database_management.py.

Finally, the previously created database is populated with the data
from each json file.  This process begins with the populate_database()
method found in database_management.py.
"""
from database_management import create_database, populate_database
from file_management import normalize_file
from key_comparison import compare_keys

FILES = [
    "rapid_jobs2.json",
    "rapid_results.json"
]

normalized_files = []

DATABASE_PATH = "job_listings.db"


def launch_job_database():

    for file in FILES:
        normalized_files.append(normalize_file(file))

    # Prints shared and unique keys after initial normalization
    # Can be used for further comparison and normalization of data
    compare_keys(normalized_files)

    create_database(DATABASE_PATH)
    populate_database(DATABASE_PATH, normalized_files)


if __name__ == "__main__":
    launch_job_database()