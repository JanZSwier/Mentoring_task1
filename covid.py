import argparse
import json
import requests
import black as b


def parser():
    my_parser = argparse.ArgumentParser(description='By giving name of country you will get '
                                                    'percentage of people recovered and still sick from all population')
    my_parser.add_argument('--country', action='store', required=True, help="Name of country"
                                                                            " begins with BIG LETTER")
    return my_parser.parse_args()


def computing_answer(population, confirmed_cases, recovered_people, dead_people):
    percent_of_recovered = round(100 * recovered_people / population, 1)
    percent_of_sick = round(100 * (confirmed_cases - recovered_people - dead_people) / population, 1)
    print(json.dumps(
        {
            'recovered': percent_of_recovered,
            'sick': percent_of_sick
        }
        , indent=1))


def check_http_response():
    response = requests.get(url="https://covid-api.mmediagroup.fr/v1/cases")
    return response


def main():
    args = parser()

    if check_http_response().ok:

        countries_data = requests.get(url="https://covid-api.mmediagroup.fr/v1/cases?country="
                                          + args.country.capitalize()).json()

        all_data = countries_data.get("All")

        try:

            computing_answer(all_data.get("population"), all_data.get("confirmed"),
                             all_data.get("recovered"), all_data.get("deaths"))

        except AttributeError:
            print("There is no data for country:\n" + args.country)
    else:
        print("Oh no, unfortunately, some external error occurred. Please try again later")


if __name__ == "__main__":
    main()
