from fastapi import FastAPI, Query
from rss_parser import get_last_50_movies
from top_rated_parser import get_top_rated_movies

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
@app.get("/get-top-rated")
def get_top_rated(username: str = Query(..., example="mmdurgut")):
    try:
        movies = get_top_rated_movies(username)
        return {
            "username": username,
            "movie_count": len(movies),
            "movies": movies
        }
    except Exception as e:
        return {"error": str(e)}
