"""
This is a docstring
"""
import tkinter as tk


class JobListingPopUp(tk.Toplevel):
    """
    This is a docstring
    """
    def __init__(self, parent, job_info):
        super().__init__(parent)
        self.close_button = None
        self.title(f"Job Listing Details for {job_info['job_title']}")
        self.geometry("600x500")
        self.create_label(job_info)
        frame = self.create_frame()
        self.text_widget = tk.Text(frame, wrap=tk.WORD, width=70, height=20)
        self.create_text_widget(frame, job_info)
        self.create_close_button()

    def create_text_widget(self, frame, job_info):
        """
        This is a docstring
        :param frame:
        :param job_info:
        :return:
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
        self.text_widget.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    def create_frame(self):
        """
        This is a docstring
        :return:
        """
        # Create a frame to hold the Text widget and scrollbar
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def create_label(self, job_info):
        """
        This is a docstring
        :param job_info:
        :return:
        """
        # Label to show the job title
        label = tk.Label(self, text=f"{job_info['job_title']}")
        label.pack(pady=20)

    def create_close_button(self):
        """
        This is a docstring
        :return:
        """
        # Button to close the pop-up window
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)
