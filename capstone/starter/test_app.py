import os
import unittest
import json
from app import create_app
from models import setup_db, db, Actor, Movie
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from datetime import datetime

import os
import unittest
import json
from app import create_app
from models import setup_db

class FSNDTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()  

        # Set your valid JWT token here (replace with actual token)
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZFUVB0eXA4RUxHQjBhLVpsTDd2biJ9.eyJpc3MiOiJodHRwczovL2Rldi1vbTgwbTU0N2h3eGlwbzcyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiI0cHN2NUYya1BTcU5zWkU5MWJHajc0aVZNUDNkMTIzcUBjbGllbnRzIiwiYXVkIjoiZnNuZCIsImlhdCI6MTczODkwODc0MCwiZXhwIjoxNzM4OTk1MTQwLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiI0cHN2NUYya1BTcU5zWkU5MWJHajc0aVZNUDNkMTIzcSJ9.LwkgsFVpcRE1spZbEWpueBoLY7Ic8FBxzNOeClSOo1fo8HR-shVNTmegAA2-xUhhxsneGeT92cJ7GY7pyipxZindNF3fWiGAORL2ao91p3zExxRNwNUoBBe4d5iBVGMDsuLUWz8P5zoXCqkj_i9XK1BwYJC9WsNF4S4Ic3zHnvV-RqWNVSt37_7qiuhbo2zfZQDfW0EStOrLr5M2qIqn46Af3v1z2LUn12NhBZ0yw92aHpwJL8dqPsYh_zWmVAsxWjre7NFgBhGvgGNrywJyWhjInopa8QWmRFIXEcE-U0Afe_byZrATwSzEqCcTYY4wPGapW_aWLA4W8jNCzRZYlQ"

        # Set headers for authentication
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ---------------------- GET Tests ----------------------

    def test_get_movies(self):
        res = self.client.get("/movies", headers=self.headers) 
        data = json.loads(res.data)
        print("get movie",data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("total_movies" in data)
        self.assertTrue(len(data["movies"]) >= 0)

    def test_get_actors(self):
        res = self.client.get("/actors", headers=self.headers)
        data = json.loads(res.data)
        print("get actor",data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("total_actors" in data)
        self.assertTrue(len(data["actors"]) >= 0)


    def test_get_movies_failure(self):
        res = self.client.get("/movies/100", headers=self.headers) 
        data = json.loads(res.data)
        print("movie fail",data)
        self.assertEqual(res.status_code, 405)

    # ---------------------- DELETE Tests ----------------------

    def test_delete_actor_failure(self):
        res = self.client.delete("/actors/2", headers=self.headers)  
        data = res.get_json()
        print("delete actor",data)
        self.assertEqual(res.status_code, 200)
    def test_delete_movie_failure(self):
        res = self.client.delete("/movies/2", headers=self.headers)  
        data = res.get_json()
        print("delete movie",data)
        self.assertEqual(res.status_code, 200)
        
    #----------------------PATCH Tsts--------------------------
    def test_patch_actor(self):
        actor = {"name": "Mohan", "age": 30, "gender": "Male"}
        res = self.client.patch("/actors/1", json=actor, headers=self.headers)
        data = res.get_json()
        print("patch actor",data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    def test_patch_movie(self):
        actor = {"title": "Anime Movie","release_date": "2025-01-01","genres": "Anime"}
        res = self.client.patch("/movies/1", json=actor, headers=self.headers) 
        data = res.get_json()
        print("patch movie",data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # ---------------------- POST Tests ----------------------

    def test_submit_actor(self):
        new_actor = {"name": "Mohan", "age": 30, "gender": "Male"}
        res = self.client.post("/actors", json=new_actor, headers=self.headers) 
        data = res.get_json()
        print("new actor",data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)


    def test_submit_actor_failure(self):
        new_actor = {"name": "", "age": 7, "gender": "Male"}  
        res = self.client.post("/actors", json=new_actor,headers=self.headers)
        data = res.get_json()
        print("actor new fail",data)
        self.assertEqual(res.status_code, 400)

    def test_submit_movie(self):
        new_movie = {
            "title": "Anime Movie",
            "release_date": "2025-01-01",
            "genres": "Anime"
        }
        res = self.client.post("/movies", json=new_movie, headers=self.headers) 
        data = res.get_json()
        print("new movie",data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)



    def test_submit_movie_failure(self):
        new_movie = {"release_date": "2025-01-01"} 
        res = self.client.post("/movies", json=new_movie,headers=self.headers)
        data = res.get_json()
        print("new movie fail",data)
        self.assertEqual(res.status_code, 400)

    # ---------------------- RELATIONSHIP Tests ----------------------

    def test_movies_with_actors_failure(self):
        res = self.client.get("/movies/9999/actors",headers=self.headers)
        data = res.get_json()
        print(data)
        self.assertEqual(res.status_code, 404)

    def test_movies_with_actors_failure2(self):
        res = self.client.get("/movies/9999",headers=self.headers)
        data = res.get_json()
        print(data)
        self.assertEqual(res.status_code, 405)


if __name__ == "__main__":
    unittest.main()
