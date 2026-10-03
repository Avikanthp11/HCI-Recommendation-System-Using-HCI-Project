from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    """Content-based recommender using TF-IDF and cosine similarity."""
    def __init__(self, csv_path=None):
        csv_path = csv_path or Path(__file__).parent / "data" / "movies.csv"
        self.movies = pd.read_csv(csv_path).fillna("")
        required = {"title", "genres", "keywords"}
        missing = required - set(self.movies.columns)
        if missing:
            raise ValueError(f"Missing dataset columns: {sorted(missing)}")
        self.movies["features"] = (
            self.movies["genres"].str.replace("|", " ", regex=False)
            + " " + self.movies["keywords"]
        )
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.movies["features"])
        self.similarity = cosine_similarity(self.matrix)

    def titles(self):
        return sorted(self.movies["title"].tolist())

    def genres(self):
        all_genres = set()
        for value in self.movies["genres"]:
            all_genres.update(value.split("|"))
        return ["All Genres"] + sorted(all_genres)

    def recommend(self, title, top_n=5, genre_filter="All Genres"):
        matches = self.movies.index[
            self.movies["title"].str.casefold() == str(title).casefold()
        ].tolist()
        if not matches:
            raise ValueError(f'Movie "{title}" was not found.')
        idx = matches[0]
        source_genres = set(self.movies.loc[idx, "genres"].split("|"))
        ranked = sorted(enumerate(self.similarity[idx]), key=lambda x: x[1], reverse=True)
        results = []
        for movie_idx, score in ranked:
            if movie_idx == idx:
                continue
            row = self.movies.loc[movie_idx]
            genres = set(row["genres"].split("|"))
            if genre_filter != "All Genres" and genre_filter not in genres:
                continue
            shared = sorted(source_genres & genres)
            results.append({
                "title": row["title"],
                "genres": row["genres"].replace("|", ", "),
                "score": round(float(score) * 100, 1),
                "explanation": "Shared genres: " + ", ".join(shared)
                    if shared else "Similar descriptive keywords",
            })
            if len(results) >= int(top_n):
                break
        return results

if __name__ == "__main__":
    engine = MovieRecommender()
    for item in engine.recommend("Orbit Rescue", 5):
        print(f"{item['title']}: {item['score']}% - {item['explanation']}")
