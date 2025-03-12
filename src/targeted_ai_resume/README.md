Author: Andrew Janedy
March 2025

Each module in the source folder (ai_resume_builder, job_search_database, and
job_search_gui) represent their own, standalone program.  To see how to use 
each of these programs in isolation, refer to the README.md in each module
directory.

===============================================================================

To use this program in full , Python 3.9 or higher needs to be installed on your 
machine.  Pytest is also required if you wish to run the test module
locally (Functionality currently unavailable, test in IDE virtual environment
or test through GitHub actions).  If running on Linux, you may have to install
tkinter as it is not included in the base installation for this operating
system.  

This program is designed to create a database of job listings taken from 
popular online job search engines.  A simple GUI is implemented to allow a user
to more easily navigate through the database.  The GUI also offers the user the
ability to create a job/market specific user profile and save that in the same
database.  After one or more user profiles are created, the user has the 
option to query Google Gemini AI to create a custom tailored cover letter and
resume using the information provided in the job listing and the user profile.

===============================================================================
FOR WINDOWS

To run program in command line, powershell, or gitbash, navigate to the root 
directory of the project (AJanedy_Comp490_002_Sprints), set your PYTHONPATH 
to the root directory:

    set PYTHONPATH=%cd%

then run:

    python src\job_search_database\job_search_database.py
    python src\job_search_gui\job_search_gui_driver.py

===============================================================================
FOR LINUX

To run program in linux shell, navigate to the root directory of the project
(AJanedy_Comp490_002_Sprints), set your PYTHONPATH to the root directory:
    
    export PYTHONPATH=$(pwd)

then run:

    python3 src/job_search_database/job_search_database.py
    python3 src/job_search_gui/job_search_gui_driver.py

===============================================================================

To run pytest in command line, gitbash, or linux shell, navigate to 
the project root directory and run:

export PYTHONPATH=$(pwd)/src
pytest tests/

### PYTEST FUNCTIONALITY NOT CURRENTLY IMPLEMENTED ###


===============================================================================

~~Project passes all tests and requirements~~

