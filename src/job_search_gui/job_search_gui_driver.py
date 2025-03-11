"""
job_search_gui_driver.py is the entry point for our job search
database GUI.

os.path is leveraged to determine the absolute path of the root
directory, the name of the database file is then appended so the
absolute path can be passed into create_database_connection() to
establish a connection.

That connection is then used to extract all data from the database
and create a dictionary containing all attributes from every job
listing.  We then pass the list into our GUI's main window to be
displayed to the end user.
"""

import os

from src.job_search_gui.job_app_main_window_class import AppMainWindow
from src.job_search_gui.database_handler import (
    create_database_connection, get_jobs_from_database)

DATA_BASE_PATH = "job_listings.db"
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(SCRIPT_DIRECTORY, "../../"))
ROOT_DATABASE_PATH = os.path.join(ROOT_DIRECTORY, DATA_BASE_PATH)


def main():
    """
    Program entry.  Establish a database connection, retrieve all job listings
    from the database, open the job_search_gui main window and display every
    job listing
    """
    # Establish database connection
    database_connection = create_database_connection(ROOT_DATABASE_PATH)

    # Create a dictionary containing all job info
    job_listings = get_jobs_from_database(database_connection)

    # Launch the GUI and display all job listings
    app = AppMainWindow(database_connection, job_listings)
    app.mainloop()


if __name__ == "__main__":
    main()
