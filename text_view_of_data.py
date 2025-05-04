from data import *
from utils import sorted_tuples_list


def get_sim_usage_for_uavs(simulator: Simulator):
    return round(sim_uav_popularity[simulator] / simulators_popularity[simulator] * 100)


def get_software_usage_for_uavs(flight_software: Flight_Software):
    return round(
        flight_softwares_uav_popularity[flight_software]
        / flight_softwares_popularity[flight_software]
        * 100
    )


def get_usages_for_uavs_for_all_simulators():
    usages = map(
        lambda simulator: (simulator, get_sim_usage_for_uavs(simulator)),
        Simulator,
    )
    return sorted(usages, key=lambda tup: tup[1], reverse=True)


def usage_of_flight_software(flight_software, simulator):
    return round(
        (
            flight_softwares_and_sims[flight_software][simulator]
            / sim_uav_popularity[simulator]
        )
        * 100,
    )


def get_popularities_of_softwares(simulator):
    popularities = map(
        lambda software: (software, usage_of_flight_software(software, simulator)),
        Flight_Software,
    )
    popularities = sorted(popularities, key=lambda tup: tup[1], reverse=True)
    return popularities


def pretty_print_popularities_of_software(popularities):
    for software, percent in popularities:
        print(f"{software.value}: {percent}%")


def pretty_print_popularities_of_simulators(popularities):
    for simulator, percent in popularities:
        print(f"{simulator.value}: {percent}%")


def get_popularities_for_all_simulators():
    return list(
        map(
            lambda simulator: (simulator, get_popularities_of_softwares(simulator)),
            Simulator,
        )
    )


def usage_of_simulator(simulator, flight_software):
    return round(
        (
            flight_softwares_and_sims[flight_software][simulator]
            / flight_softwares_uav_popularity[flight_software]
        )
        * 100,
    )


def get_popularities_of_simulators(software):
    popularities = map(
        lambda simulator: (simulator, usage_of_simulator(simulator, software)),
        Simulator,
    )
    popularities = sorted(popularities, key=lambda tup: tup[1], reverse=True)
    return popularities


def get_popularities_for_all_softwares():
    return list(
        map(
            lambda software: (
                software,
                get_popularities_of_simulators(software),
            ),
            Flight_Software,
        )
    )


def pretty_print_popularities_for_all_simulators(software_popularities_for_simulators):
    simulator_popularities = sorted_tuples_list(simulators_popularity)
    for simulator, popularity in simulator_popularities:
        print(
            f"{simulator.value} ({popularity} mentions overall, with {get_sim_usage_for_uavs(simulator)}% mentions with UAVs)"
        )
        softwares = next(
            filter(
                lambda tup: tup[0] == simulator, software_popularities_for_simulators
            ),
        )[1]
        pretty_print_popularities_of_software(softwares)
        print()


def pretty_print_popularities_for_all_softwares(simulator_popularities_for_softwares):
    popularities = sorted_tuples_list(flight_softwares_popularity)
    for software, popularity in popularities:
        print(
            f"Flight control software {software.value}: {popularity} mentions overall, with {get_software_usage_for_uavs(software)}% mentions with UAVs"
        )
        simulators = next(
            filter(
                lambda tup: tup[0] == software, simulator_popularities_for_softwares
            ),
        )[1]
        pretty_print_popularities_of_simulators(simulators)
        print()


def pretty_print_uav_popularities_for_all_softwares():
    popularities = sorted_tuples_list(flight_softwares_uav_popularity)
    for software, popularity in popularities:
        print(
            f"Flight control software {software.value}: {popularity} mentions with UAVs"
        )
    print()


def pretty_print_uav_popularities_for_all_simulators():
    popularities = sorted_tuples_list(sim_uav_popularity)
    for simulator, popularity in popularities:
        print(f"Simulator {simulator.value}: {popularity} mentions with UAVs")
    print()


if __name__ == "__main__":
    sim_popularities = get_popularities_for_all_simulators()
    software_popularities = get_popularities_for_all_softwares()
    pretty_print_popularities_for_all_simulators(sim_popularities)
    pretty_print_popularities_for_all_softwares(software_popularities)
    pretty_print_uav_popularities_for_all_simulators()
    pretty_print_uav_popularities_for_all_softwares()
