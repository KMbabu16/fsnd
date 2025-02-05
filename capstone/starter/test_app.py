import os
import unittest
import json
from app import create_app
from models import setup_db, db, Actor, Movie
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from datetime import datetime


class FSNDTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ---------------------- GET Tests ----------------------

    def test_get_movies(self):
        res = self.client.get("/movies")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("total_movies" in data)
        self.assertTrue(len(data["movies"]) >= 0)

    def test_get_actors(self):
        res = self.client.get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("total_actors" in data)
        self.assertTrue(len(data["actors"]) >= 0)

    def test_get_movies_failure(self):
        res = self.client.get("/movies/100")  # Invalid ID
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    # ---------------------- DELETE Tests ----------------------

    def test_delete_actor_failure(self):
        res = self.client.delete("/actors/9999")  # Non-existent ID
        data = res.get_json()
        self.assertEqual(res.status_code, 404)

    # ---------------------- POST Tests ----------------------

    def test_submit_actor(self):
        new_actor = {"name": "Mohan", "age": 30, "gender": "Male"}
        res = self.client.post("/actors", json=new_actor)
        data = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)

    def test_submit_actor_failure(self):
        new_actor = {"name": "", "age": 7, "gender": "Male"}  # Empty name should fail
        res = self.client.post("/actors", json=new_actor)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)

    def test_submit_movie(self):
        # Step 1: Create an actor
        new_actor = {"name": "Test Actor", "age": 35, "gender": "Male"}
        actor_res = self.client.post("/actors", json=new_actor)
        actor_data = actor_res.get_json()
        actor_id = actor_data.get("actor_id")

        # Step 2: Create a movie using the valid `actor_id`
        new_movie = {
            "title": "Anime Movie",
            "release_date": "2025-01-01",
            "actor_id": actor_id,  # Ensure it's an integer
            "genres": "Anime"
        }
        res = self.client.post("/movies", json=new_movie)
        data = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)

    def test_submit_movie_failure(self):
        new_movie = {"release_date": "2025-01-01"}  # Missing title should fail
        res = self.client.post("/movies", json=new_movie)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)

    # ---------------------- SEARCH Tests ----------------------

    def test_search_actor_failure(self):
        search = {"searchTerm": "nonexistentname"}
        res = self.client.post("/actors/search", json=search)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)

    def test_search_movie_failure(self):
        search = {"searchTerm": "mohanbabu"}
        res = self.client.post("/movies/search", json=search)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)

    # ---------------------- RELATIONSHIP Tests ----------------------

    def test_movies_with_actors_failure(self):
        res = self.client.get("/movies/9999/actors")  # Non-existent movie ID
        data = res.get_json()
        self.assertEqual(res.status_code, 404)

    def test_movies_with_actors_failure2(self):
        res = self.client.get("/movies/9999")
        data = res.get_json()
        self.assertEqual(res.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
