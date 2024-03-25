import re
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from config import HOME_URL


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def get_all_links(url: str, number_of_pages: int) -> List[str]:
    links = []

    for i in range(number_of_pages):
        links.append(f"{url}?page={i+1}")

    return links


def get_movies_links(url: str) -> List[str]:
    response = requests.get(url, timeout=100)
    soup = BeautifulSoup(response.content, "html.parser")

    article = soup.find("article", "main-article")
    links = [f"{HOME_URL}{link['href']}" for link in article.find_all("a") if link]

    print(f"[INFO] Found {len(links)} links")
    return links


def parse_movie_transcript(url: str) -> Dict[str, str]:
    response = requests.get(url, timeout=100)
    soup = BeautifulSoup(response.content, "html.parser")

    movie_name = slugify(soup.find("h1").get_text(strip=True))
    transcript = soup.find("div", "full-script").get_text(separator="\n", strip=True)

    print(f"[INFO] Successfully parsed script for {movie_name}")
    return {"name": movie_name, "script": transcript}


def write_data_into_file(file_path: str, text: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
