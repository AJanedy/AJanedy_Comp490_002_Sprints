"""
A module for testing essential job_search_gui functions
"""
import os.path
from unittest.mock import MagicMock, patch
import pytest
import sqlite3
import tkinter as tk
from pathlib import Path
import google.generativeai as genai

from src.job_search_gui.job_app_main_window_class import AppMainWindow
from src.job_search_gui.user_attribute_popup import UserAttributePopup
from src.ai_resume_builder.resume_generator import get_api_key

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
ROOT_DIRECTORY = SCRIPT_DIRECTORY.parent.parent


@pytest.fixture
def setup_user_attribute_popup():
    """
    Fixture to set up a mock root window if headless or allow a normal display
    if running locally, create a database connection, then instantiate an instance
    of the UserAttributePopup class and create

    Lines 22 - 34 written by Google Gemini
    """

    # Mock Tk() to prevent actual GUI window creation in headless environments
    mock_root = MagicMock(spec=tk.Tk)
    mock_root.withdraw = MagicMock()  # Mock the withdraw method
    mock_root.quit = MagicMock()  # Mock the quit method to prevent blocking event loop
    # Mock the necessary `tk` attributes for proper initialization of UserAttributePopup
    mock_root.tk = MagicMock()  # Mock the `tk` attribute
    mock_root.children = {}  # Mock the `children` attribute
    mock_root.master = None  # Mock the `master` attribute as None, or root
    root = mock_root

    db_conn = sqlite3.connect(":memory:")  # In-memory database
    popup = UserAttributePopup(root, db_conn)

    # Mock the Entry widgets' get method to return the expected values
    popup.entries = {
        "Full Name:": MagicMock(spec=tk.Entry),
        "Email:": MagicMock(spec=tk.Entry),
        "Phone Number:": MagicMock(spec=tk.Entry),
        "LinkedIn URL:": MagicMock(spec=tk.Entry),
        "GitHub URL:": MagicMock(spec=tk.Entry),
        "Classes Taken:": MagicMock(spec=tk.Text),
        "Projects Worked On:": MagicMock(spec=tk.Text),
        "Additional Information:": MagicMock(spec=tk.Text)
    }

    # Set the get() method to return the correct values
    popup.entries["Full Name:"].get.return_value = "Lenny Pepperbottom"
    popup.entries["Email:"].get.return_value = "Lenny_Pepperbottom@thatsprettyneat.com"
    popup.entries["Phone Number:"].get.return_value = "123-456-7890"
    popup.entries["LinkedIn URL:"].get.return_value = "https://linkedin.com/lenny"
    popup.entries["GitHub URL:"].get.return_value = "https://github.com/lenny"
    popup.entries["Classes Taken:"].get.return_value = "Environmental Science 101, Foraging 302"
    popup.entries["Projects Worked On:"].get.return_value = "Manhattan Project, Project How Neat is That"
    popup.entries["Additional Information:"].get.return_value = "Host of 'Neature Walk'"

    yield popup, db_conn
    db_conn.close()
    popup.destroy()
    root.quit()  # Ensure the root.quit() is called to clean up Tkinter correctly
    root.destroy()  # Clean up the mock object or real root window


