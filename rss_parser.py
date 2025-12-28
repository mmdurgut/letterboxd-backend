import requests
import xml.etree.ElementTree as ET

NAMESPACES = {
    "letterboxd": "https://letterboxd.com",
    "tmdb": "https://themoviedb.org"
}

def get_last_50_movies(username: str):
    rss_url = f"https://letterboxd.com/{username}/rss/"
    response = requests.get(rss_url)

    if response.status_code != 200:
        raise Exception("RSS alınamadı")

    root = ET.fromstring(response.text)

    movies = []

    for item in root.findall(".//item"):
        film_title = item.find("letterboxd:filmTitle", NAMESPACES)

        # Film değilse (liste vs.) atla
        if film_title is None:
            continue

        title = film_title.text
        year = item.find("letterboxd:filmYear", NAMESPACES).text

        rating_elem = item.find("letterboxd:memberRating", NAMESPACES)
        rating = float(rating_elem.text) if rating_elem is not None else None

        link = item.find("link").text

        movie = {
            "title": title,
            "year": int(year),
            "rating": rating,
            "letterboxd_link": link
        }

        movies.append(movie)

        if len(movies) == 50:
            break

    return movies
