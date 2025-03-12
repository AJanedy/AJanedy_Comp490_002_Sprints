"""
A module to generate resumes and cover letters by leveraging AI content
generation.  generate_resume_and_cover_letter() will get the user profile
and job listing information, format a query to generate a cover letter
and a resume based on that information, and then query Google Gemini AI
to create those documents.

Key Methods:
    - generate_resume_and_cover_letter(parent): The entry point of this module;
      fetches user_profile, job_listing, api_key, and the relevant queries,
      then calls two helper functions (listed below) to make a query to
      Google Gemini AI and convert that feedback to a PDF to be stored in
      the resume_and_cover_letters directory
    - query_ai(api_key, query): Sends a query to Google Gemini AI to generate
      content and return a response.
    - generate_pdf(): Formats the AI generated content into a structured, readable
      format, then saves the PDF to resume_and_cover_letters.
"""

import os
import re
import google.generativeai as genai
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.ai_resume_builder.resume_generator import get_api_key


# ...\AJanedy_Comp490_002_Sprints\src\job_search_gui
script_directory = os.path.dirname(os.path.abspath(__file__))
# \AJanedy_Comp490_002_Sprints\src\ai_resume_builder\resumes_and_cover_letters
resume_and_cover_letter_directory = os.path.join(script_directory, "resumes_and_cover_letters")

# Constants for layout.
# This is an extension of the AI assisted code from pdf_formatting()
MARGIN_LEFT = 40
MARGIN_TOP = 750
LINE_HEIGHT = 12  # Spacing between lines
PAGE_HEIGHT = letter[1]
PARAGRAPH_SPACING = 10
BOTTOM_MARGIN = 50  # Margin before starting a new page
MAX_WIDTH = 520  # Max text width before wrapping


def generate_documents(parent):
    """
    Generates a resume and cover letter based on the user's chosen profile
    and the selected job listing.  A PDF is then created for each of those
    generated documents and saved to resumes_and_cover_letters.

    :param parent:
    """
    # Make the directory if it does not exist
    if not os.path.exists(resume_and_cover_letter_directory):
        os.mkdir(resume_and_cover_letter_directory)

    user_profile = parent.user_profile
    job_listing = parent.relevant_job_info

    api_key = get_api_key()
    resume_query = get_resume_query(user_profile, job_listing)
    cover_letter_query = get_cover_letter_query(user_profile, job_listing)

    resume = query_ai(api_key, resume_query).text
    cover_letter = query_ai(api_key, cover_letter_query).text

    generate_pdf(resume, parent, "resume")
    generate_pdf(cover_letter, parent, "cover_letter")


def get_resume_query(user_profile, job_listing):
    """
    Constructs a query based on the chosen user profile and job listing that will
    be sent to Google Gemini AI to construct a resume.

    :param user_profile:
    :param job_listing:
    :return resume_query:
    """
    resume_prompt = ("Given the job description and the information I have "
                     "provided about myself, please write me a sample resume "
                     "in markdown format that is specifically designed around "
                     "my skills and the job description provided.")

    resume_query = (f"Job Description: {job_listing}\n\n"
                    f"Personal Information: {user_profile}\n\n"
                    f"{resume_prompt}")

    return resume_query


def get_cover_letter_query(user_profile, job_listing):
    """
        Constructs a query based on the chosen user profile and job listing that will
        be sent to Google Gemini AI to construct a cover letter.

        :param user_profile:
        :param job_listing:
        :return resume_query:
        """
    cover_letter_prompt = ("Given the job description and the information I have "
                           "provided about myself, please write me a sample cover letter "
                           "in markdown format that is specifically designed around "
                           "my skills and the job description provided.")

    cover_letter_query = (f"Job Description: {job_listing}\n\n"
                          f"Personal Information: {user_profile}\n\n"
                          f"{cover_letter_prompt}")

    return cover_letter_query


