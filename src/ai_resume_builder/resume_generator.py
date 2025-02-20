"""
Author: Andrew Janedy
February 2025

A program to access Google Generative AI for the purpose of automating
resume construction.  The AI is given a predetermined prompt that
includes a job posting, and is asked to build a resume for that job
given the applicant's skills, education, and work experience.
"""

import google.generativeai as genai
import os

FILES = {
    "api_key": "api_key.txt",
    "job_description": "job_description.txt",
    "skills": "skills.txt",
    "prompt": "prompt.txt",
    "resume": "AI_generated_resume_2.txt"
}


def read_file(filename):
    """
    A method to get file contents as a string

    :param filename:
    :return: Returns file contents as a string
    """
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return " ".join(file.read().splitlines())
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None


def write_to_file(filename, resume):
    """
    A method to write content to a file

    :param filename:
    :param resume:
    :return:
    """
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(resume)


def get_api_key():
    """
    A method to extract an API key either from the environment variable (used
    for GitHub actions) or from a provided file
    :return:
    """
    api_key = os.environ.get("API_KEY")  # Get API key from environment variable
    if not api_key:
        api_key = read_file(FILES["api_key"])
    return api_key


def generate_resume():
    """
    Program entry
    """

    api_key = get_api_key()
    job_description = read_file(FILES["job_description"])
    skills = read_file(FILES["skills"])
    prompt = read_file(FILES["prompt"])

    query = (f"Job Description: {job_description}\n\n"
             f"Skills and Qualifications: {skills}\n\n"
             f"{prompt}")

    # This code is mirrored from the ai.google.dev website sample code and is modified only
    # slightly to meet project requirements.  Original code can be found at
    # https://ai.google.dev/gemini-api/docs?_gl=1*nqyqa0*_ga*NzExNDg0MDc0LjE3Mzg0Mjg3Njk.*_ga_P1DBVKWT6V
    # *MTczODQyODc2OS4xLjEuMTczODQyOTAwNy42MC4wLjc3ODAwMjE5Mg..#python
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)

    write_to_file(FILES["resume"], response.text)


if __name__ == "__main__":
    generate_resume()
