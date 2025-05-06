import sys, os, json, argparse
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import valid_years_range
from src.data_retrieval import (
    get_flight_software_names,
    get_simulators_names,
    generate_output_file,
    add_popularity,
)

# Load required variables from .env
load_dotenv(override=True)
from_semantic_scholar = os.getenv("FROM_SEMANTIC_SCHOLAR") == "true"


def retrieve_years_data(years_range: tuple[int, int] = None):
    software = get_flight_software_names()
    sims = get_simulators_names()
    output_filepath = generate_output_file()

    if years_range and not valid_years_range(years_range):
        return

    result_data = {}

    for year in range(years_range[0], years_range[1]):
        data = {
            "software_popularities": {},
            "sim_popularities": {},
            "uav_software_popularities": {},
            "uav_sim_popularities": {},
            "soft_sim_distributions": {},
        }

        for soft in software:
            add_popularity(soft, is_software=True, data=data, year=year)

        for sim in sims:
            add_popularity(sim, is_software=False, data=data, year=year)

        result_data[f"{year}"] = data

    with open(output_filepath, "w") as f:
        total = {
            "from": "Semantic Scholar" if from_semantic_scholar else "Google Scholar",
            "data": result_data,
        }
        json.dump(total, f, indent=2)

    print(f"Saved received data to '{output_filepath}'")
    print("End")


parser = argparse.ArgumentParser(description="Years range")
parser.add_argument(
    "--from_year", type=int, help="From which year to search (inclusively)"
)
parser.add_argument(
    "--to_year", type=int, help="Till which year to search (inclusively)"
)
args = parser.parse_args()

retrieve_years_data(years_range=(args.from_year, args.to_year))
