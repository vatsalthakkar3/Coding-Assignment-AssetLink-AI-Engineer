from json import load
from pydantic import BaseModel, Field
from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
import traceback
from security import safe_requests

load_dotenv()


class LinkedinInput(BaseModel):
    query_url: str = Field(
        ..., description="Linkedin URL of the person for whom you want to fetch data"
    )


@tool(args_schema=LinkedinInput)
def get_linkedin_profile_data(query_url: str) -> dict:
    """Fetch the linkedin profile data of a person using the linkedin profile URL mentioned in the Linkedin Column of in the database.
    Output will contain the persons information like his current job, company, location, headline, summary, positions, educations, skills, projects etc.
    """
    url = "https://linkedin-data-api.p.rapidapi.com/get-profile-data-by-url"

    querystring = {"url": query_url}  # Replace with the actual profile URL

    headers = {
        "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
        "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com",
    }

    try:
        response = safe_requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        profile_data = response.json()

        extracted_data = {
            "username": profile_data.get("username"),
            "full_name": f"{profile_data.get('firstName', '')} {profile_data.get('lastName', '')}",
            "is_open_to_work": profile_data.get("isOpenToWork"),
            "is_hiring": profile_data.get("isHiring"),
            "headline": profile_data.get("headline"),
            "summary": profile_data.get("summary"),
            "location": profile_data.get("geo", {}).get("full"),
            "skills": profile_data.get("skills", []),
            "education": (
                [
                    {
                        "institution": edu.get("institutionName"),
                        "degree": edu.get("degreeName"),
                        "field_of_study": edu.get("fieldOfStudy"),
                        "start_date": edu.get("timePeriod", {})
                        .get("startDate", {})
                        .get("year"),
                        "end_date": edu.get("timePeriod", {})
                        .get("endDate", {})
                        .get("year"),
                    }
                    for edu in profile_data.get("educations", [])
                    if edu is not None
                ]
                if profile_data.get("educations")
                else []
            ),
            "positions": (
                [
                    {
                        "title": pos.get("title"),
                        "company": pos.get("companyName"),
                        "location": pos.get("geoLocationName"),
                        "start_date": pos.get("timePeriod", {})
                        .get("startDate", {})
                        .get("year"),
                        "end_date": pos.get("timePeriod", {})
                        .get("endDate", {})
                        .get("year"),
                        "description": pos.get("description"),
                    }
                    for pos in profile_data.get("positions", [])
                    if pos is not None
                ]
                if profile_data.get("positions")
                else []
            ),
            "projects": (
                [
                    {
                        "title": proj.get("title"),
                        "description": proj.get("description"),
                        "start_date": proj.get("timePeriod", {})
                        .get("startDate", {})
                        .get("year"),
                        "end_date": proj.get("timePeriod", {})
                        .get("endDate", {})
                        .get("year"),
                    }
                    for proj in profile_data.get("projects", {}).get("items", [])
                    if proj is not None
                ]
                if profile_data.get("projects")
                and profile_data.get("projects").get("items")
                else []
            ),
        }

        return extracted_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        traceback.print_exc()


if __name__ == "__main__":
    output_data = get_linkedin_profile_data(
        "https://www.linkedin.com/in/vatsal-thakkar-880320161/"
    )
    print(output_data)
