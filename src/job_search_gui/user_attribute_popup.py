"""
This module creates a graphical user interface popup used for
collecting a user profile in relation to a job search.

The GUI popup is a form for users to input personal details
that would be relevant on a resume.  The data collected is
stored to the same database used for organizing the job
listings presented in the main window of this application.
"""
import tkinter as tk


class UserAttributePopup(tk.Toplevel):
    """
    A popup GUI used to collect user attributes

    This is a Toplevel window with labeled input fields used
    to collect user details such as name, email, phone number,
    LinkedIn and GitHub URLs, courses taken, applicable projects,
    and other relevant information.

    Key Attributes:
        - db_conn: A database connection object
        - entries: A dictionary mapping the GUI input labels to the
            input given by the user.

    Key Methods:
        - create_input_fields(): Creates the labeled entry fields for the
            user to enter attributes.
        - create_text_area(label_text): Used to create multiple, multi-line
            input fields.
        - create_buttons(): Used to create the close and submit buttons
        - submit_info(): A method to submit user info to the database
    """
    def __init__(self, parent, database_connection):
        super().__init__(parent)
        self.entries = None
        self.title("Profile Creation")
        self.geometry("600x800")
        self.db_conn = database_connection
        self.create_buttons()
        self.create_input_fields()

    def create_input_fields(self):
        """ Creates labeled input fields for user attributes. """

        fields = [
            ("Full Name:", 40),
            ("Profile Name:", 40),
            ("Email:", 40),
            ("Phone Number:", 40),
            ("LinkedIn URL:", 40),
            ("GitHub URL:", 40)
        ]

        self.entries = {}  # A dictionary to hold user entries

        for label_text, width in fields:
            frame = tk.Frame(self)  # Create Frame widget.
            # Stretch frame to fit window with padding
            frame.pack(fill=tk.X, padx=10, pady=2)

            # Create a label for each field in the frame, align left
            label = tk.Label(frame, text=label_text, width=20, anchor="w")
            label.pack(side=tk.LEFT)

            # Creates an entry widget, aligns it to the right of the frame,
            # and saves the user entry to the self.entries dictionary
            entry = tk.Entry(frame, width=width)
            entry.pack(side=tk.RIGHT, expand=True)
            self.entries[label_text] = entry

        # Multi-line text areas
        self.create_text_area("Classes Taken:")
        self.create_text_area("Projects Worked On:")
        self.create_text_area("Additional Information:")

    def create_text_area(self, label_text):
        """ Creates a labeled text widget. """

        frame = tk.Frame(self)  # Create a frame widget
        # Stretch the frame to fit the window with padding
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create a label for each field in the frame, align left
        label = tk.Label(frame, text=label_text, anchor="w")
        label.pack(anchor="w")

        # Create a multiline text box that fills the frame and saves
        # the user entry to the self.entries dictionary
        text_widget = tk.Text(frame, wrap=tk.WORD, height=5)
        text_widget.pack(fill=tk.BOTH, expand=True)
        self.entries[label_text] = text_widget

    def create_buttons(self):
        """
        A method to create a close button at the bottom of each window so the
        user can exit each window.
        """
        # Create a frame for sorting buttons and align them side by side.
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Submit button
        submit_button = tk.Button(button_frame, text="Submit", command=self.submit_info)
        submit_button.pack(side=tk.LEFT, padx=10, pady=(0, 0))

        # Button to close the pop-up window
        close_button = tk.Button(button_frame, text="Close", command=self.destroy)
        close_button.pack(side=tk.LEFT, padx=10, pady=(0, 0))

    def submit_info(self):
        """
        A method to handle user profile submission to the database.
        """
        cursor = self.db_conn.cursor()

        name = self.entries["Full Name:"].get()
        profile_name = self.entries["Profile Name:"].get()
        email = self.entries["Email:"].get()
        phone_number = self.entries["Phone Number:"].get()
        linkedin_url = self.entries["LinkedIn URL:"].get()
        github_url = self.entries["GitHub URL:"].get()
        classes_taken = self.entries["Classes Taken:"].get("1.0", tk.END).strip()
        projects = self.entries["Projects Worked On:"].get("1.0", tk.END).strip()
        additional_info = self.entries["Additional Information:"].get("1.0", tk.END).strip()

        cursor.execute("""
        INSERT OR IGNORE INTO user_profiles(
            name, profile_name, email, phone_number, linkedin_url, 
            github_url, classes_taken, projects_worked_on, additional_info
        )
        values (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, profile_name, email, phone_number, linkedin_url, github_url,
              classes_taken, projects, additional_info
              ))

        self.db_conn.commit()
        self.destroy()
