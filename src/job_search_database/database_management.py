"""
A module for creating a database that will hold job listings sourced from
varying files of json objects.

create_database(), which accepts a .db path as an argument, is the entry
point for database creation.  If the given path does not exist this method
will create and open that database, if it does exist it will simply open the
database.  create_database() then leverages 3 helper methods to create 3
predefined tables to hold the data from normalized .json files

populate_database(), which accepts a .db path as well as a list of files as
arguments, is the entry point for the insertion of data into the previously
created database.  This method will open each file in the list, create a
json object from each line in the file, then call the appropriate helper
functions used to populate each table.
"""
import json
import sqlite3
from sqlite3 import Cursor


def create_database(database_path: str):
    """
    Creates a database with the passed argument as the database name

    create_database() accepts a string argument that represents the name
    of the database being opened or created.  Helper methods create...()
    are used to create tables to be used elsewhere in this module to
    hold data from json objects representing job listings.

    :param database_path:
    :return:
    """
    print(f"\nCreating database {database_path}")

    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        create_shared_table(cursor)
        create_rapid_results_unique_table(cursor)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    print(f"{database_path} created.")


def create_shared_table(cursor: Cursor):
    """
    Creates a table that contains the shared keys of both json files

    :param cursor: A cursor object used to execute SQL queries
    :return:
    """

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_listings (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            date_posted TEXT,
            description TEXT,
            employment_type TEXT,
            interval TEXT,
            compensation TEXT,
            job_url TEXT
        )   
    """)


def create_rapid_results_unique_table(cursor: Cursor):
    """
    Creates a table for the unique values of rapidResults_normalized.json

    :param cursor: A cursor object used to execute SQL queries
    :return:
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rapid_results_unique_data (
            id TEXT PRIMARY KEY,
            company_url_direct TEXT,
            company_description TEXT,
            currency TEXT,
            job_function TEXT,
            company_num_employees INT,
            job_url_direct TEXT,
            ceo_name TEXT,
            ceo_photo_url TEXT,
            company_revenue TEXT,
            job_level TEXT,
            logo_photo_url TEXT,
            salary_source TEXT,
            emails TEXT,
            site TEXT,
            is_remote INT,
            listing_type TEXT,
            banner_photo_url TEXT,
            company_industry TEXT,
            company_url TEXT
        )
    """)


def populate_database(database_path: str, source_files: list):
    """
    A method to parse json objects from a file and populate a .db
    database

    populate_database() creates a connection via sqlite3 to the
    database passed in as argument, then opens each file in the
    passed list, creates a json object from each line in that
    list, then passes those objects into the appropriate helper
    function to populate the tables in the database.

    :param database_path: .db path to database file
    :param source_files: list of files containing json objects
    :return:
    """
    print(f"Populating {database_path}")

    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        for file in source_files:
            with open(file, "r", encoding="utf-8") as source_file:
                for line in source_file:
                    json_object = json.loads(line)
                    populate_shared_table(cursor, json_object)
                    if file.filename == "rapid_results_normalized.json":
                        populate_rapid_results_unique_table(cursor, json_object)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    print(f"{database_path} populated.")


def populate_shared_table(cursor: Cursor, json_object: dict):
    """
    Executes a sql statement to populate a table within a database

    *** Proper syntax assisted with Google Gemini AI ***

    :param cursor:
    :param json_object:
    :return:
    """
    cursor.execute("""
        INSERT OR IGNORE INTO job_listings (
            id, title, company, location, date_posted, description, 
            employment_type, interval, compensation, job_url
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        json_object["id"], json_object["title"],
        json_object["company"], json_object["location"],
        json_object["date_posted"], json_object["description"],
        json_object["employment_type"], json_object["interval"],
        json_object["compensation"], json_object["job_url"]
    ))


def populate_rapid_results_unique_table(cursor: Cursor, json_object: dict):
    """
    Executes a sql statement to populate a table within a database

    :param cursor:
    :param json_object:
    :return:
    """
    cursor.execute("""
        INSERT OR IGNORE INTO rapid_results_unique_data (
            id, company_url_direct, company_description,
            currency, job_function, company_num_employees, job_url_direct,
            company_revenue, job_level,
            salary_source, emails, site, is_remote, listing_type,
            company_industry, company_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (json_object["id"],
          json_object["company_url_direct"], json_object["company_description"],
          json_object["currency"], json_object["job_function"],
          json_object["company_num_employees"], json_object["job_url_direct"],
          json_object["company_revenue"], json_object["job_level"],
          json_object["salary_source"], json_object["emails"],
          json_object["site"], json_object["is_remote"],
          json_object["listing_type"], json_object["company_industry"],
          json_object["company_url"]
          ))
