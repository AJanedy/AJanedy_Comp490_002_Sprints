"""
This is a docstring
"""
import tkinter as tk
from src.job_search_gui.job_listing_pop_up_class import JobListingPopUp


class AppMainWindow(tk.Tk):
    """
    This is a docstring
    """
    def __init__(self, database_connection, job_listings):
        super().__init__()
        self.sort_by_location_button = None
        self.sort_by_name_button = None
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.title("Job List")
        self.geometry("800x400")
        self.db_conn = database_connection
        self.job_listings = job_listings
        self.populate_listbox_with_jobs()
        self.create_sort_buttons()
        self.event_handler()

    def event_handler(self):
        """
        This is a docstring
        :return:
        """
        # Bind event for when an item is selected
        self.listbox.bind("<<ListboxSelect>>", self.on_job_selected)
        self.listbox.bind("<Return>", self.on_job_selected)
        self.listbox.bind("<Tab>", self.on_tab_pressed)

    def populate_listbox_with_jobs(self):
        """
        This is a docstring
        :return:
        """
        self.listbox.delete(0, tk.END)
        for _, job_info in self.job_listings.items():
            job_title = job_info['job_title']
            location = job_info['location']

            formatted_string = f"{job_title}: {location}"

            self.listbox.insert(tk.END, formatted_string)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))

    def on_job_selected(self, _):
        """
        This is a docstring
        :return:
        """
        # Get the selected job from the Listbox
        selected_index = self.listbox.curselection()
        if selected_index:
            job_id = list(self.job_listings.keys())[selected_index[0]]
            job_info = self.job_listings[job_id]
            # Open a pop-up window for the selected job
            JobListingPopUp(self, job_info)

    def on_tab_pressed(self):
        """
        This is a docstring
        :return:
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
            return 0  # Prevent the default Tab behavior (to focus on other widgets)
        return 0

    def create_sort_buttons(self):
        """
        This is a docstring
        :return:
        """
        # Create a frame for sorting buttons and align them side by side.
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.LEFT, fill=tk.X, pady=5)

        # Button to close the pop-up window
        self.sort_by_name_button = tk.Button(
            button_frame, text="Sort by Name", command=self.sort_by_name)
        self.sort_by_name_button.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        self.sort_by_location_button = tk.Button(
            button_frame, text="Sort by Location", command=self.sort_by_location)
        self.sort_by_location_button.pack(side=tk.LEFT, expand=True, padx=(10, 5), pady=5)

    def sort_by_name(self):
        """Sort job listings by job title and update the listbox."""
        self.job_listings = dict(sorted(self.job_listings.items(),
                                        key=lambda item: item[1]['job_title']))
        self.populate_listbox_with_jobs()

    def sort_by_location(self):
        """Sort job listings by location and update the listbox."""
        self.job_listings = dict(reversed(sorted(self.job_listings.items(),
                                                 key=lambda item: item[1]['location'])))
        self.populate_listbox_with_jobs()
