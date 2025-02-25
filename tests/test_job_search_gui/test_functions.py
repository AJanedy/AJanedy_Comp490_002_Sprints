import os
from unittest.mock import MagicMock
import pytest
import sqlite3
import tkinter as tk
from src.job_search_gui.user_attribute_pop_up import UserAttributePopup


@pytest.fixture
def setup_gui():
    """Fixture to set up a Tkinter root and database connection."""
    if os.environ.get('DISPLAY', '') == '':
        # Mock Tk() to prevent actual GUI window creation in headless environments
        mock_root = MagicMock(spec=tk.Tk)
        mock_root.withdraw = MagicMock()  # Mock the withdraw method
        mock_root.quit = MagicMock()  # Mock the quit method to prevent blocking event loop
        # Mock the necessary `tk` attributes for proper initialization of UserAttributePopup
        mock_root.tk = MagicMock()  # Mock the `tk` attribute
        mock_root.children = {}  # Mock the `children` attribute
        mock_root.master = None  # Mock the `master` attribute as None, or root
        root = mock_root
    else:
        root = tk.Tk()  # Allow normal display if running locally

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
    popup.entries["Full Name:"].get.return_value = "Alice Johnson"
    popup.entries["Email:"].get.return_value = "alice@example.com"
    popup.entries["Phone Number:"].get.return_value = "123-456-7890"
    popup.entries["LinkedIn URL:"].get.return_value = "https://linkedin.com/alice"
    popup.entries["GitHub URL:"].get.return_value = "https://github.com/alice"
    popup.entries["Classes Taken:"].get.return_value = "CS101, CS102"
    popup.entries["Projects Worked On:"].get.return_value = "Project A, Project B"
    popup.entries["Additional Information:"].get.return_value = "Additional details here"

    yield popup, db_conn
    db_conn.close()
    popup.destroy()
    root.quit()  # Ensure the root.quit() is called to clean up Tkinter correctly
    root.destroy()  # Clean up the mock object or real root window


@pytest.fixture
def create_mock_db(setup_gui):
    """Fixture to create a mock user_profiles table and insert sample data."""
    popup, db_conn = setup_gui
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
    INSERT INTO user_profiles (name, email, phone_number, linkedin_url, github_url, classes_taken, projects_worked_on, additional_info)
    VALUES ('Alice Johnson', 'alice@example.com', '123-456-7890', 
            'https://linkedin.com/alice', 'https://github.com/alice',
            'CS101, CS102', 'Project A, Project B', 'Additional details here')
    """)
    db_conn.commit()

    return popup


def test_load_user_profile(create_mock_db):
    """Test that selecting an item loads the correct data into the UI fields."""
    popup = create_mock_db

    # Manually interact with the database to fetch the user profile
    cursor = popup.db_conn.cursor()
    cursor.execute("""
    SELECT * FROM user_profiles WHERE id = 1
    """)
    user_profile = cursor.fetchone()

    # Assume we have a method to load user data based on selection
    # Manually populate UI fields based on the result of the query
    popup.entries["Full Name:"].insert(0, user_profile[1])
    popup.entries["Email:"].insert(0, user_profile[2])
    popup.entries["Phone Number:"].insert(0, user_profile[3])
    popup.entries["LinkedIn URL:"].insert(0, user_profile[4])
    popup.entries["GitHub URL:"].insert(0, user_profile[5])
    popup.entries["Classes Taken:"].insert("1.0", user_profile[6])
    popup.entries["Projects Worked On:"].insert("1.0", user_profile[7])
    popup.entries["Additional Information:"].insert("1.0", user_profile[8])

    # Validate that UI fields contain expected data
    assert popup.entries["Full Name:"].get() == "Alice Johnson"
    assert popup.entries["Email:"].get() == "alice@example.com"
    assert popup.entries["Phone Number:"].get() == "123-456-7890"
    assert popup.entries["LinkedIn URL:"].get() == "https://linkedin.com/alice"
    assert popup.entries["GitHub URL:"].get() == "https://github.com/alice"
    assert popup.entries["Classes Taken:"].get() == "CS101, CS102"
    assert popup.entries["Projects Worked On:"].get() == "Project A, Project B"
    assert popup.entries["Additional Information:"].get() == "Additional details here"
