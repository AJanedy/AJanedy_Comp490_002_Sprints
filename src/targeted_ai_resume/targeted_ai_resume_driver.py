from src.job_search_database import job_search_database_driver
from src.job_search_gui import job_search_gui_driver
from src.ai_resume_builder import resume_generator

if __name__ == "__main__":

    resume_generator.get_api_key()

    job_search_database_driver.main()
    job_search_gui_driver.main()


