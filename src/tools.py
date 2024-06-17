from pydantic import BaseModel, Field
from langchain.tools import tool


class LinkedinInput(BaseModel):
    url: str = Field(
        ..., description="LinkedIn URL of the person for whom you want to fetch data"
    )


@tool(args_schema=LinkedinInput)
def get_linkedin_profile_data(url: str) -> dict:
    """Fetch the LinkedIn profile for given person."""
    return f"{url} : He is a software engineer at Google. His DOB is June 19, 2000."


class BrokerCheckInput(BaseModel):
    crd: str = Field(
        ..., description="CRD Number of the person for whom you want to fetch data"
    )


@tool(args_schema=BrokerCheckInput)
def get_brokercheck_profile_data(crd: str) -> dict:
    """Fetch the BrokerCheck profile for given person."""
    BASE_URL = f"https://brokercheck.finra.org/individual/summary/{crd}"
    return {
        "Broker Name": "DOUGLAS GAINES",
        "Is a Broker": True,
        "Is an Investment Adviser": True,
        "Broker CRD": 1000059,
        "Firm Name": "STIFEL, NICOLAUS & COMPANY, INCORPORATED",
        "Firm CRD": 793,
        "Firm Street": "10400 NE 4TH STREET, SUITE 2000",
        "Firm State": "WA",
        "Firm Zip": "98004",
        "Number of Disclosures": 0,
        "Years of Experience": 42,
        "Number of Firms": "4",
    }


def get_tools(toolkit):
    tools = toolkit.get_tools() + [
        get_linkedin_profile_data,
        get_brokercheck_profile_data,
    ]
    return tools