def generate_pdf(content, parent, letter_or_resume):
    """
    A method to generate an HTML formatted document, cleans that document
    of HTML markers, formats it to a clean and human-readable structure,
    then converts it to a PDF and saves it to resumes_and_cover_letters

    :param content:
    :param parent:
    :param letter_or_resume:
    :return:
    """

    # Convert to HTML format then clean HTML markers
    cleaned_content = clean_html(content)

    # Add "_" to company and job title for file naming
    company, job_title = format_job_for_filename(parent)

    # Construct the filepath for the new .pdf file
    file_path = get_filepath(company, job_title, letter_or_resume)

    # Create a blank canvas object for the PDF
    pdf_canvas = canvas.Canvas(file_path, pagesize=letter)

    # Set font
    pdf_canvas.setFont("Helvetica", 10)

    # Format text
    pdf_formatting(cleaned_content, pdf_canvas)

    # Save the PDF
    pdf_canvas.save()


def pdf_formatting(cleaned_content, pdf_canvas):
    """
    This method was written with the assistance of Google Gemini AI
    to quickly format text into a structured, readable format.

    :param cleaned_content:
    :param pdf_canvas:
    :return:
    """
    def wrap_text(text, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            if pdf_canvas.stringWidth(test_line, "Helvetica", 10) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)  # Add the last line
        return lines

    # Track vertical position for text placement
    y_position = MARGIN_TOP
    # Process each paragraph separately
    paragraphs = cleaned_content.split("\n")  # Use single newline to separate lines properly
    for paragraph in paragraphs:
        if not paragraph.strip():
            y_position -= PARAGRAPH_SPACING  # Add space between paragraphs
            continue  # Skip empty paragraphs

        wrapped_lines = wrap_text(paragraph, MAX_WIDTH)

        for wrapped_line in wrapped_lines:
            if y_position < BOTTOM_MARGIN:  # If at bottom, start a new page
                pdf_canvas.showPage()
                pdf_canvas.setFont("Helvetica", 10)
                y_position = MARGIN_TOP  # Reset y_position for the new page

            pdf_canvas.drawString(MARGIN_LEFT, y_position, wrapped_line)
            y_position -= LINE_HEIGHT  # Move down for the next line

        y_position -= PARAGRAPH_SPACING  # Add space after each paragraph


def get_filepath(company, job_title, letter_or_resume):
    """
    A method to create a filename/file path using the company name, the
    job title, and distinguish if it is a resume or cover letter

    :param company:
    :param job_title:
    :param letter_or_resume:
    :return:
    """
    file_name = f"{job_title}_{company}_{letter_or_resume}"
    file_path = os.path.join(resume_and_cover_letter_directory, f"{file_name}.pdf")
    return file_path


def format_job_for_filename(parent):
    """
    A method to remove whitespace and replace with "_" for file naming

    :param parent:
    :return:
    """
    job_title = parent.job_title.replace(" ", "_")
    company = parent.company.replace(" ", "_")
    return company, job_title


def clean_html(content):
    """
    A method to remove HTML tags from resume/cover letter content
    :param content:
    :return:
    """
    # Convert markdown to HTML.  Pdfkit works with HTML format
    html_content = markdown.markdown(content)
    # Remove HTML tags.  Regex pattern obtained from Google AI
    cleaned_content = re.sub(r'<[^>]+>', '', html_content)
    return cleaned_content


def query_ai(api_key, query):
    """
    A method to connect with Google Gemini AI and initiate a query

    :param api_key:
    :param query:
    :return:
    """
    # This code is mirrored from the ai.google.dev website sample code and is modified only
    # slightly to meet project requirements.  Original code can be found at
    # https://ai.google.dev/gemini-api/docs?_gl=1*nqyqa0*_ga*NzExNDg0MDc0LjE3Mzg0Mjg3Njk.*_ga_P1DBVKWT6V
    # *MTczODQyODc2OS4xLjEuMTczODQyOTAwNy42MC4wLjc3ODAwMjE5Mg..#python
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)  # Execute query, store response

    return response
