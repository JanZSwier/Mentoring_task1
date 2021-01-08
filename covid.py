import argparse
import json
import requests


def parser():
    my_parser = argparse.ArgumentParser(
        description="By giving name of country you will get "
        "percentage of people recovered and still sick from all population"
    )
    my_parser.add_argument(
        "--country",
        action="store",
        required=True,
        help="Name of country",
    )
    return my_parser.parse_args()


def compute_answer(population, confirmed_cases, recovered_people, dead_people):
    percent_of_recovered = round(100 * recovered_people / population, 1)
    percent_of_sick = round(
        100 * (confirmed_cases - recovered_people - dead_people) / population, 1
    )

    return json.dumps(
        {"recovered": percent_of_recovered, "sick": percent_of_sick}, indent=1
    )


def call_covid_api(country_name):
    response = requests.get(
        url="https://covid-api.mmediagroup.fr/v1/cases?country=" + country_name
    )
    return response


def main():
    args = parser()
    covid_api_response = call_covid_api(args.country.capitalize())
    if covid_api_response.ok:

        all_data = covid_api_response.json()

        country_data = all_data.get("All")

        try:

            print(
                compute_answer(
                    country_data.get("population"),
                    country_data.get("confirmed"),
                    country_data.get("recovered"),
                    country_data.get("deaths"),
                )
            )

        except AttributeError:
            print(f"There is no data for country:\n{args.country}")
    else:
        print(
            "Oh no, unfortunately, some external error occurred. Please try again later"
        )


if __name__ == "__main__":
    main()
