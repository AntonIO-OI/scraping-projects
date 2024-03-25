import time

from config import driver
from utils import get_match, get_table_rows, get_tables_for_country, write_list_into_csv


def main():
    time.sleep(1)
    country = input("Enter country to get list of matches: ")
    time.sleep(1)
    tables = get_tables_for_country(country)

    if not tables:
        print(f"Couldn't find any data about matches for {country}")
        return

    rows = []
    matches = []

    # Get all the tables with football statistics
    for table in tables:
        rows.extend(get_table_rows(table))

    # Get information about the match in each row
    for row in rows:
        match = get_match(row)
        if not match:
            continue
        matches.append(match)

    fieldnames = ["date", "home_team", "away_team", "home_score", "away_score"]
    filename = f"data/football_matches_{country}.csv"
    print(f"Data parsed successfully\nSaving in {filename}")

    write_list_into_csv(fieldnames, filename, matches)


if __name__ == "__main__":
    main()
    driver.quit()
