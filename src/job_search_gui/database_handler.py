"""
A module for connecting to an SQL database and making basic queries
"""
import sqlite3
from sqlite3 import Connection


def create_database_connection(database_path: str):
    """
    Connect to database
    :param database_path:
    :return:
    """
    connection = sqlite3.connect(database_path)
    return connection


def get_jobs_from_database(database_connection: Connection):
    """
    A method to execute an SQL query to retrieve all job listings
    and associated data from the job_listings database.

    :param database_connection:
    :return job_listings:
    """
    cursor = database_connection.cursor()
    cursor.execute("""
        SELECT id, 
               title, 
               company, 
               location, 
               date_posted, 
               description, 
               employment_type, 
               interval, 
               compensation, 
               job_url 
        FROM job_listings
        """
                   )
    job_listings = {}  # Create a dictionary to hold job data

    rows = cursor.fetchall()

    for row in rows:
        job_listings[row[0]] = {
            "job_title": row[1],
            "company": row[2],
            "location": row[3],
            "date_posted": row[4],
            "description": row[5],
            "employment_type": row[6],
            "interval": row[7],
            "compensation": row[8],
            "job_url": row[9]
        }

    return job_listings
