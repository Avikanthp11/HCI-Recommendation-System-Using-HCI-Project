import unittest
from recommender import MovieRecommender

class RecommenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = MovieRecommender()

    def test_returns_five(self):
        self.assertEqual(len(self.engine.recommend("Orbit Rescue", 5)), 5)

    def test_excludes_selected_title(self):
        titles = [x["title"] for x in self.engine.recommend("Orbit Rescue", 10)]
        self.assertNotIn("Orbit Rescue", titles)

    def test_unknown_title(self):
        with self.assertRaises(ValueError):
            self.engine.recommend("Unknown Movie")

    def test_genre_filter(self):
        results = self.engine.recommend("Orbit Rescue", 5, "Sci-Fi")
        self.assertTrue(all("Sci-Fi" in x["genres"] for x in results))

if __name__ == "__main__":
    unittest.main()
