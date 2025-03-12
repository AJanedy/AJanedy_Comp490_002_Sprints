"""
The module defines the JobListingPopup class.  The class creates a popup window
that displays all available information regarding a chosen job posting in a database
of job listings.

The popup also allows a user to select a user profile from a list of previously
submitted profiles that can then be used in combination with the job information
to make a request to Google Gemini AI to create a resume and cover letter
specifically designed for that job.
"""

import tkinter as tk
from src.job_search_gui.profile_selection_popup_class import ProfileSelectionPopup


class JobListingPopup(tk.Toplevel):
    """
    Instantiating this class creates a Toplevel window used to display
    the job details about a specific job listing.

    Key Attributes:
        - job_info: A dictionary containing job details.
        - db_conn: Database connection to fetch related data.

    Key Methods:
        - create_buttons: Creates buttons for profile selection and closing the window.
        - select_profile: Instantiates an instance of ProfileSelectionPopup.
        - get_all_job_info: Gets all associated attributes of a given job listing.
        - get_relevant_info: Gets specific info relevant for creating targeted resumes.
    """

    def __init__(self, parent, job_info, database_connection):
        super().__init__(parent)
        self.db_conn = database_connection
        self.job_info = job_info
        self.relevant_job_info = get_relevant_info(self.job_info)
        self.create_buttons()
        self.title(f"Job Listing Details for {self.job_info['job_title']}")
        self.create_label()
        self.frame = self.create_frame()
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, width=70, height=20)
        self.create_text_widget()

    def create_text_widget(self):
        """
        Populates the read-only text widget with all available job info
        :return:
        """
        all_job_info = get_all_job_info(self.job_info)

        self.text_widget.insert(tk.END, all_job_info)
        self.text_widget.config(state=tk.DISABLED)  # Make text widget read-only
        self.text_widget.pack(side=tk.LEFT, padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

    def create_frame(self):
        """
        Creates and returns a frame that will hold the text widget used for displaying
        the job info of a chosen job listing

        :return frame:
        """
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def create_label(self):
        """ Creates a label for the JobListingPopup """
        label = tk.Label(self, text=f"{self.job_info['job_title']}")
        label.pack(pady=20)

    def select_profile(self):
        """ Instantiates a ProfileSelectionPopup """
        ProfileSelectionPopup(self)

    def create_buttons(self):
        """
        Method to create the buttons for selecting a user profile and closing the window
        """
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Button to select a user profile
        profile_button = tk.Button(button_frame, text="Select User Profile",
                                   command=self.select_profile)
        profile_button.pack(side=tk.LEFT, padx=10, pady=(0, 0))

        # Button to close the pop-up window
        close_button = tk.Button(button_frame, text="Close", command=self.destroy)
        close_button.pack(side=tk.LEFT, padx=10, pady=(0, 0))


def get_all_job_info(job_info):
    """
        Formats the relevant job details into a string, this will be used to help
        formulate our query to Google Gemini AI
        :param job_info:
        :return String:
        """
    return (f"Company: {job_info['company']}\n\n"
                f"Location: {job_info['location']}\n\n"
                f"Date Posted: {job_info['date_posted']}\n\n"
                f"Description: {job_info['description']}\n\n"
                f"Employment Type: {job_info['employment_type']}\n\n"
                f"Compensation ({job_info['interval']}): {job_info['compensation']}\n\n"
                f"Job URL: {job_info['job_url']}")


def get_relevant_info(job_info):
    """
    Formats the relevant job details into a string, this will be used to help
    formulate our query to Google Gemini AI
    :param job_info:
    :return String:
    """
    return (f"Company: {job_info['company']}\n\n"
            f"Location: {job_info['location']}\n\n"
            f"Description: {job_info['description']}\n\n")
