"""
This module defines a class to represent a popup window that will display all
job listing details in a graphical user interface.

JobListingPopUp is a Toplevel window that provides a detailed description of
a selected job listing.
"""
import tkinter as tk
from src.job_search_gui.profile_selection_popup_class import ProfileSelectionPopup


class JobListingPopup(tk.Toplevel):
    """
    Instantiating this class creates a Toplevel window used to display
    the job details about a specific job listing.

    Attributes:
        - close_button: A button to close the window
        - text_widget: A text window to display the job info

    Methods:
        - __init__(parent, job_info): Initializes the window with job info
        - create_close_button: Creates a close button for the window
        - create_label(job_info): Creates a label that displays the job title
        - create_frame(): Makes a frame to hold the text_widget
        - create_text_widget(): Creates the widget and fills it with job details
    """
    def __init__(self, parent, job_info, database_connection):
        super().__init__(parent)
        self.profile_button = None
        self.close_button = None
        self.create_buttons()
        self.job_title = job_info['job_title']
        self.title(f"Job Listing Details for {self.job_title}")
        self.company = job_info['company']
        self.geometry("600x500")
        self.create_label(job_info)
        self.frame = self.create_frame()
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, width=70, height=20)
        self.create_text_widget(job_info)
        self.db_conn = database_connection
        self.relevant_job_info = (f"Company: {self.company}\n"
                                  f"Job Title: {self.job_title}\n"
                                  f"Location: {job_info['location']}\n"
                                  f"Description: {job_info['description']}")

    def create_text_widget(self, job_info):
        """
        Creates and populates a text widget with job details

        Args:
            job_info (dict)

        :param job_info:
        """

        # Create the Text widget (for job details)
        self.text_widget.insert(tk.END, f"Company: {job_info['company']}\n\n"
                                    f"Location: {job_info['location']}\n\n"
                                    f"Date Posted: {job_info['date_posted']}\n\n"
                                    f"Description: {job_info['description']}\n\n"
                                    f"Employment Type: {job_info['employment_type']}\n\n"
                                    f"Compensation ({job_info['interval']}): "
                                        f"{job_info['compensation']}\n\n"
                                    f"Job URL: {job_info['job_url']}")
        self.text_widget.config(state=tk.DISABLED)  # Make text widget read-only
        self.text_widget.pack(side=tk.LEFT, padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

    def create_frame(self):
        """
        A method to create a frame to hold a text widget
        """
        # Create a frame to hold the Text widget and scrollbar
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def create_label(self, job_info):
        """
        A method to create a label out of the job title from a given listing

        Args:
            job_info (dict)
        """
        # Label to show the job title
        label = tk.Label(self, text=f"{job_info['job_title']}")
        label.pack(pady=20)

    def select_profile(self):
        """
        Opens the profile selection popup and receives the selected profile.
        """

        ProfileSelectionPopup(self)

    def create_buttons(self):
        """
        A method to create a close button at the bottom of each window so the
        user can exit each window as well as a button to select a previously
        submitted user profile
        """
        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)  # Pack at the bottom with spacing

        # Button to select a user profile
        self.profile_button = tk.Button(button_frame, text="Select User Profile", command=self.select_profile)
        self.profile_button.pack(side=tk.LEFT, padx=10, pady=(0, 0))

        # Button to close the pop-up window
        self.close_button = tk.Button(button_frame, text="Close", command=self.destroy)
        self.close_button.pack(side=tk.LEFT, padx=10, pady=(0, 0))

        return self.close_button
