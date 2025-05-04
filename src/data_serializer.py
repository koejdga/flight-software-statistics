import enum, json, os


class Data:
    data_filename = os.getenv("STATS_TO_VISUALIZE")

    def __init__(self):
        with open(self.data_filename) as f:
            dict = json.load(f)
            dict = dict["data"]

        self.Flight_Software = enum.Enum(
            "DynamicEnum", {k: k for k in dict["software_popularities"]}
        )
        self.Simulator = enum.Enum(
            "DynamicEnum", {k: k for k in dict["sim_popularities"]}
        )

        self.software_popularities = {}
        if "software_popularities" in dict.keys():
            for software, value in dict["software_popularities"].items():
                self.software_popularities[self.Flight_Software[software]] = value
        else:
            print("There are no software_popularities in given dict")

        self.sim_popularities = {}
        if "sim_popularities" in dict.keys():
            for sim, value in dict["sim_popularities"].items():
                self.sim_popularities[self.Simulator[sim]] = value
        else:
            print("There are no sim_popularities in given dict")

        self.uav_software_popularities = {}
        if "uav_software_popularities" in dict.keys():
            for software, value in dict["uav_software_popularities"].items():
                self.uav_software_popularities[self.Flight_Software[software]] = value
        else:
            print("There are no uav_software_popularities in given dict")

        self.uav_sim_popularities = {}
        if "uav_sim_popularities" in dict.keys():
            for sim, value in dict["uav_sim_popularities"].items():
                self.uav_sim_popularities[self.Simulator[sim]] = value
        else:
            print("There are no uav_sim_popularities in given dict")

        self.soft_sim_distributions = {}
        if "soft_sim_distributions" in dict.keys():
            for software, dict_value in dict["soft_sim_distributions"].items():
                self.soft_sim_distributions[self.Flight_Software[software]] = {}
                for sim, value in dict_value.items():
                    self.soft_sim_distributions[self.Flight_Software[software]][
                        self.Simulator[sim]
                    ] = value
        else:
            print("There are no soft_sim_distributions in given dict")
