"""
A class to represent the main window of a job listing GUI
"""
import tkinter as tk
from src.job_search_gui.job_listing_pop_up_class import JobListingPopup
from src.job_search_gui.user_attribute_popup import UserAttributePopup


class AppMainWindow(tk.Tk):
    """
    Instantiating this class creates the main level window for the job listing
    GUI.  This window will create a listbox that contains all job listings
    and their location retrieved from a database connection.  It also contains
    functionalities for sorting job listings and closing the application.

    Attributes:
        - database_connection: A database connection object used to retrieve job listings.
        - job_listings (list): A list of job listings, each being represented by a
            dictionary containing job info.
        - sort_by_location_button (tk.Button): A button to sort job listings by location
        - sort_by_name_button (tk.Button): A button to sort job listings by name
        - close_button (tk.Button): A button to close the window
        - listbox (tk.Listbox): A listbox to display the job listings

    Methods:
        - __init__(database_connection, job_listings): Initialize the window, populated the
            listbox, create sort and close buttons.
        - populate_listbox(): Populates the lisbox with jobs from the 'job_listings' list
            attribute.
        - create_buttons(): Creates buttons for sorting as well as the close button
        - event_handler(): Registers event handlers (buttons clicks, listbox selection, etc.).
    """

    def __init__(self, database_connection, job_listings):
        super().__init__()
        self.sort_by_location_button = None
        self.sort_by_name_button = None
        self.user_data_collection_button = None
        self.close_button = None
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, activestyle='none')
        self.title("Job List")
        self.geometry("800x400")
        self.db_conn = database_connection
        self.job_listings = job_listings
        self.populate_listbox()
        self.create_buttons()
        self.event_handler()

    def event_handler(self):
        """
        Event handler for the popup window.  Registers interactions with the
        job listings listbox.

        Events handled:
            - "<<ListboxSelect>>": Triggers a selected job listing.
            - "<Return>": Triggers a job selection when enter is pressed.
            - "<Tab>": Cycles through listbox and buttons.
            - "<Up>" and "<Down>": Allows navigation through the listbox
        """
        # Bind event for when an item is selected
        self.listbox.bind("<<ListboxSelect>>", self.on_job_selected)
        self.listbox.bind("<Return>", self.on_job_selected)
        self.listbox.bind("<Tab>", self.on_tab_pressed)
        self.listbox.bind("<Up>", self.navigate)
        self.listbox.bind("<Down>", self.navigate)

    def populate_listbox(self):
        """
        Populates the listbox with job listings after initially clearing the
        existing entries in the listbox.  Job postings will be displayed in
        the format job title: location.
        """
        # Clear the listbox
        self.listbox.delete(0, tk.END)

        # Add all jobs to the listbox
        for _, job_info in self.job_listings.items():
            job_title = job_info['job_title']
            location = job_info['location']
            formatted_string = f"{job_title}: {location}"
            self.listbox.insert(tk.END, formatted_string)

        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))

    def navigate(self, event):
        """
        Navigates through the listbox using up and down arrow keys.
        :param event: The event triggered by keypress (Up or Down).
        """
        current_selection = self.listbox.curselection()  # Get current selection

        if not current_selection:
            current_selection = (0,)  # If no item is selected, start from the first item

        index = current_selection[0]  # Get the index of the selected item

        if event.keysym == 'Up':  # Check if the Up Arrow key is pressed
            index = index - 1 if index > 0 else len(self.job_listings) - 1
        elif event.keysym == 'Down':  # Check if the Down Arrow key is pressed
            index = index + 1 if index < len(self.job_listings) - 1 else 0

        self.listbox.select_clear(0, tk.END)  # Clear any previous selection
        self.listbox.select_set(index)  # Select the new item
        self.listbox.activate(index)  # Ensure the item is highlighted

    def on_job_selected(self, _):
        """
        A method to instantiate a JobListingPopUp window on the selection
        of a job in the listbox.
        """
        # Get the selected job from the Listbox
        selected_index = self.listbox.curselection()

        if selected_index:
            job_id = list(self.job_listings.keys())[selected_index[0]]
            job_info = self.job_listings[job_id]
            # Open a pop-up window for the selected job
            JobListingPopup(self, job_info)

    def on_tab_pressed(self, _):
        """
        A method to navigate through actionable parts of the main window. Tab
        will cycle through the listbox as well as each button in the button
        frame.  Shift-tab will cycle through those items in reverse.
        """
        # Move the focus to the next item in the Listbox when Tab is pressed
        current_selection = self.listbox.curselection()
        if not current_selection:
            # If nothing is selected, select the first item
            self.listbox.activate(0)
            self.listbox.select_set(0)
        else:
            # Move selection to the next item and wrap around at the end
            next_index = (current_selection[0] + 1) % len(self.job_listings)
            self.listbox.select_clear(0, tk.END)  # Clear all selections
            self.listbox.select_set(next_index)  # Set the next item as selected
            self.listbox.activate(next_index)

            self.listbox.see(next_index)

        self.listbox.focus_set()

    def create_buttons(self):
        """
        Creates a button frame to hold the buttons and creates each button
        and puts them into the frame.
        """
        # Create a frame for sorting buttons and align them side by side.
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.LEFT, fill=tk.X, pady=5)

        self.sort_by_location_button = tk.Button(
            button_frame, text="Sort by Location", command=self.sort_by_location)
        self.sort_by_location_button.pack(
            side=tk.LEFT, expand=True, padx=(10, 5), pady=5)

        self.sort_by_name_button = tk.Button(
            button_frame, text="Sort by Name", command=self.sort_by_name)
        self.sort_by_name_button.pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)

        self.user_data_collection_button = tk.Button(
            button_frame, text="Make Profile", command=self.make_profile)
        self.user_data_collection_button.pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)

        self.close_button = tk.Button(
            button_frame, text="Close", command=self.destroy)
        self.close_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def sort_by_name(self):
        """Sort job listings by job title and update the listbox."""
        self.job_listings = dict(sorted(self.job_listings.items(),
                                        key=lambda item: item[1]['job_title']))
        self.populate_listbox()

    def sort_by_location(self):
        """Sort job listings by location and update the listbox."""
        self.job_listings = dict(reversed(sorted(self.job_listings.items(),
                                                 key=lambda item: item[1]['location'])))
        self.populate_listbox()

    def make_profile(self):
        """Create a popup window for the user to create a profile"""
        UserAttributePopup(self, self.db_conn)
