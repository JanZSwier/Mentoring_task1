import argparse
import json
from pip._vendor import requests


def main():

    my_parser = argparse.ArgumentParser(description='By giving name of country you will get '
                                                    'percentage of people recovered and still sick from all population'
                                                    '\n exmaple of usage: \n'
                                                    'python3 covid.py --country Poland')

    my_parser.add_argument('--country', action='store',  required=True, help="Name of country"
                                                                             " begins with BIG LETTER")

    args = my_parser.parse_args()

    countrys_data = requests.get("https://covid-api.mmediagroup.fr/v1/cases?country="+args.country).json()

    all_data = countrys_data.get("All")

    popul = all_data.get("population")
    reco = all_data.get("recovered")
    sik = all_data.get("confirmed")
    #print(popul, reco, sik)

    percent_of_recovered = round(100 * reco / popul, 1)
    percent_of_sick = round(100 * sik / popul, 1)

    relevant_info = {
        'recovered': percent_of_recovered,
        'sick': percent_of_sick
                    }

    json_object = json.dumps(relevant_info, indent=1)

    print(json_object)
    return json_object
