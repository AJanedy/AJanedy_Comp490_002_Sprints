import io

from src.ai_resume_builder.resume_generator import get_api_key
import google.generativeai as genai
import os
import markdown
import pdfkit

# ...\AJanedy_Comp490_002_Sprints\src\job_search_gui
script_directory = os.path.dirname(os.path.abspath(__file__))
# \AJanedy_Comp490_002_Sprints\src\ai_resume_builder\resumes_and_cover_letters
resume_and_cover_letter_directory = os.path.join(script_directory, "resumes_and_cover_letters")


def generate_resume_and_cover_letter(user_profile, job_listing, profile_name, parent):

    job_title = parent.job_title
    company = parent.company

    print(job_title)

    api_key = get_api_key()
    resume_query = get_resume_query(user_profile, job_listing)
    cover_letter_query = get_cover_letter_query(user_profile, job_listing)

    resume = query_ai(api_key, resume_query).text
    cover_letter = query_ai(api_key, cover_letter_query).text

    generate_pdf(resume, profile_name, "resume")
    generate_pdf(cover_letter, profile_name, "cover_letter")


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


def generate_pdf(content, profile_name, letter_or_resume):

    # Convert markdown to HTML.  Pdfkit works with HTML format
    html_content = markdown.markdown(content)

    # Make the directory if it does not exist
    if not os.path.exists(resume_and_cover_letter_directory):
        os.mkdir(resume_and_cover_letter_directory)



def query_ai(api_key, query):
    # This code is mirrored from the ai.google.dev website sample code and is modified only
    # slightly to meet project requirements.  Original code can be found at
    # https://ai.google.dev/gemini-api/docs?_gl=1*nqyqa0*_ga*NzExNDg0MDc0LjE3Mzg0Mjg3Njk.*_ga_P1DBVKWT6V
    # *MTczODQyODc2OS4xLjEuMTczODQyOTAwNy42MC4wLjc3ODAwMjE5Mg..#python
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)  # Execute query, store response

    return response