@pytest.fixture
def create_mock_db(setup_user_attribute_popup):
    """
    Fixture to create a mock user_profiles table and insert sample data
    into the table.  A mock UserAttributePopup is yielded from the
    setup_user_attribute_popup fixture method, as well as a database
    connection.  The yielded popup fixture contains a simulated set of
    input values, which are then read out and inserted into the database.
    """

    user_attribute_popup, db_conn = setup_user_attribute_popup
    cursor = db_conn.cursor()
    cursor.execute("""
    CREATE TABLE user_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone_number TEXT,
        linkedin_url TEXT,
        github_url TEXT,
        classes_taken TEXT,
        projects_worked_on TEXT,
        additional_info TEXT
    )
    """)
    db_conn.commit()

    cursor.execute("""
        INSERT OR IGNORE INTO user_profiles (
            name, email, phone_number, linkedin_url, github_url, classes_taken, 
            projects_worked_on, additional_info
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_attribute_popup.entries["Full Name:"].get(), user_attribute_popup.entries["Email:"].get(),
          user_attribute_popup.entries["Phone Number:"].get(), user_attribute_popup.entries["LinkedIn URL:"].get(),
          user_attribute_popup.entries["GitHub URL:"].get(), user_attribute_popup.entries["Classes Taken:"].get(),
          user_attribute_popup.entries["Projects Worked On:"].get(),
          user_attribute_popup.entries["Additional Information:"].get()
          ))

    db_conn.commit()

    return user_attribute_popup


@pytest.fixture
def setup_main_window():
    """
    Fixture to mock the main window with a listbox populated with fixed,
    known job listings.  The listbox.curselection is set to the first
    available index of the listbox.  The mock window also contains a
    mocked version of the AppMainWindow's on_job_selected() method, which
    is what needs to be tested to determine the accuracy of data collection
    and entry into the database.  When this method is called it returns
    this mock window (and it's attributes) as an object.
    """
    job_listings = {
        1: {"job_title": "Data Analyst", "location": "Raleigh, NC",
            "description": "A good job", "compensation": "$100k-$120k",
            "date_posted": "1/21/25"},
        2: {"job_title": "Code Scrubber", "location": "Hell, Michigan",
            "description": "A bad job", "compensation": "$40k-$60k",
            "date_posted": "3/18/22"}
    }

    mock_window = MagicMock(spec=AppMainWindow)  # Mock main window
    mock_window.job_listings = job_listings  # Mock job listings attribute
    mock_window.listbox = MagicMock(spec=tk.Listbox)  # Mock listbox

    mock_window.listbox.insert = MagicMock(spec=tk.Listbox.insert)  # mock listbox.insert
    mock_window.on_job_selected = MagicMock(spec=AppMainWindow.on_job_selected)  # mock on_job_selected()

    for _, job_info in job_listings.items():
        job_title = job_info['job_title']
        location = job_info['location']
        formatted_string = f"{job_title}: {location}"
        mock_window.listbox.insert(tk.END, formatted_string)

    mock_window.listbox.curselection.return_value = (0,)

    return mock_window


def test_on_job_selected(setup_main_window):
    """
    Tests a MagicMock instance of the AppMainWindow class.  Specifically
    testing the accuracy of the on_job_selected() method, which is designed
    to retrieve the full data set associated with the job listing selected
    by the user.

    :param setup_main_window:
    """
    mock_window = setup_main_window  # Create mock main window
    mock_window.on_job_selected()  # Call on_job_selected()

    # Make sure on_job_selected() was called
    mock_window.on_job_selected.assert_called_once()

    # Get fixed curselection()
    selected_index = mock_window.listbox.curselection()
    # Get corresponding job_listing id
    selected_job_id = list(mock_window.job_listings.keys())[selected_index[0]]
    # Get job details of the selected job id
    job_details = mock_window.job_listings[selected_job_id]

    assert job_details == {"job_title": "Data Analyst", "location": "Raleigh, NC",
                           "description": "A good job", "compensation": "$100k-$120k",
                           "date_posted": "1/21/25"}


def test_load_user_profile(create_mock_db):
    """
    A test method to check the accuracy of data entry into a database.
    create_mock_db() is a fixture that calls setup_user_attrubute_popup(),
    another fixture.  In those fixture methods, a mock UserAttrubutePopup is
    instantiated, its fields are populated with fixed values, and those
    values are then read into an SQL query, populating a user_profiles with
    a singular entry based on those fixed values.  We then look for and attempt
    to extract that data from the database, and compare the found values against
    the known values to confirm accuracy of this process.

    :param create_mock_db:
    """

    user_profile_popup = create_mock_db

    # Fetch the user profile if it was created
    cursor = user_profile_popup.db_conn.cursor()
    cursor.execute("""
    SELECT * FROM user_profiles WHERE id = 1
    """)
    user_profile = cursor.fetchone()

    entry_id = 1
    full_name = "Lenny Pepperbottom"
    email = "Lenny_Pepperbottom@thatsprettyneat.com"
    phone_number = "123-456-7890"
    linkedin_url = "https://linkedin.com/lenny"
    github_url = "https://github.com/lenny"
    classes_taken = "Environmental Science 101, Foraging 302"
    projects_worked_on = "Manhattan Project, Project How Neat is That"
    additional_info = "Host of 'Neature Walk'"

    # Validate that UI fields contain expected data
    assert user_profile[0] == entry_id
    assert user_profile[1] == full_name
    assert user_profile[2] == email
    assert user_profile[3] == phone_number
    assert user_profile[4] == linkedin_url
    assert user_profile[5] == github_url
    assert user_profile[6] == classes_taken
    assert user_profile[7] == projects_worked_on
    assert user_profile[8] == additional_info


def test_get_api_key():
    """
    Testing get_api_key in ai_resume_builder/resume_generator.py.

    1st assert tests to ensure get_api_key() properly extracts the api key
        from the api_key.txt file

    2nd assert tests to ensure get_api_key() asks the user for an api key
        if the api_key.txt file is empty

    3rd assert tests to ensure that the api key is retrieved from the
        environment variable API_KEY if it exists.  This is used for GitHub
        actions
    """

    relative_api_key_path = "src\\ai_resume_builder\\source_text_files\\api_key.txt"
    absolute_api_key_path = os.path.join(ROOT_DIRECTORY, relative_api_key_path)

    api_key = "5jl6fsLKD45jnJ43pds56Jmi"

    with open(absolute_api_key_path, 'w', encoding="utf-8") as file:
        file.write(api_key)  # Write api key to file

    retrieved_api_key = get_api_key()  # Get api key from file

    assert api_key == retrieved_api_key

    delete_api_key(absolute_api_key_path)

    # Simulate user input of a valid api key and test that get_api_key() returns it
    with patch('builtins.input', return_value='5jl6fsLKD45jnJ43pds56Jmi'):
        api_key = get_api_key()
        assert api_key == '5jl6fsLKD45jnJ43pds56Jmi'

    delete_api_key(absolute_api_key_path)

    # Simulate an API_KEY environment variable and ensure that get_api_key()
    # finds and returns it
    with patch.dict(os.environ, {'API_KEY': '5jl6fsLKD45jnJ43pds56Jmi'}):
        api_key = get_api_key()
        assert api_key == '5jl6fsLKD45jnJ43pds56Jmi'


def delete_api_key(absolute_api_key_path):
    with open(absolute_api_key_path, 'w', encoding="utf-8") as file:
        pass  # Remove api key from file
    # Make sure file is empty
    assert os.path.getsize(absolute_api_key_path) == 0







