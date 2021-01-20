import argparse
import ast
import json
import requests
import os

cache_file = "data.txt"


def get_parsed_arguments():
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


def is_cache_empty():
    return os.stat(cache_file).st_size == 0


def save_response_to_cache(response):
    f = open(cache_file, "w")
    f.write(str(response.json()))
    f.close()


def get_cached_content():
    with open(cache_file, "r") as file:
        return ast.literal_eval(file.read())


def check_if_calling_api_is_needed(country):
    if not is_cache_empty():
        cached_info = get_cached_content()
        try:
            return not cached_info.get("All").get("country") == country
        except AttributeError:
            return True
    else:
        return True


def get_covid_data(country):
    if check_if_calling_api_is_needed(country):
        response = call_covid_api(country)
        if response.ok:
            save_response_to_cache(response)
            return response.json()

        else:
            print(
                "Oh no, unfortunately, some external error occurred. Please try again later"
            )
            return 0
    elif get_cached_content().get("All").get("country") == country:
        return get_cached_content()
    else:
        return 1


def main():
    args = get_parsed_arguments()

    all_data = get_covid_data(args.country.capitalize())
    if all_data == 0:
        return 0
    elif all_data == 1:
        print(f"There is no data for country:\n{args.country}")
        return 1

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


if __name__ == "__main__":
    main()
