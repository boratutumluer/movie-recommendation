from flask import render_template, request, redirect, url_for, session
from movie_recommendation import app
from .models import Movies


@app.route("/")
@app.route("/home")
def home_page():
    movies = Movies()
    movies = movies.get_all_movies()
    return render_template("home.html",
                           items=movies[["original_title", "popularity"]].sort_values("popularity",
                                                                                      ascending=False)[
                               "original_title"])


@app.route("/recommend", methods=["POST"])
def recommend_page():
    movies = Movies()
    all_movies = movies.get_all_movies()
    movie = request.form['movie']
    selected_movie = movies.get_movie(movie)
    recommended_movies = movies.get_similarity(selected_movie)
    session['recommended_movies'] = recommended_movies

    movie_poster = []
    movie_link = []
    for m in recommended_movies:
        link = movies.get_link(m)
        movie_link.append(link)
        poster = movies.get_poster(m)
        movie_poster.append(poster)

    return render_template("recommend.html",
                           items=all_movies[["original_title", "popularity"]].sort_values("popularity",
                                                                                          ascending=False)[
                               "original_title"],
                           recommended_movies=recommended_movies,
                           movie_link=movie_link,
                           movie_poster=movie_poster)


@app.route("/sorting", methods=["POST"])
def sorting_page():
    movies = Movies()
    all_movies = movies.get_all_movies()
    recommended_movies = session.get('recommended_movies')  # get recommended_movies recommend_page root function
    if request.form['sort_key'] == "rating":
        sorted_rec = movies.sorted_recommendations(recommended_movies, sort_key="weighted_sorting_score")
    elif request.form['sort_key'] == "popularity":
        sorted_rec = movies.sorted_recommendations(recommended_movies, sort_key="popularity")
    elif request.form['sort_key'] == "duration":
        sorted_rec = movies.sorted_recommendations(recommended_movies, sort_key="runtime")
    else:
        sorted_rec = recommended_movies

    movie_poster = []
    movie_link = []
    for sr in sorted_rec:
        link = movies.get_link(sr)
        movie_link.append(link)
        poster = movies.get_poster(sr)
        movie_poster.append(poster)

    return render_template("sorting.html", items=
    all_movies[["original_title", "popularity"]].sort_values("popularity", ascending=False)["original_title"],
                           sorted_rec=sorted_rec, movie_link=movie_link, movie_poster=movie_poster)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")
