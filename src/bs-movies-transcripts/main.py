from config import NUMBER_OF_PAGES, URL
from utils import (
    get_all_links,
    get_movies_links,
    parse_movie_transcript,
    write_data_into_file,
)


def main():
    links = get_all_links(URL, NUMBER_OF_PAGES)
    movie_links = []
    for link in links[:5]:
        movie_links.extend(get_movies_links(link))

    for movie_link in movie_links:
        movie_data = parse_movie_transcript(movie_link)
        write_data_into_file(
            f"transcripts/{movie_data['name']}.txt", movie_data["script"]
        )


if __name__ == "__main__":
    main()
