import csv
from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from config import driver


def get_tables_for_country(country: str) -> List[WebElement]:
    try:
        dropdown = Select(driver.find_element(by=By.ID, value="country"))
        dropdown.select_by_visible_text(text=country.lower().capitalize())
        driver.find_element(
            by=By.XPATH, value='//label[@analytics-event="All matches"]'
        ).click()

        return driver.find_elements(by=By.TAG_NAME, value="table")
    except Exception:
        return None


def get_table_rows(table: WebElement) -> List[WebElement]:
    return table.find_elements(By.TAG_NAME, "tr")


def get_match(row: WebElement) -> Dict[str, str]:
    cols = row.find_elements(By.TAG_NAME, "td")
    home_team_element = row.find_element(
        By.CSS_SELECTOR, 'td[style*="font-weight: bold"]'
    )
    home_team = home_team_element.text
    away_team = cols[1].text if cols[1].text != home_team else cols[3].text

    try:
        score = cols[2].text.split(" - ")
        home_score = int(score[0]) if cols[1].text == home_team else int(score[1])
        away_score = int(score[0]) if cols[1].text == away_team else int(score[1])
    except ValueError:
        return {}

    return {
        "date": cols[0].text,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
    }


def write_list_into_csv(
    fieldnames: List[str], filename: str, data: List[Dict[str, str]]
):

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for match in data:
            writer.writerow(match)
