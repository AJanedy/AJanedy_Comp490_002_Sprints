from src.ai_resume_builder.resume_generator import get_api_key
import google.generativeai as genai
import os
import re
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ...\AJanedy_Comp490_002_Sprints\src\job_search_gui
script_directory = os.path.dirname(os.path.abspath(__file__))
# \AJanedy_Comp490_002_Sprints\src\ai_resume_builder\resumes_and_cover_letters
resume_and_cover_letter_directory = os.path.join(script_directory, "resumes_and_cover_letters")

# Constants for layout
MARGIN_LEFT = 40
MARGIN_TOP = 750
LINE_HEIGHT = 12  # Spacing between lines
PAGE_HEIGHT = letter[1]
PARAGRAPH_SPACING = 10
BOTTOM_MARGIN = 50  # Margin before starting a new page
MAX_WIDTH = 520  # Max text width before wrapping


def generate_resume_and_cover_letter(parent):
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
    resume_prompt = ("Given the job description and the information I have "
                     "provided about myself, please write me a sample resume "
                     "in markdown format that is specifically designed around "
                     "my skills and the job description provided.")

    resume_query = (f"Job Description: {job_listing}\n\n"
                    f"Personal Information: {user_profile}\n\n"
                    f"{resume_prompt}")

    return resume_query


def get_cover_letter_query(user_profile, job_listing):
    cover_letter_prompt = ("Given the job description and the information I have "
                           "provided about myself, please write me a sample cover letter "
                           "in markdown format that is specifically designed around "
                           "my skills and the job description provided.")

    cover_letter_query = (f"Job Description: {job_listing}\n\n"
                          f"Personal Information: {user_profile}\n\n"
                          f"{cover_letter_prompt}")

    return cover_letter_query


def generate_pdf(content, parent, letter_or_resume):

    # Convert to HTML format then clean HTML markers
    cleaned_content = clean_html(content)

    company, job_title = format_job_for_filename(parent)

    file_path = get_filepath(company, job_title, letter_or_resume)

    # Create a blank canvas object for the PDF
    pdf_canvas = canvas.Canvas(file_path, pagesize=letter)

    # Set font
    pdf_canvas.setFont("Helvetica", 10)

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
    file_name = f"{job_title}_{company}_{letter_or_resume}"
    file_path = os.path.join(resume_and_cover_letter_directory, f"{file_name}.pdf")
    return file_path


def format_job_for_filename(parent):
    job_title = parent.job_title.replace(" ", "_")
    company = parent.company.replace(" ", "_")
    return company, job_title


def clean_html(content):
    # Convert markdown to HTML.  Pdfkit works with HTML format
    html_content = markdown.markdown(content)
    # Remove HTML tags.  Regex pattern obtained from Google AI
    cleaned_content = re.sub(r'<[^>]+>', '', html_content)
    return cleaned_content


def query_ai(api_key, query):
    # This code is mirrored from the ai.google.dev website sample code and is modified only
    # slightly to meet project requirements.  Original code can be found at
    # https://ai.google.dev/gemini-api/docs?_gl=1*nqyqa0*_ga*NzExNDg0MDc0LjE3Mzg0Mjg3Njk.*_ga_P1DBVKWT6V
    # *MTczODQyODc2OS4xLjEuMTczODQyOTAwNy42MC4wLjc3ODAwMjE5Mg..#python
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)  # Execute query, store response

    return response
