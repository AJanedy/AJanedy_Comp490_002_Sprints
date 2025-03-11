import tkinter as tk
from src.job_search_gui.generate_resume_and_cover_letter import generate_resume_and_cover_letter


class ProfileSelectionPopup(tk.Toplevel):
    """
    A popup window to allow users to select a profile from the database.

    Attributes:
        - parent: The parent Tkinter window
        - callback: A function to handle the selected profile
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
        self.company = parent.company
        self.job_title = parent.job_title
        self.user_profile = None
        self.profile_name = None

        # Label
        label = tk.Label(self, text="Select a Profile:")
        label.pack(pady=10)

        # Listbox to display profiles
        self.listbox = tk.Listbox(self)
        self.listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Select button
        select_button = tk.Button(self, text="Create Resume and Cover Letter", command=self.on_select)
        select_button.pack(pady=5)

        # Fetch and display profiles
        self.fetch_profiles()

    def fetch_profiles(self):
        """
        Fetches user profiles from the database and populates the listbox.
        """

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM user_profiles")  # Assuming table 'user_profiles' exists
        profiles = cursor.fetchall()

        # Insert profiles into the listbox
        for profile in profiles:
            self.listbox.insert(tk.END, profile[2])

    def on_select(self):
        """
        Retrieves the selected profile and passes it to the callback function.
        """
        selected_profile = self.listbox.get(tk.ACTIVE)
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE profile_name = ?", (selected_profile,))

        raw_profile = cursor.fetchall()
        raw_profile = raw_profile[0]

        self.user_profile = (f"Name: {raw_profile[1]}\n"
                               f"Email: {raw_profile[3]}\n"
                               f"Phone Number: {raw_profile[4]}\n"
                               f"LinkedIn: {raw_profile[5]}\n"
                               f"GitHub: {raw_profile[6]}\n"
                               f"Classes Taken: {raw_profile[7]}\n"
                               f"Projects Worked On: {raw_profile[8]}\n"
                               f"Additional Info: {raw_profile[9]}")

        self.profile_name = raw_profile[2]

        generate_resume_and_cover_letter(self)
