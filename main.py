from fastapi import FastAPI, Query
from rss_parser import get_last_50_movies

app = FastAPI(title="Letterboxd Backend")

@app.get("/get-profile")
def get_profile(username: str = Query(..., example="mmdurgut")):
    try:
        movies = get_last_50_movies(username)
        return {
            "username": username,
            "movie_count": len(movies),
            "movies": movies
        }
    except Exception as e:
        return {
            "error": str(e)
        }
