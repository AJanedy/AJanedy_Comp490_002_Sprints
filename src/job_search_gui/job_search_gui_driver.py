import os

from src.job_search_gui.JobAppMainWindow import AppMainWindow
from src.job_search_gui.database_handler import create_database_connection, get_job_titles_from_database

DATA_BASE_PATH = "job_listings.db"
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(SCRIPT_DIRECTORY, "../../"))
ROOT_DATABASE_PATH = os.path.join(ROOT_DIRECTORY, DATA_BASE_PATH)


if __name__ == "__main__":

    database_connection = create_database_connection(ROOT_DATABASE_PATH)
    job_listings = get_job_titles_from_database(database_connection)

    app = AppMainWindow(database_connection, job_listings)
    app.mainloop()



