from enum import Enum


class Simulator(Enum):
    GAZEBO = "Gazebo"
    FLIGHTMARE = "Flightmare"
    AIRSIM = "AirSim"
    ISAAC_SIM = "Isaac Sim"
    MICROSOFT_AIRSIM = "Microsoft AirSim"
    NVIDIA_ISAAC_SIM = "NVIDIA Isaac Sim"


class Flight_Software(Enum):
    PX4 = "PX4"
    ARDUPILOT = "ArduPilot"
    BETAFLIGHT = "BetaFlight"
    INAV = "INAV"


simulators_popularity = {
    Simulator.GAZEBO: 71600,
    Simulator.FLIGHTMARE: 323,
    Simulator.AIRSIM: 5600,
    Simulator.ISAAC_SIM: 371000,
    Simulator.MICROSOFT_AIRSIM: 1950,
    Simulator.NVIDIA_ISAAC_SIM: 6870,
}

flight_softwares_popularity = {
    Flight_Software.PX4: 15900,
    Flight_Software.ARDUPILOT: 9930,
    Flight_Software.BETAFLIGHT: 581,
    Flight_Software.INAV: 9110,
}

flight_softwares_uav_popularity = {
    Flight_Software.PX4: 7100,
    Flight_Software.ARDUPILOT: 7950,
    Flight_Software.BETAFLIGHT: 422,
    Flight_Software.INAV: 405,
}

sim_uav_popularity = {
    Simulator.GAZEBO: 10300,
    Simulator.FLIGHTMARE: 238,
    Simulator.AIRSIM: 2650,
    Simulator.ISAAC_SIM: 2250,
    Simulator.MICROSOFT_AIRSIM: 1140,
    Simulator.NVIDIA_ISAAC_SIM: 502,
}

flight_softwares_and_sims = {
    Flight_Software.PX4: {
        Simulator.GAZEBO: 3530,
        Simulator.FLIGHTMARE: 90,
        Simulator.AIRSIM: 672,
        Simulator.ISAAC_SIM: 100,
        Simulator.MICROSOFT_AIRSIM: 362,
        Simulator.NVIDIA_ISAAC_SIM: 66,
    },
    Flight_Software.ARDUPILOT: {
        Simulator.GAZEBO: 2370,
        Simulator.FLIGHTMARE: 32,
        Simulator.AIRSIM: 340,
        Simulator.ISAAC_SIM: 106,
        Simulator.MICROSOFT_AIRSIM: 196,
        Simulator.NVIDIA_ISAAC_SIM: 47,
    },
    Flight_Software.BETAFLIGHT: {
        Simulator.GAZEBO: 82,
        Simulator.FLIGHTMARE: 18,
        Simulator.AIRSIM: 39,
        Simulator.ISAAC_SIM: 8,
        Simulator.MICROSOFT_AIRSIM: 23,
        Simulator.NVIDIA_ISAAC_SIM: 8,
    },
    Flight_Software.INAV: {
        Simulator.GAZEBO: 54,
        Simulator.FLIGHTMARE: 0,
        Simulator.AIRSIM: 17,
        Simulator.ISAAC_SIM: 1,
        Simulator.MICROSOFT_AIRSIM: 12,
        Simulator.NVIDIA_ISAAC_SIM: 0,
    },
}
