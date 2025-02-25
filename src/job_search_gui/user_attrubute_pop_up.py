"""
This is a docstring
"""

import tkinter as tk


class UserAttributePopup(tk.Toplevel):
    """
    This is a docstring
    """
    def __init__(self, parent, database_connection):
        super().__init__(parent)
        self.entries = None
        self.close_button = self.create_buttons()
        self.title("Profile Creation")
        self.geometry("600x800")
        self.db_conn = database_connection
        self.create_input_fields()

    def create_input_fields(self):
        """Creates labeled input fields for user attributes."""
        fields = [
            ("Full Name:", 40),
            ("Email:", 40),
            ("Phone Number:", 40),
            ("LinkedIn URL:", 40),
            ("GitHub URL:", 40)
        ]

        self.entries = {}

        for label_text, width in fields:
            frame = tk.Frame(self)
            frame.pack(fill=tk.X, padx=10, pady=2)

            label = tk.Label(frame, text=label_text, width=20, anchor="w")
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, width=width)
            entry.pack(side=tk.RIGHT, expand=True)
            self.entries[label_text] = entry

        # Multi-line text areas
        self.create_text_area("Classes Taken:")
        self.create_text_area("Projects Worked On:")
        self.create_text_area("Additional Information:")

    def create_text_area(self, label_text):
        """Creates a labeled text widget with a scrollbar."""
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        label = tk.Label(frame, text=label_text, anchor="w")
        label.pack(anchor="w")

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
        self.close_button = tk.Button(button_frame, text="Close", command=self.destroy)
        self.close_button.pack(side=tk.LEFT, padx=10, pady=(0, 0))

        return self.close_button

    def submit_info(self):
        """Placeholder function to handle form submission."""
        cursor = self.db_conn.cursor()

        name = self.entries["Full Name:"].get()
        email = self.entries["Email:"].get()
        phone_number = self.entries["Phone Number:"].get()
        linkedin_url = self.entries["LinkedIn URL:"].get()
        github_url = self.entries["GitHub URL:"].get()
        classes_taken = self.entries["Classes Taken:"].get("1.0", tk.END).strip()
        projects = self.entries["Projects Worked On:"].get("1.0", tk.END).strip()
        additional_info = self.entries["Additional Information:"].get("1.0", tk.END).strip()

        cursor.execute("""
        INSERT OR IGNORE INTO user_profiles(
            name, email, phone_number, linkedin_url, 
            github_url, classes_taken, projects_worked_on, additional_info
        )
        values (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone_number, linkedin_url, github_url,
              classes_taken, projects, additional_info
              ))

        self.db_conn.commit()

        print(name)
        print(email)
        print(phone_number)
        print(linkedin_url)
        print(github_url)
        print(classes_taken)
        print(projects)
        print(additional_info)
