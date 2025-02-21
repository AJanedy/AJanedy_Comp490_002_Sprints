=======================================================================================================================

To use this program, Python 3.6 or higher and google-generativeai need to be installed on your machine.

=======================================================================================================================

This program requires a Google generative-ai API key.  It must be saved into the api_key.txt file for the 
program to work.  This key is not provided on GitHub, as such the api_key.txt file will be empty.  A user 
must procure their own key or have it be provided via a private channel, and either copy it into api_key.txt, 
or alternatively, before running the program in command line, create an environment variable and set it equal 
to the API key.

Special note: A pre-commit hook has been added to api_key.txt; changes to this file cannot be committed.

=======================================================================================================================

To run the program, navigate to the root folder in command line, terminal, gitbash, or shell.  Run command
"python src\ai_resume_builder\resume_generator.py" or "python3 src/ai_resume_builder/resume_generator.py", 
depending on your chosen platform, the program should return a resume based on the provided job description, 
user qualifications, and prompt for the AI platform.  All of those files are provided in the respective .txt files. 
New resumes will be dynamically named and added to the resumes directory in ai_resume_builder.

=======================================================================================================================

My initial first run response is saved to AI_generated_resume.txt, all subsequent runs
will overwrite AI_generated_resume_2.txt to allow for a comparison between different runs of the same query.

=======================================================================================================================
=======================================================================================================================
THE RESULT OF THE QUERY WILL BE SAVED TO AI_generated_resume_2.txt
=======================================================================================================================
=======================================================================================================================

This program uses Google AI Studio, this is the chosen platform because of it's ease of use and compatibility with 
Python.  API keys are easy to secure and Google provides clear instruction on how to integrate their program with 
Python given their API; Google AI provides native Python support. The Google AI platform also provides a comprehensive 
selection of tools, high levels of scalability, and easy to use APIs.

=======================================================================================================================

The prompt given to the AI platform is saved into prompt.txt.  It is my experience that succinct queries often generate
a more relevant and desired result when using LLM generative AI.  The approach was to provide clear information without
being over verbose and giving the language model an over reaching breadth of sources with which to populate its 
response.  Most of the changes made in trying to get the best possible result were made to skills_and_qualifications.txt 
in an effort to get a more populated response as the initial feedback was asking for more information.

=======================================================================================================================