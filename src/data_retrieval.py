import sys, os, json, time, requests
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join("..")))
from src.utils import now_timestamp, valid_year


# Load required variables from .env
load_dotenv(override=True)
software_names_filepath = os.getenv("SOFT_LIST_PATH")
sim_names_filepath = os.getenv("SIM_LIST_PATH")
output_folderpath = os.getenv("OUTPUT_JSON_PATH")
from_semantic_scholar = os.getenv("FROM_SEMANTIC_SCHOLAR") == "true"


def get_flight_software_names():
    with open(software_names_filepath) as f:
        names = json.load(f)
        print("Loaded flight software names successfully")
        return names


def get_simulators_names():
    with open(sim_names_filepath) as f:
        names = json.load(f)
        print("Loaded simulators names successfully")
        return names


# returns filepath of output file
def generate_output_file() -> str:
    filepath = f"{output_folderpath}/flight_soft_sims_data_{now_timestamp()}.json"
    with open(filepath, "w+") as _:
        pass
    print(f"Output will be saved to {filepath}")
    return filepath


def get_results_amount_from_google_scholar(query: str, year: int = None) -> int:
    if year and not valid_year(year):
        return

    url = f"https://serpapi.com/search.json?q={"+".join(query.split(" "))}&engine=google_scholar&as_vis=1&num=1&api_key={os.getenv("SERPAPI_API_KEY")}"
    url = url + f"&as_ylo={year}&as_yhi={year}" if year else url

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["search_information"]["total_results"]
    else:
        print(f"Could not find url: {url}, response: {response}, {response.text}")
        print(f"Given request: '{query}'")
        return None


def get_results_amount_from_semantic_scholar(query: str, year: int = None) -> int:
    if year and not valid_year(year):
        return

    time.sleep(4)
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={"+".join(query.split(" "))}&limit=1"
    url = url + f"&year={year}" if year else url
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        total_results = data.get("total", 0)
        print(f"Total results for '{query} at Semantic Scholar': {total_results}")
        return total_results
    else:
        print(
            f"Request to Semantic Scholar with query '{query}' failed with status code {response.status_code}: {response.text}"
        )
        return None


def get_results_amount(query: str, year: int = None):
    if from_semantic_scholar:
        return get_results_amount_from_semantic_scholar(query, year)
    else:
        return get_results_amount_from_google_scholar(query, (year, year))


def add_popularity(name: str, is_software: bool, data: dict, year: int = None):
    entity = "software" if is_software else "sim"

    overall_result = get_results_amount(name, year)
    if overall_result:
        data[f"{entity}_popularities"][name] = overall_result
        print("Added overall popularity of " + name)

    uav_result = get_results_amount(name + " uav", year)
    if uav_result:
        data[f"uav_{entity}_popularities"][name] = uav_result
        print("Added UAV popularity of " + name)

    else:
        print("An error occured while adding popularity of " + name)
        if not overall_result:
            print(f"Overall result of {name} not found")
        if not uav_result:
            print(f"UAV result of {name} not found")


def add_software_and_sim_usage(sim: str, software: str, data: dict):
    res = get_results_amount(f"UAV simulation {software} {sim}")
    if res:
        data["soft_sim_distributions"][software][sim] = res
        print(f"Added distibution of {software} with {sim}")
    else:
        print(f"Could not add distibution of {software} with {sim}")
