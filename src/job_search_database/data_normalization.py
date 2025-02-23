from pathlib import Path
from typing import TextIO
import json
import re


def process_json_array(source_file: Path, line: str, output_file: TextIO):
    """
    A method for extracting individual json objects from a line (string) containing a
    list of json objects.

    process_json_array() leverages the json.loads() method to create a list of json
    objects from a single line (a string obtained from a source json file), the method
    then iterates through this list, passing each json object into the
    normalize_json_object() method where keys are normalized between sources where
    applicable.  json.dumps() then formats the json object into a string to be written
    to the new, normalized file

    :param source_file: A Path object that represents a source json file
    :param line: A string containing the contents of one line from the source json file.
    :param output_file: A TextIO wrapper representing the output file for the
        normalized json data
    :return:
    """
    try:
        json_objects = json.loads(line)  # Parse the JSON array from the line into a list.

        for json_object in json_objects:
            json_object = normalize_json_object(json_object)
            # Write each JSON object to the new file, one per line
            output_file.write(json.dumps(json_object) + "\n")

    except json.JSONDecodeError as e:
        print(f"Error parsing line in {source_file}: {e}")


def process_json_object(source_file: Path, line: str, output_file: TextIO):
    """
    A method for extracting individual json objects from a line (string) that
    represents a single json object

    process_json_array() leverages the json.loads() method to create a json objects
    from a single line (a string obtained from a source json file), the method
    then passes this object into the normalize_json_object() method where keys are
    normalized between sources where applicable.  json.dumps() then formats the json
    object into a string to be written to the new, normalized file.

    :param source_file: A Path object that represents a source json file
    :param line: A string containing the contents of one line from the source json file.
    :param output_file: A TextIO wrapper representing the output file for the
        normalized json data
    :return:
    """
    try:
        json_objects = json.loads(line)
        json_object = normalize_json_object(json_objects)
        output_file.write(json.dumps(json_object) + "\n")

    except json.JSONDecodeError as e:
        print(f"Error parsing line in {source_file}: {e}")


def normalize_json_object(json_obj: dict):
    """
    A method for normalizing json objects with similar attributes
    of different names for future database manipulation

    :param json_obj: Dictionary/json object
    :return json_obj: Dictionary/json object
    """
    json_obj = normalize_attributes(json_obj)
    json_obj = normalize_location_data(json_obj)

    return json_obj


def normalize_attributes(json_obj):
    if "salaryRange" in json_obj:
        json_obj["compensation"] = json_obj.pop("salaryRange")
    if "jobProviders" in json_obj:
        json_obj["job_providers"] = json_obj.pop("jobProviders")
    if "employmentType" in json_obj:
        json_obj["employment_type"] = json_obj.pop("employmentType")
    if "datePosted" in json_obj:
        json_obj["date_posted"] = json_obj.pop("datePosted")
    if "interval" not in json_obj:
        json_obj["interval"] = "yearly"
    if "min_amount" in json_obj:
        json_obj["compensation"] = f"{json_obj['min_amount']} - {json_obj['max_amount']}"
        del json_obj["min_amount"]
        del json_obj["max_amount"]
    if "company_addresses" in json_obj:
        json_obj["location"] = json_obj.pop("company_addresses")
    if "job_type" in json_obj:
        json_obj["employment_type"] = json_obj.pop("job_type")
    if "image" in json_obj:
        json_obj["company_logo"] = json_obj.pop("image")
    if "job_url" not in json_obj:
        json_obj["job_url"] = ""

    return json_obj


def normalize_location_data(json_obj: dict):
    """
        A method for normalizing the location data for each
        job posting

        :param json_obj: Dictionary/json object
        :return json_obj: Dictionary/json object
        """
    state_abbreviations = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
        "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
        "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
    }

    # Remove numbers and dashes from the end of locations (zip codes)
    json_obj["location"] = re.sub(r'[\s\d,.-]+$', '', json_obj["location"]).strip()

    remove_usa(json_obj)

    normalize_state_abbreviations(json_obj, state_abbreviations)
    location = append_united_states(json_obj, state_abbreviations)
    change_language_and_formatting_usa(json_obj, location)
    json_obj["location"] = extract_city_state_country(json_obj["location"])
    normalize_city_state_country(json_obj)

    return json_obj


