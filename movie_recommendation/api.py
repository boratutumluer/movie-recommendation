import pandas as pd
import csv
import requests

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_rows", None)

tmdb = pd.read_csv("dataset/tmdb_5000_movies.csv")
metadata = pd.read_csv("dataset/movies_metadata.csv")
tmdb["id"] = tmdb["id"].astype(str)
tmdb = tmdb.merge(metadata[["imdb_id", "id"]])
tmdb["movie_url"] = tmdb["imdb_id"].map(lambda x: 'http://www.imdb.com/title/' + x + '/?ref_=fn_al_tt_1')


def get_poster_url():
    poster_url = {"id": [], "url": [], "success_false": []}
    for id in tmdb["id"]:
        try:
            print(id)
            r = requests.get(
                f"https://api.themoviedb.org/3/movie/{id}?api_key=57487b7722336999b8d39ab3d5c94009&language=en-US")
            data = r.json()
            image = data["poster_path"]
            image_url = "https://image.tmdb.org/t/p/original" + image
            poster_url["id"].append(id)
            poster_url["url"].append(image_url)
        except Exception as e:
            print(id, e)
            poster_url["success_false"].append(id)
            continue
    return poster_url


poster_url = get_poster_url()

posters = pd.DataFrame({"id": poster_url["id"], "poster_url": poster_url["url"]})
tmdb = tmdb.merge(posters, on="id")
tmdb = tmdb[
    ["id", "original_title", "genres", "overview", "popularity", "runtime", "vote_average", "vote_count", "movie_url",
     "poster_url"]]
tmdb.to_csv("dataset/movies.csv")
