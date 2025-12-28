from fastapi import FastAPI, Query
from rss_parser import get_last_50_movies
from top_rated_parser import get_top_rated_movies

app = FastAPI()

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
