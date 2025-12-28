from fastapi import FastAPI, Query
from rss_parser import get_last_50_movies
from top_rated_parser import get_top_rated_movies

app = FastAPI(title="Letterboxd Backend")

@app.get("/get-profile")
def get_profile(username: str = Query(...)):
    movies = get_last_50_movies(username)
    return {
        "username": username,
        "movie_count": len(movies),
        "movies": movies
    }

@app.get("/get-top-rated")
def get_top_rated(username: str = Query(...)):
    movies = get_top_rated_movies(username)
    return {
        "username": username,
        "movie_count": len(movies),
        "movies": movies
    }

@app.get("/get-user-data")
def get_user_data(username: str = Query(...)):
    recent_movies = get_last_50_movies(username)
    top_rated_movies = get_top_rated_movies(username)

    return {
        "username": username,
        "recent_movies": {
            "movie_count": len(recent_movies),
            "movies": recent_movies
        },
        "top_rated_movies": {
            "movie_count": len(top_rated_movies),
            "movies": top_rated_movies
        }
    }
