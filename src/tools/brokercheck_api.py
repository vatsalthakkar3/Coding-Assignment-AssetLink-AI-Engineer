from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from pydantic import BaseModel, Field
from langchain.tools import tool


class BrockerCheckInput(BaseModel):
    crd: str = Field(
        ..., description="CRD Number of the person for whom you want to fetch data"
    )


@tool(args_schema=BrockerCheckInput)
def get_brokercheck_profile_data(crd: str) -> dict:
    """Fetch the BrokerCheck profile for given person."""
    link = f"https://brokercheck.finra.org/individual/summary/{crd}"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    response = []

    timeout = False
    driver.get(link)

    try:
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/bc-root/div/bc-individual-container-page/bc-individual-detail-page/div[2]/investor-tools-individual-summary-template/div/div[1]/div[1]/div/investor-tools-big-name/div[1]/span[1]",
                )
            )
        )
    except TimeoutException:
        timeout = True
    finally:
        if not timeout:
            response = driver.page_source
        else:
            response = (int(link.rsplit("/", 1)[1]), "IA")
            timeout = False

    driver.quit()

    scraped_data_partial = {}
    if type(response) == tuple:
        scraped_data_partial["Broker CRD"] = response[0]
        scraped_data_partial["Is a Broker"] = "null"
        scraped_data_partial["Is an Investment Adviser"] = True
    else:
        soup = BeautifulSoup(response, features="html.parser")
        scraped_data_partial["name"] = soup.find(
            "span", {"class": "text-lg sm:text-sm font-semibold"}
        )
        scraped_data_partial["status"] = soup.find_all(
            "span", {"class": "text-gray-80 text-xs font-medium"}
        )
        scraped_data_partial["crd"] = soup.find(
            "div",
            {
                "class": "text-gray-85 text-left font-semibold mt-2 text-sm ng-star-inserted"
            },
        )
        scraped_data_partial["firm"] = soup.find(
            "div", {"class": "flex flex-col text-sm"}
        )
        scraped_data_partial["background"] = soup.find_all(
            "div", {"class": "flex-1 flex flex-col justify-center"}
        )

    scrape = scraped_data_partial

    if len(scrape) > 3:
        clean_data = {}
        clean_data["Broker Name"] = scrape["name"].string.strip()

        raw_status = scrape["status"]

        if len(raw_status) == 1:
            if scrape["status"][0].find("span").string == "Broker":
                clean_data["Is a Broker"] = True
            else:
                clean_data["Is a Broker"] = False

            clean_data["Is an Investment Adviser"] = False
        else:
            if raw_status[1].find("span").string == "Broker":
                clean_data["Is a Broker"] = True
            else:
                clean_data["Is a Broker"] = False

            if (
                raw_status[0]
                .find("span", {"title": "Investment Adviser"})
                .string.strip()
                == "Investment Adviser"
            ):
                clean_data["Is an Investment Adviser"] = True
            else:
                clean_data["Is an Investment Adviser"] = False

        clean_data["Broker CRD"] = int(scrape["crd"].find("span").next_sibling.string)

        if scrape["firm"]:
            clean_data["Firm Name"] = scrape["firm"].find("span").string
            clean_data["Firm CRD"] = int(
                scrape["firm"]
                .find("span")
                .next_sibling.find("span")
                .next_sibling.string
            )

            rawAddress = scrape["firm"].find("investor-tools-address")

            rawStreetAddress = rawAddress.next_element

            for x in range(3):
                rawStreetAddress = rawStreetAddress.next_element

            clean_data["Firm Street"] = rawStreetAddress.strip()

            rawCityStateZip = rawAddress.find("br")

            # for x in range(4):
            #     rawCityStateZip = rawCityStateZip.next_element

            #     rawCityStateZip = rawCityStateZip.strip()

            #     rawStateZip = rawCityStateZip.split(" ", 1)[1].split(" ", 1)

            # clean_data["Firm State"] = rawStateZip[0]

            # clean_data["Firm Zip"] = rawStateZip[1]
        else:
            clean_data["Firm Name"] = "none"
            clean_data["Firm CRD"] = "none"
            clean_data["Firm Street"] = "none"
            clean_data["Firm State"] = "none"
            clean_data["Firm Zip"] = "none"

        clean_data["Number of Disclosures"] = int(
            scrape["background"][0]
            .find(
                "span",
                {"class": "sm:text-lg sm:font-semibold text-3xl ng-star-inserted"},
            )
            .string.strip()
        )

        rawYearsFirms = scrape["background"][1].find_all(
            "span", {"class": "sm:text-lg sm:font-semibold text-3xl ng-star-inserted"}
        )

        if len(rawYearsFirms) == 2:
            clean_data["Years of Experience"] = int(rawYearsFirms[0].string.strip())
            clean_data["Number of Firms"] = rawYearsFirms[1].string.strip()
        else:
            clean_data["Years of Experience"] = int(rawYearsFirms[0].string.strip())
            clean_data["Number of Firms"] = (
                scrape["background"][1]
                .find(
                    "span",
                    {"class": "sm:text-lg sm:font-semibold text-xl ng-star-inserted"},
                )
                .string.strip()
            )

        scraped_data_clean = clean_data
    else:
        scraped_data_clean = scrape

    return scraped_data_clean
