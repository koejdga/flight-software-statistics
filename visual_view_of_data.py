from data import *
from utils import sorted_tuples_list
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


sim_uav_popularity_list = sorted_tuples_list(sim_uav_popularity)
simulators_data = list(
    map(
        lambda tup: (
            tup[0],
            tup[1],
            next(filter(lambda x: x[0] == tup[0], sim_uav_popularity_list))[1],
        ),
        sorted_tuples_list(simulators_popularity),
    )
)
simulators_data = [(tup[0].value, tup[1], tup[2]) for tup in simulators_data]

flight_softwares_uav_popularity_list = sorted_tuples_list(
    flight_softwares_uav_popularity
)
software_data = list(
    map(
        lambda tup: (
            tup[0],
            tup[1],
            next(
                filter(lambda x: x[0] == tup[0], flight_softwares_uav_popularity_list)
            )[1],
        ),
        sorted_tuples_list(flight_softwares_popularity),
    )
)
software_data = [(tup[0].value, tup[1], tup[2]) for tup in software_data]


def get_software_in_simulators():
    simulator_totals = {
        sim: sum(
            softwares.get(sim, 0) for softwares in flight_softwares_and_sims.values()
        )
        for sim in Simulator
    }

    software_in_simulators = {"Simulator": [sim.value for sim in Simulator]}
    for software in flight_softwares_and_sims:
        software_in_simulators[f"{software.value} (%)"] = []

    for sim in Simulator:
        for software, software_data in flight_softwares_and_sims.items():
            percentage = (
                (software_data.get(sim, 0) / simulator_totals[sim]) * 100
                if simulator_totals[sim] > 0
                else 0
            )
            software_in_simulators[f"{software.value} (%)"].append(round(percentage))

    return software_in_simulators


def get_software_in_simulators_absolute():
    software_in_simulators = {"Simulator": [sim.value for sim in Simulator]}

    for software in flight_softwares_and_sims:
        software_in_simulators[f"{software.value} (Count)"] = []

    for sim in Simulator:
        for software, software_data in flight_softwares_and_sims.items():
            count = software_data.get(sim, 0)
            software_in_simulators[f"{software.value} (Count)"].append(count)

    return software_in_simulators


def get_simulators_in_software():
    software_totals = {
        software: sum(sim_data.values())
        for software, sim_data in flight_softwares_and_sims.items()
    }

    simulators_in_software = {
        "Software": [software.value for software in Flight_Software]
    }

    for sim in Simulator:
        simulators_in_software[f"{sim.value} (in %)"] = []

    for software, sim_data in flight_softwares_and_sims.items():
        for sim in Simulator:
            percentage = (
                (sim_data.get(sim, 0) / software_totals[software]) * 100
                if software_totals[software] > 0
                else 0
            )
            simulators_in_software[f"{sim.value} (in %)"].append(round(percentage))

    return simulators_in_software


def get_simulators_in_software_absolute():
    simulators_in_software = {
        "Software": [software.value for software in Flight_Software]
    }

    for sim in Simulator:
        simulators_in_software[f"{sim.value} (Count)"] = []

    for _, sim_data in flight_softwares_and_sims.items():
        for sim in Simulator:
            count = sim_data.get(sim, 0)
            simulators_in_software[f"{sim.value} (Count)"].append(count)

    return simulators_in_software


simulators_df = pd.DataFrame(
    simulators_data, columns=["Simulator", "Overall Mentions", "UAV Mentions"]
)
software_df = pd.DataFrame(
    software_data, columns=["Software", "Overall Mentions", "UAV Mentions"]
)


folder_to_save_plots = "flight software and sims visualizations"

width = 0.4


def bar_chart_sims_by_overall_and_uav_mentions():
    plt.figure(figsize=(10, 6))
    x = np.arange(len(simulators_df["Simulator"]))
    plt.bar(
        x - width / 2,
        simulators_df["Overall Mentions"],
        width,
        label="Overall Mentions",
    )
    plt.bar(x + width / 2, simulators_df["UAV Mentions"], width, label="UAV Mentions")

    plt.xticks(x, simulators_df["Simulator"], rotation=45)
    plt.ylabel("Mentions (log scale)")
    plt.yscale("log")
    plt.title("Simulators: Overall vs UAV Mentions")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{folder_to_save_plots}/Simulators: Overall vs UAV Mentions.png")


def bar_chart_flight_software_by_overall_and_uav_mentions():
    plt.figure(figsize=(8, 5))
    x = np.arange(len(software_df["Software"]))
    plt.bar(
        x - width / 2, software_df["Overall Mentions"], width, label="Overall Mentions"
    )
    plt.bar(x + width / 2, software_df["UAV Mentions"], width, label="UAV Mentions")

    plt.xticks(x, software_df["Software"], rotation=45)
    plt.ylabel("Mentions (log scale)")
    plt.yscale("log")
    plt.title("Flight Control Software: Overall vs UAV Mentions")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        f"{folder_to_save_plots}/Flight Control Software: Overall vs UAV Mentions.png"
    )


def stacked_bar_chart_sim_mentions_with_software_breakdown(
    df, title, index, legend_title
):
    df.set_index(index, inplace=True)
    df.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="viridis")

    plt.ylabel("Percentage Mentions")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend(title=legend_title)
    plt.tight_layout()
    plt.savefig(f"{folder_to_save_plots}/{title}.png")


def heatmap_software_mentions_across_sims(df, title, xlabel, ylabel, rotate_xs=False):
    plt.figure(figsize=(10, 6))
    sns.heatmap(
        df,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        linewidths=0.5,
        cbar_kws={"label": "Percentage Mentions"},
    )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.xticks(rotation=45 if rotate_xs else 0)
    plt.savefig(f"{folder_to_save_plots}/{title}.png")


# bar_chart_sims_by_overall_and_uav_mentions()
# bar_chart_flight_software_by_overall_and_uav_mentions()

# software_simulators_df = pd.DataFrame(get_software_in_simulators())
# stacked_bar_chart_sim_mentions_with_software_breakdown(
#     software_simulators_df,
#     "Simulator Mentions with Software Breakdown",
#     index="Simulator",
#     legend_title="Software",
# )
# heatmap_software_mentions_across_sims(
#     software_simulators_df,
#     "Heatmap: Software Mentions Across Simulators",
#     xlabel="Software",
#     ylabel="Simulator",
# )

# simulators_software_df = pd.DataFrame(get_simulators_in_software())
# stacked_bar_chart_sim_mentions_with_software_breakdown(
#     simulators_software_df,
#     "Software Mentions with Simulator Breakdown",
#     index="Software",
#     legend_title="Simulator",
# )
# heatmap_software_mentions_across_sims(
#     simulators_software_df,
#     "Heatmap: Simulator Mentions Across Software",
#     xlabel="Simulator",
#     ylabel="Software",
#     rotate_xs=True,
# )

# software_simulators_df_abs = pd.DataFrame(get_software_in_simulators_absolute())
# stacked_bar_chart_sim_mentions_with_software_breakdown(
#     software_simulators_df_abs,
#     "Simulator Mentions Absolute with Software Breakdown",
#     index="Simulator",
#     legend_title="Software",
# )

# simulators_software_df_abs = pd.DataFrame(get_simulators_in_software_absolute())
# stacked_bar_chart_sim_mentions_with_software_breakdown(
#     simulators_software_df_abs,
#     "Software Mentions Absolute with Simulator Breakdown",
#     index="Software",
#     legend_title="Simulator",
# )
