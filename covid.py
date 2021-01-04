import argparse
import json
import requests # when i use that im getting ModuleNotFoundError: No module named 'requests'

def main():

    my_parser = argparse.ArgumentParser(description='By giving name of country you will get '
                                                    'percentage of people recovered and still sick from all population')

    my_parser.add_argument('--country', action='store',  required=True, help="Name of country"
                                                                             " begins with BIG LETTER")

    args = my_parser.parse_args()

    response=requests.get(url="https://covid-api.mmediagroup.fr/v1/cases?country=" + args.country)

    if response.ok:

        countries_data = requests.get(url="https://covid-api.mmediagroup.fr/v1/cases?country="+args.country).json()

        all_data = countries_data.get("All")

        try:
            population = all_data.get("population")
            dead_people=all_data.get("deaths")
            recovered_people = all_data.get("recovered")
            confirmed_cases = all_data.get("confirmed")

            percent_of_recovered = round(100 * recovered_people / population, 1)
            percent_of_sick = round(100 * (confirmed_cases-recovered_people-dead_people) / population, 1)

            relevant_info = {
                'recovered': percent_of_recovered,
                'sick': percent_of_sick
                            }

            json_object = json.dumps(relevant_info, indent=1)

            print(json_object)
        except AttributeError:
            print("Probably there is no such country as:\n"+args.country+"\n;)")
    else:
        print("Oh no, unfortunately, some external error occurred. Please try again later")




if __name__ == "__main__":
    main()
