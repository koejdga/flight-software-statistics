# Simulators and Flight Software Distribution Statistics

This repository is devoted to the retrieving of mentions' statistics for two entities, namely, UAV simulators (e.g., Gazebo) and flight control software (e.g., ArduPilot).

Mention's amount is retrieved from two academic search engines: Google Scholar and Semantic Scholar.

The search queries conducted to those engine include either only the name of the product (e.g., Gazebo) or the name and the word "uav" appended at the end of the query.

Finally, the statitics comes in two variants with first being the total papers' amount and the second being the papers' amount over the years.

Also, to find out **usage of specific simulator with specific flight software**, queries with such structure were used: UAV simulation {flight software name} {simulator name} (e.g., "UAV simulation PX4 gazebo" without parentheses)

## The objective of this repository

There are two main reasons why this repository might be useful.

The first one is the already gathered statistics and visualizations of it
The second one are the scripts that enable the gathering of the statistics later again.

The gathered statistics might give someone insights about the popularity of the products overall or over the years.

The comparison between Google Scholar and Semantic Scholar can provide insights about where is it better to search for the relevant information depending on what simulator or flight software is a subject of your interest.

## Structure

### 1. `input` folder - contains 3 input files

1. `flight_software_list.json` - a list of flight control software for which the statistics is going to be retrieved
2. `simulators_list.json` - a list of UAV simulators for which the statistics is going to be retrieved
3. `supplementary_data.json` - a file where supplementary data could be attached. For now, the only data that is expected to be there is the release years of the simulators and flight control software specified in the previously mentioned two files.

### 2. `output` folder - contains JSON files with the retrieved statistics and PNG files with visualizations.

- `statistics` - contains JSON files
- `visualizations` - contains PNG files

### 3. `scripts` folder - contains scripts for data retrieval and data visualization.

1. `01_data_retrieval.py` - a script that sends requests to the chosen search engine, parses responses to them, and saves the result in the `output` folder.

It saves the information about

- the total amount of papers with the product mentions
- the total amount of papers with the product mentions with "UAV"
- the total amount of papers with mentions of the pairing of one UAV simulator and one flight control software

2. `02_data_retrieval_years.py` - a script that sends requests to the chosen search engine, parses responses to them, and saves the result in the `output` folder.

It saves the information about

- the amount of papers with the product mentions in each year that is included in the provided years' range

Script command-line parameters:

- from-year - the starting year from which to retrieve the statistics (including this year)
- to-year - the ending year till which to retrieve the statistics (including this year)

3. `03_data_visualization.py` - a script that creates visualization plots for the total amount of mentions data and saves them in the files in `output/visualizations/graphs` folder

4. `04_data_visualization_years.py` - a script that creates visualization plots for the amount of mentions over the years and save them in the files in `output/visualizations/graphs` folder

### 4. `src` folder - contains python files that are used in the scripts.

### 5. `templates` folder - contains a template that anyone can fill up and use visualization scripts to better understand the data.

## Used libraries

- matplotlib - to generate plots with graphs for visualizations
- seaborn - to generate heatmap plots
- requests - to make HTTP requests
- dotenv - to load variables from .env file
- argparse - parses command-line arguments
