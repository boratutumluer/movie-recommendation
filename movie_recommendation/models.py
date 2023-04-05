import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


class Movies:
    def __init__(self):
        self.movie_data = pd.read_csv("dataset/movies.csv")

    def get_all_movies(self):
        movies = self.movie_data
        return movies

    def get_movie(self, movie_title):
        movie_name = self.movie_data.loc[self.movie_data["original_title"] == movie_title, "original_title"].values[0]
        return movie_name

    def get_similarity(self, movie_name):
        tfidf = TfidfVectorizer(stop_words="english")
        self.movie_data["overview"] = self.movie_data["overview"].fillna('')
        tfidf_matrix = tfidf.fit_transform(self.movie_data["overview"])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        indices = pd.Series(self.movie_data.index, index=self.movie_data["original_title"])
        indices = indices[~indices.index.duplicated(keep="last")]
        movie_index = indices[movie_name]
        similarity_score = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
        movie_indices = similarity_score.sort_values("score", ascending=False)[1:6].index
        recommended_movies = list(self.movie_data.iloc[movie_indices]["original_title"])
        return recommended_movies

    def get_poster(self, movie_recommended_name):
        movies = self.get_all_movies()
        movie_poster = movies.loc[movies["original_title"] == movie_recommended_name, "poster_url"].values[0]
        return movie_poster

    def get_link(self, movie_recommended_name):
        movies = self.get_all_movies()
        movie_link = movies.loc[movies["original_title"] == movie_recommended_name, "movie_url"].values[0]
        return movie_link

    def weighted_sorting_score(self, w1=26, w2=32, w3=42):
        self.movie_data["vote_count_scale"] = MinMaxScaler(feature_range=(1, 10)).fit(
            self.movie_data["vote_count"].values.reshape(-1, 1)).transform(
            self.movie_data["vote_count"].values.reshape(-1, 1))
        self.movie_data["popularity_count_scale"] = MinMaxScaler(feature_range=(1, 10)).fit(
            self.movie_data["popularity"].values.reshape(-1, 1)).transform(
            self.movie_data["popularity"].values.reshape(-1, 1))
        return self.movie_data["vote_average"] * w3 / 100 + self.movie_data["popularity_count_scale"] * w2 / 100 + \
            self.movie_data["vote_count_scale"] * w1 / 100

    def sorted_recommendations(self, recommendations, sort_key):
        self.movie_data["weighted_sorting_score"] = self.weighted_sorting_score()
        sorted_rec = list(self.movie_data.loc[
                              self.movie_data["original_title"].isin(recommendations), ["original_title",
                                                                                        sort_key]].sort_values(sort_key,
                                                                                                               ascending=False)[
                              "original_title"])
        return sorted_rec
