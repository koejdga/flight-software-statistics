import sys, os, json
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_retrieval import (
    get_flight_software_names,
    get_simulators_names,
    generate_output_file,
    add_popularity,
    add_software_and_sim_usage,
)


# Load required variables from .env
load_dotenv(override=True)
from_semantic_scholar = os.getenv("FROM_SEMANTIC_SCHOLAR") == "true"


def retrieve_data():
    software = get_flight_software_names()
    sims = get_simulators_names()
    output_filepath = generate_output_file()
    data = {
        "software_popularities": {},
        "sim_popularities": {},
        "uav_software_popularities": {},
        "uav_sim_popularities": {},
        "soft_sim_distributions": {},
    }

    for soft in software:
        add_popularity(soft, is_software=True, data=data)
        data["soft_sim_distributions"][soft] = {}

        for sim in sims:
            add_popularity(sim, is_software=False, data=data)
            add_software_and_sim_usage(sim, soft, data)

    with open(output_filepath, "w") as f:
        total = {
            "from": "Semantic Scholar" if from_semantic_scholar else "Google Scholar",
            "data": data,
        }
        json.dump(total, f, indent=2)

    print(f"Saved received data to '{output_filepath}'")
    print("End")


retrieve_data()
