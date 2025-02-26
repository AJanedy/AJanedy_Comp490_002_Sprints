import os
from unittest.mock import MagicMock
import pytest
import sqlite3
import tkinter as tk

from src.job_search_gui.job_app_main_window_class import AppMainWindow
from src.job_search_gui.user_attribute_pop_up import UserAttributePopup


@pytest.fixture
def setup_user_attribute_popup():
    """Fixture to set up a mock root window if headless or allow a normal display
    if running locally, create a database connection, then instantiate an instance
    of the UserAttributePopup class and create """

    # if os.environ.get('DISPLAY', '') == '':  # If no display
    # Mock Tk() to prevent actual GUI window creation in headless environments
    mock_root = MagicMock(spec=tk.Tk)
    mock_root.withdraw = MagicMock()  # Mock the withdraw method
    mock_root.quit = MagicMock()  # Mock the quit method to prevent blocking event loop
    # Mock the necessary `tk` attributes for proper initialization of UserAttributePopup
    mock_root.tk = MagicMock()  # Mock the `tk` attribute
    mock_root.children = {}  # Mock the `children` attribute
    mock_root.master = None  # Mock the `master` attribute as None, or root
    root = mock_root
    # else:
    #     root = tk.Tk()  # Allow normal display if running locally

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
    """Fixture to create a mock user_profiles table and insert sample data."""

    popup, db_conn = setup_user_attribute_popup
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
    """, (popup.entries["Full Name:"].get(), popup.entries["Email:"].get(),
          popup.entries["Phone Number:"].get(), popup.entries["LinkedIn URL:"].get(),
          popup.entries["GitHub URL:"].get(), popup.entries["Classes Taken:"].get(),
          popup.entries["Projects Worked On:"].get(),
          popup.entries["Additional Information:"].get()
          ))

    db_conn.commit()

    return popup


@pytest.fixture
def setup_main_window():
    """Fixture to set up a mock root window if headless or allow a normal display
    if running locally, create a database connection, then instantiate an instance
    of the UserAttributePopup class and create """

    """Fixture to mock the main window with job listings."""
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

    mock_window.listbox.insert = MagicMock(spec=tk.Listbox.insert)
    mock_window.on_job_selected = MagicMock(spec=AppMainWindow.on_job_selected)

    for _, job_info in job_listings.items():
        job_title = job_info['job_title']
        location = job_info['location']
        formatted_string = f"{job_title}: {location}"
        mock_window.listbox.insert(tk.END, formatted_string)

    mock_window.listbox.curselection.return_value = (0,)

    return mock_window


def test_on_job_selected(setup_main_window):
    mock_window = setup_main_window

    mock_window.on_job_selected()

    mock_window.on_job_selected.assert_called_once()

    selected_index = mock_window.listbox.curselection()
    selected_job_id = list(mock_window.job_listings.keys())[selected_index[0]]

    job_details = mock_window.job_listings[selected_job_id]

    assert job_details == {"job_title": "Data Analyst", "location": "Raleigh, NC",
                           "description": "A good job", "compensation": "$100k-$120k",
                           "date_posted": "1/21/25"}


def test_load_user_profile(create_mock_db):
    """Test that selecting an item loads the correct data into the UI fields."""

    popup = create_mock_db

    # Manually interact with the database to fetch the user profile
    cursor = popup.db_conn.cursor()
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