def normalize_city_state_country(json_obj):
    location = json_obj["location"]
    if location.strip() in ["Boston", "Cambridge", "Somerville"]:
        json_obj["location"] = f"{json_obj['location']}, MA, United States"
    if location.strip() in ["San Francisco", "San Jose", "Sacramento"]:
        json_obj["location"] = f"{json_obj['location']}, CA, United States"
    if location.strip() in ["Pittsburgh"]:
        json_obj["location"] = f"{json_obj['location']}, PA, United States"
    if location.strip() in ["Atlanta"]:
        json_obj["location"] = f"{json_obj['location']}, GA, United States"
    if location.strip() in ["Chicago"]:
        json_obj["location"] = f"{json_obj['location']}, IL, United States"
    if location.strip() in ["Austin"]:
        json_obj["location"] = f"{json_obj['location']}, TX, United States"
    if location.strip() in ["New Orleans"]:
        json_obj["location"] = f"{json_obj['location']}, LA, United States"
    if location.strip() in ["Las Vegas"]:
        json_obj["location"] = f"{json_obj['location']}, NV, United States"
    if location.strip() == "WA DC":
        json_obj["location"] = "Washington, DC, United States"
    if location.strip() == "Dublin, Dublin":
        json_obj["location"] = "Dublin, Ireland"
    if location.strip() in ["Tokyo"]:
        json_obj["location"] = f"{json_obj['location']}, Japan"
    if all(word in location for word in ["Tokyo", "Japan"]):
        json_obj["location"] = "Tokyo, Japan"
    if location.strip() in ["Paris"]:
        json_obj['location'] = f"{json_obj['location']}, France"
    if location.strip() in ["Bengaluru"]:
        json_obj['location'] = f"{json_obj['location']}, India"
    if location.strip() in ["Madrid", "Barcelona"]:
        json_obj["location"] = f"{json_obj['location']}, Spain"


def remove_usa(json_obj):
    if json_obj["location"].endswith(" USA"):
        json_obj["location"] = json_obj["location"].strip(" USA")


def change_language_and_formatting_usa(json_obj, location):
    if "États-Unis" in location:
        json_obj["location"] = json_obj["location"].replace("États-Unis", "United States")
    if "Stati Uniti" in location:
        json_obj["location"] = json_obj["location"].replace("Stati Uniti", "United States")
    if "Vereinigte Staaten" in location:
        json_obj["location"] = json_obj["location"].replace("Vereinigte Staaten", "United States")
    if "United States of America" in location:
        json_obj["location"] = json_obj["location"].replace("United States of America", "United States")


def append_united_states(json_obj, state_abbreviations):
    location = json_obj["location"]
    if any(location.strip().endswith(abbrev) for abbrev in state_abbreviations.values()):
        json_obj["location"] = f"{json_obj['location']}, United States"
    location = json_obj["location"]
    if any((location.strip() == abbrev) for abbrev in state_abbreviations.values()):
        json_obj["location"] = f"{json_obj['location']}, United States"
    return location


def normalize_state_abbreviations(json_obj, state_abbreviations):
    location = json_obj["location"]
    if "New York, New York" in location or "New York, NY" in location:
        json_obj["location"] = "New York, NY, United States"
    elif "Washington, DC" in location:
        json_obj["location"] = "Washington, DC, United States"
    else:
        for state, abbreviation in state_abbreviations.items():
            if state in location:
                json_obj["location"] = json_obj["location"].replace(state, abbreviation)
                # if abbreviation in json_obj["location"] and f"{abbreviation}, " not in json_obj["location"]:
                #     json_obj["location"] = json_obj["location"].replace(abbreviation, f"{abbreviation}, ")


def extract_city_state_country(address):
    """
    Pattern and match logic derived from Google Gemini AI query
    :param address:
    :return:
    """
    # Regular expression pattern to match city, state abbreviation, and country
    pattern = r"(\w+(?:[\s\w]+)?),\s([A-Z]{2}),\s([\w\s]+)$"

    match = re.search(pattern, address)

    if match:
        city = match.group(1)
        state_abbreviation = match.group(2)
        country = match.group(3)
        return f"{city}, {state_abbreviation}, {country}"
    else:
        return address
