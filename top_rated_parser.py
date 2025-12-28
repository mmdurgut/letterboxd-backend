import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple


BASE_URL = "https://letterboxd.com"


def _stars_to_float(stars_text: str) -> Optional[float]:
    """
    Converts Letterboxd star text like '★★★★½' into 4.5
    Returns None if no rating is found/recognized.
    """
    if not stars_text:
        return None
    stars_text = stars_text.strip()
    # Count full stars and half star
    full = stars_text.count("★")
    half = 0.5 if "½" in stars_text else 0.0
    if full == 0 and half == 0:
        return None
    return full + half


def _split_title_year(item_name: str) -> Tuple[str, Optional[int]]:
    """
    'Naked (1993)' -> ('Naked', 1993)
    Fallback: if year not found, return (original, None)
    """
    if not item_name:
        return "", None

    # Typical format: Title (1993)
    m = re.match(r"^(.*)\s+\((\d{4})\)\s*$", item_name.strip())
    if m:
        title = m.group(1).strip()
        year = int(m.group(2))
        return title, year

    return item_name.strip(), None


def get_top_rated_movies(username: str, max_pages: int = 10) -> List[Dict]:
    """
    Scrapes Letterboxd 'films/by/entry-rating' pages for a user.
    Returns a list of {title, year, rating}.

    max_pages limits how many pages we scan to avoid excessive requests.
    """
    if not username or not username.strip():
        raise ValueError("username is required")

    username = username.strip().strip("/")  # normalize

    session = requests.Session()
    session.headers.update({
        # Friendly User-Agent improves stability for basic scraping
        "User-Agent": "Mozilla/5.0 (compatible; LetterboxdBot/1.0; +https://github.com/)"
    })

    results: List[Dict] = []
    page = 1

    while page <= max_pages:
        # Page 1 has no /page/1/ in many Letterboxd URLs; but both forms can work.
        if page == 1:
            url = f"{BASE_URL}/{username}/films/by/entry-rating/"
        else:
            url = f"{BASE_URL}/{username}/films/by/entry-rating/page/{page}/"

        resp = session.get(url, timeout=20)
        if resp.status_code == 404:
            # Profile or page not found (private user or invalid username)
            break
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        grid_items = soup.select("li.griditem")

        # If no items found, we reached the end
        if not grid_items:
            break

        for li in grid_items:
            # Example: data-item-name="Naked (1993)"
            poster_div = li.select_one("div.react-component[data-item-name]")
            if not poster_div:
                continue

            item_name = poster_div.get("data-item-name", "")
            title, year = _split_title_year(item_name)

            # Rating is in: <p class="poster-viewingdata"> <span class="rating ...">★★★★½</span>
            rating_span = li.select_one("p.poster-viewingdata span.rating")
            rating_value = _stars_to_float(rating_span.get_text(strip=True) if rating_span else "")

            # We only care about films that have a rating on this page.
            # The page is "by entry-rating", so it should mostly be rated,
            # but we guard anyway.
            if title:
                results.append({
                    "title": title,
                    "year": year,
                    "rating": rating_value
                })

        page += 1

    # Filter out items without rating if you want strict "top-rated only"
    results = [r for r in results if r.get("rating") is not None]

    return results
