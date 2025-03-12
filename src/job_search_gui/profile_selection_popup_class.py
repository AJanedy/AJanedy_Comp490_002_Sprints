"""
This module defines the ProfileSelectioPopup class to display a list of
previously submitted user profiles.  After selection of a profile, the user
can choose to generate a resume and cover letter based on the previously
selected job listing, and the selected profile.
"""

import tkinter as tk
from src.job_search_gui.generate_resume_and_cover_letter import generate_documents


class ProfileSelectionPopup(tk.Toplevel):
    """
    A popup window to allow users to select a profile from the database.

    Key Attributes:
        - parent: The parent window is the job_listing_popup window
        - db_conn: The database connection
        - listbox: A Tkinter Listbox widget to display profiles

    Methods:
        - fetch_profiles: Retrieves profiles from the database
        - on_select: Handles profile selection and closes the popup
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select a Profile")
        self.geometry("400x300")
        self.db_conn = parent.db_conn
        self.relevant_job_info = parent.relevant_job_info
        self.company = parent.job_info['company']
        self.job_title = parent.job_info['job_title']
        self.user_profile = None
        self.profile_name = None

        # Popup window label
        label = tk.Label(self, text="Select a Profile:")
        label.pack(pady=10)

        # Listbox to display profiles
        self.listbox = tk.Listbox(self)
        self.listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # A button representing the final query to create a custom resume and cover letter
        select_button = tk.Button(self, text="Create Resume and Cover Letter",
                                  command=self.on_select)
        select_button.pack(pady=5)  # Button padding

        # Fetch and display profiles
        self.fetch_profiles()

    def fetch_profiles(self):
        """
        Fetches user profiles from the database and populates the listbox.
        """

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT profile_name FROM user_profiles")  # Get all user profiles from database
        profiles = cursor.fetchall()

        # Insert profile names (identifier) into the listbox
        for profile in profiles:
            self.listbox.insert(tk.END, *profile)

    def on_select(self):
        """
        Retrieves the data associated with the selected profile, formats that
        information into a structured string, assigns it to the class attribute
        user_profile, then calls generate_documents to have Google Gemini AI
        use the job listing and the user profile to create targeted resume
        and cover letter
        """
        selected_profile = self.listbox.get(tk.ACTIVE)  # Retrieve the selected item (job listing)
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE profile_name = ?", (selected_profile,))

        profile = cursor.fetchall()
        profile = profile[0]

        self.user_profile = (f"Name: {profile[1]}\n"
                               f"Email: {profile[3]}\n"
                               f"Phone Number: {profile[4]}\n"
                               f"LinkedIn: {profile[5]}\n"
                               f"GitHub: {profile[6]}\n"
                               f"Classes Taken: {profile[7]}\n"
                               f"Projects Worked On: {profile[8]}\n"
                               f"Additional Info: {profile[9]}")

        self.profile_name = profile[2]

        generate_documents(self)
