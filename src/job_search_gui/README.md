Author: Andrew Janedy
March 2025

===============================================================================

To use this program, Python 3.9 or higher needs to be installed on your 
machine.  Pytest is also required if you wish to run the test module
locally (Functionality currently unavailable, test in IDE virtual environment
or test through GitHub actions).  If running on Linux, you may have to install
tkinter as it is not included in the base installation for this operating
system.

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

IMPORTANT NOTE: LOCAL PYTEST FUNCTIONALITY NOT CURRENTLY WORKING, CAN RUN IN
IDE AND ON GITHUB ACTIONS

===============================================================================

~~Project passes all tests and requirements~~
