"""
Author: Andrew Janedy
February 2025

A program that utilizes Google Generative AI for the purpose of automating
resume construction.  The AI is given a predefined prompt containing a job
posting, an applicant's skills, education, and experience, and is asked to
build a customized resume.

This program requires an API key which is not included.
"""
import os
import google.generativeai as genai

files = {
    "API_KEY": "api_key.txt",
    "JOB_DESCRIPTION": "job_description.txt",
    "SKILLS": "skills.txt",
    "PROMPT": "prompt.txt"
}
# ...\AJanedy_Comp490_002_Sprints\src\ai_resume_builder
script_directory = os.path.dirname(os.path.abspath(__file__))
# \AJanedy_Comp490_002_Sprints\src\ai_resume_builder\source_text_files
txt_file_directory = os.path.join(script_directory, "source_text_files")
# Set each filepath to the absoulte path
files = {filename: os.path.join(txt_file_directory, filepath)
         for filename, filepath in files.items()}

# ...\AJanedy_Comp490_002_Sprints\src\ai_resume_builder\resumes
RESUME_DIRECTORY = os.path.join(script_directory, "resumes")


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
    for GitHub actions) or from a provided file.  If the file does not exist
    or is empty, the user is asked for the API key, and it is added into the file
    for future runs.

    :return: api_key
    """

    api_key_file = files["API_KEY"]
    api_key = os.environ.get("API_KEY")  # Get API key from environment variable

    if not api_key:  # If API_KEY is not an environment variable
        # If api_key.txt does not exist or is empty
        if not os.path.exists(api_key_file) or os.path.getsize(api_key_file) == 0:
            with open(api_key_file, 'w', encoding="utf-8") as file:
                api_key = input("Enter your api key: ")
                file.write(api_key)
        else:
            api_key = read_file(api_key_file)

    return api_key


def get_next_resume_filename():
    """
    A method for dynamically naming the new file that will contain the next AI generated
    resume response.  This method opens the directory of .txt files, creates a list of
    the counts (files are named incrementally, [ai_generated_resume_1,
    ai_generated_resume_2, ...3, ...4]), then determines what the next file should be
    called by finding the max value of the list.
    :return:
    """
    # Create a list of files in the resume directory
    existing_files = [file for file in os.listdir(RESUME_DIRECTORY)
                      # Directory should only have files starting with "ai_generated_resume"
                      if file.startswith("ai_generated_resume_") and file.endswith(".txt")]

    existing_numbers = []  # Empty list to hold extracted numbers of filenames

    for file in existing_files:
        try:
            # Extracts the number just at the end of the string, before ".txt"
            # If filename is ai_generated_resume_15.txt, this extracts the "15"
            num = int(file.split("_")[-1].split(".")[0])
            existing_numbers.append(num)
        except ValueError:
            continue

    # Finds the highest number used and increments it;
    # defaults to 0 if existing_numbers is empty
    next_number = max(existing_numbers, default=0) + 1
    return os.path.join(RESUME_DIRECTORY, f"ai_generated_resume_{next_number}.txt")


def generate_resume():
    """
    Program entry
    """

    api_key = get_api_key()

    # These str variables hold parts of the prompt given to
    # Google generative-ai
    job_description = read_file(files["JOB_DESCRIPTION"])
    skills = read_file(files["SKILLS"])
    prompt = read_file(files["PROMPT"])

    # Build the string that will hold the query
    query = (f"Job Description: {job_description}\n\n"
             f"Skills and Qualifications: {skills}\n\n"
             f"{prompt}")

    # This code is mirrored from the ai.google.dev website sample code and is modified only
    # slightly to meet project requirements.  Original code can be found at
    # https://ai.google.dev/gemini-api/docs?_gl=1*nqyqa0*_ga*NzExNDg0MDc0LjE3Mzg0Mjg3Njk.*_ga_P1DBVKWT6V
    # *MTczODQyODc2OS4xLjEuMTczODQyOTAwNy42MC4wLjc3ODAwMjE5Mg..#python
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)  # Execute query, store response

    new_resume_filename = get_next_resume_filename()  # Get next filename for new resume
    write_to_file(new_resume_filename, response.text)  # Store response to new file


if __name__ == "__main__":
    generate_resume()
