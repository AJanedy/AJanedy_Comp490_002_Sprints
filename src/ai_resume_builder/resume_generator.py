import google.generativeai as genai

FILES = {
    "api_key": "api_key.txt",
    "job_description": "job_description.txt",
    "skills": "skills.txt",
    "prompt": "prompt.txt",
    "resume": "AI_generated_resume_2.txt"
}


def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return " ".join(file.read().splitlines())
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None


def write_to_file(filename, resume):
    with open(filename, 'w') as file:
        file.write(resume)


def generate_resume():
    api_key = read_file(FILES["api_key"])
    job_description = read_file(FILES["job_description"])
    skills = read_file(FILES["skills"])
    prompt = read_file(FILES["prompt"])

    query = (f"Job Description: {job_description}\n\n"
             f"Skills and Qualifications: {skills}\n\n"
             f"{prompt}")

    # This code is mirrored from the ai.google.dev website sample code and is modified only slightly to
    # meet project requirements.  Original code can be found at
    # https://ai.google.dev/gemini-api/docs?_gl=1*nqyqa0*_ga*NzExNDg0MDc0LjE3Mzg0Mjg3Njk.*_ga_P1DBVKWT6V
    # *MTczODQyODc2OS4xLjEuMTczODQyOTAwNy42MC4wLjc3ODAwMjE5Mg..#python
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)

    write_to_file(FILES["resume"], response.text)


if __name__ == "__main__":
    generate_resume()
