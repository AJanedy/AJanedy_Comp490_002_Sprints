Author: Andrew Janedy
February 2025

===============================================================================

To use this program, Python 3.9 or higher needs to be installed on your 
machine.  Pytest is also required if you wish to run the test module
locally.

===============================================================================
FOR WINDOWS

To run program in command line, powershell, or gitbash, navigate to the root 
directory of the project (AJanedy_Comp490_002_Sprints), set your PYTHONPATH 
to the root directory:

    set PYTHONPATH=%cd%

then run:

    python src\job_search_database\job_search_database.py

===============================================================================
FOR LINUX

To run program in linux shell, navigate to the root directory of the project
(AJanedy_Comp490_002_Sprints), set your PYTHONPATH to the root directory:
    
    export PYTHONPATH=$(pwd)

then run:

    python3 src/job_search_database/job_search_database.py

===============================================================================

To run pytest in command line, gitbash, or linux shell, navigate to 
the project root directory and run:

export PYTHONPATH=$(pwd)/src
pytest tests/

===============================================================================

Project passes all tests and requirements
