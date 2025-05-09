"""
An example of the usage of this script:
1. Specify mentioned below parameters in .env file
GOOGLE_SCHOLAR_BY_YEARS = output/statistics/flight_soft_sims_data_2025-05-06_12-06-51.json
SEMANTIC_SCHOLAR_BY_YEARS = output/statistics/flight_soft_sims_data_2025-05-06_12-06-51.json
SAVE_GRAPHS_BASE_FOLDERNAME = output/visualizations/graphs
2. Run this script: `python scripts/04_data_visualization_years.py`

The script was already run with the mentioned above input parameters.
The script might be run again with other files, for example with updated statistics from the following years.

In addition, the called methods might be adjusted at the end of this file.
For example, if you don't need plots related to flight software at all, you caan exclude correspoding method calls.
"""

import matplotlib.pyplot as plt
import numpy as np
import os, json, sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import now_timestamp


class YearsVisualization:
    """
    A class used to create a folder and save the generated plots there.

    The generated plots include:
    1. Graphs for simulators' usage over the years
    1. Graphs for flight software' usage over the years
    1. Graphs for simulators' usage **with UAV** over the years
    1. Graphs for flight software' usage **with UAV** over the years

    Graphs may be generated for Google Scholar and Semantic Scholar.

    In addition, there is a method that generates graphs that compare Google Scholar and Semantic Scholar search results.

    You can flexibly adjust which methods to call.

    To use this class, you have to provide three variables in .env file:
    - GOOGLE_SCHOLAR_BY_YEARS - a path to a file with Google Scholar statistics over the years
    - SEMANTIC_SCHOLAR_BY_YEARS - a path to a file with Semantic Scholar statistics over the years
    - SAVE_GRAPHS_BASE_FOLDERNAME - a path to a folder where to save the generated folder with all the plots

    ...

    Attributes
    ----------
    google_scholar_data : object
        a formatted string to print out what the animal says
    semantic_scholar_data : str
        the name of the animal
    years : str
        the sound that the animal makes
    softwares : int
        the number of legs the animal has (default 4)
    sims : jdnclzn
        kjdfnvjv
    folder_to_save_plots : str
        kjvdfhvdjhfbvdjhfb

    Methods
    -------
    popularities_by_years_plot(sound=None)
        Gets data from parsed dict, generates plot and saves it to the file
    """

    # created folder is named 'visualization_{timestamp}' where timestamp is equal to the time of creation
    # inside the folder there is a file called ??? where the sources of statistics for Google Scholar and Semantic Scholar data are specified

    def __init__(self):
        load_dotenv(override=True)
        self.folder_to_save_plots = (
            os.getenv("SAVE_GRAPHS_BASE_FOLDERNAME")
            + "/"
            + "visualization_"
            + now_timestamp()
        )
        Path(self.folder_to_save_plots).mkdir(parents=True, exist_ok=True)

        google_scholar_stats = os.getenv("GOOGLE_SCHOLAR_BY_YEARS")
        with open(google_scholar_stats) as f:
            google_scholar_data = json.load(f)
            self.google_scholar_data = google_scholar_data["data"]

        semantic_scholar_stats = os.getenv("SEMANTIC_SCHOLAR_BY_YEARS")
        with open(semantic_scholar_stats) as f:
            semantic_scholar_data = json.load(f)
            self.semantic_scholar_data = semantic_scholar_data["data"]

        self.years = list(self.google_scholar_data.keys())
        first_year = self.years[0]
        self.softwares = self.google_scholar_data[first_year][
            "software_popularities"
        ].keys()
        self.sims = self.google_scholar_data[first_year]["sim_popularities"].keys()

        with open(self.folder_to_save_plots + "/source.txt", "w+") as f:
            f.write("GOOGLE_SCHOLAR_BY_YEARS = " + google_scholar_stats + "\n")
            f.write("SEMANTIC_SCHOLAR_BY_YEARS = " + semantic_scholar_stats + "\n")
            f.write(
                "SAVE_GRAPHS_BASE_FOLDERNAME = "
                + os.getenv("SAVE_GRAPHS_BASE_FOLDERNAME")
            )
            pass

    def __get_key_name(self, is_software: bool, with_uav: bool):
        # helper method to define required key name to get required statistics
        soft_key_name = ("uav_" if with_uav else "") + "software_popularities"
        sim_key_name = ("uav_" if with_uav else "") + "sim_popularities"

        return soft_key_name if is_software else sim_key_name

    def popularities_by_years_plot(
        self,
        name: str,
        is_software: bool,
        with_uav: bool,
        from_google: bool,
    ):
        # gets data from parsed dict, generates plot and saves it to the file
        # the plot shows a graph with changes in published academic papers present at either Google Scholar or Semantic Scholar over the years
        dict = self.google_scholar_data if from_google else self.semantic_scholar_data
        key_name = self.__get_key_name(is_software, with_uav)
        popularities = list(map(lambda obj: obj[key_name][name], dict.values()))

        title = f"{name}{" UAV" if with_uav else ""} Over Years"
        label = "with UAV" if with_uav else "total"
        label += f" from {"Google Scholar" if from_google else "Semantic Scholar"}"

        plt.figure(figsize=(8, 5))
        plt.xticks(np.arange(len(self.years)), self.years, rotation=45)
        plt.plot(self.years, popularities, label=label)
        plt.title(title)
        plt.legend()

        folder = f"{self.folder_to_save_plots}"
        folder += f"/{"software" if is_software else "simulators"}"
        folder += f"/{"with_uav" if with_uav else "total"}"
        folder += f"/{"google_scholar" if from_google else "semantic_scholar"}"
        Path(folder).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{folder}/{title}.png")

    def all_popularities_by_years(
        self, for_software: bool, from_google: bool, with_uav: bool
    ):
        # generates graphs for either all simulators or all flight software that is present in the provided files
        if for_software:
            for soft in self.softwares:
                self.popularities_by_years_plot(
                    soft,
                    is_software=True,
                    with_uav=with_uav,
                    from_google=from_google,
                )
        else:
            for sim in self.sims:
                self.popularities_by_years_plot(
                    sim, is_software=False, with_uav=with_uav, from_google=from_google
                )

    def compare_one_google_semantic(self, name, is_software: bool, with_uav: bool):
        # creates a plot with two graphs where
        # one shows the amount of papers related to the searched product over the years at Google Scholar
        # and another one shows the amount of papers at Semantic Scholar

        key_name = self.__get_key_name(is_software, with_uav)
        title = f"{name} {" UAV" if with_uav else ""} Over Years"

        google_popularities = list(
            map(
                lambda obj: obj[key_name][name],
                self.google_scholar_data.values(),
            )
        )
        semantic_popularities = list(
            map(
                lambda obj: obj[key_name][name],
                self.semantic_scholar_data.values(),
            )
        )

        plt.figure(figsize=(8, 5))
        plt.xticks(np.arange(len(self.years)), self.years, rotation=45)
        plt.plot(self.years, google_popularities, label="Google Scholar")
        plt.plot(self.years, semantic_popularities, label="Semantic Scholar")
        plt.title(title)
        plt.legend()

        folder = f"{self.folder_to_save_plots}/google_vs_semantic"
        folder += f"/{"software" if is_software else "sims"}"
        folder += f"/{"with_uav" if with_uav else "total"}"
        Path(folder).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{folder}/{title}.png")

    def compare_all_google_semantic(self, is_software: bool, with_uav: bool):
        # generates plots with academic search engines (Google Scholar and Semantic Scholar) comparison
        # the plots compare the amount of papers found for the same search queries
        # the queries are related to either simulators or flight software
        if is_software:
            for soft in self.softwares:
                self.compare_one_google_semantic(
                    soft, is_software=True, with_uav=with_uav
                )
        else:
            for sim in self.sims:
                self.compare_one_google_semantic(
                    sim, is_software=False, with_uav=with_uav
                )


# variations:
# either simulator or flight software
# either Google Scholar or Sematic Scholar
# search contains either only the name of the product or the name concatinated with "uav" word

if __name__ == "__main__":
    vis = YearsVisualization()
    vis.all_popularities_by_years(for_software=True, from_google=True, with_uav=False)
    vis.all_popularities_by_years(for_software=True, from_google=True, with_uav=True)
    vis.all_popularities_by_years(for_software=True, from_google=False, with_uav=False)
    vis.all_popularities_by_years(for_software=True, from_google=False, with_uav=True)
    vis.all_popularities_by_years(for_software=False, from_google=True, with_uav=False)
    vis.all_popularities_by_years(for_software=False, from_google=True, with_uav=True)
    vis.all_popularities_by_years(for_software=False, from_google=False, with_uav=False)
    vis.all_popularities_by_years(for_software=False, from_google=False, with_uav=True)

    vis.compare_all_google_semantic(is_software=True, with_uav=False)
    vis.compare_all_google_semantic(is_software=True, with_uav=True)
    vis.compare_all_google_semantic(is_software=False, with_uav=False)
    vis.compare_all_google_semantic(is_software=False, with_uav=True)

# Google Scholar NVIDIA Isaac Sim from 2010 till 2025
# remove extra backspace
