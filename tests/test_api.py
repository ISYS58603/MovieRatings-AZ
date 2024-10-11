import pytest
from run import create_app
from api.models import User, Rating, Movie
from flask import json


@pytest.fixture(scope="module")
def test_client():
    # Set up Flask test client
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as testing_client:
        yield testing_client


@pytest.fixture
def known_user(test_client):
    # Create a known user for testing purposes via API
    user_data = {"username": "known_user", "email": "knownuser@example.com"}
    response = test_client.post("/api/users", json=user_data)
    data = json.loads(response.data)
    user_id = data["user"]["id"]
    yield user_id
    # Delete the known user after the test
    test_client.delete(f"/api/users/{user_id}")


@pytest.fixture
def new_movie(test_client):
    # Create a new movie for testing purposes via API
    movie_data = {
        "title": "test_movie",
        "genre": "test_genre",
        "release_year": 2024,
        "director": "Test Director",
    }
    response = test_client.post("/api/movies", json=movie_data)
    data = json.loads(response.data)
    movie_id = data["movie"]["id"]
    yield movie_id
    # Delete the movie after the test
    test_client.delete(f"/api/movies/{movie_id}")


class TestDatabaseConnections:
    def test_create_connection(self, test_client):
        response = test_client.get("/api/connection")
        assert response.status_code == 200

    def test_run_query(self, test_client):
        response = test_client.get("/api/users?username=%%")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0


class TestUserRoutes:
    def test_get_all_users(self, test_client):
        response = test_client.get("/api/users")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0

    def test_get_user_by_id(self, test_client):
        response = test_client.get("/api/users/1")
        assert response.status_code == 200
        user = json.loads(response.data)
        assert user is not None
        assert user["id"] == 1
        assert user["username"] == "jane_doe"

    def test_get_users_by_starts_with_name(self, test_client):
        response = test_client.get("/api/users?starts_with=jane")
        assert response.status_code == 200
        users = json.loads(response.data)
        assert len(users) > 0
        for user in users:
            assert "jane" in user["username"].lower()

        # Now test for the opposite case, where we shouldn't get the user back
        response = test_client.get("/api/users?starts_with=wilson")
        assert response.status_code == 200
        users = json.loads(response.data)
        assert len(users) == 0

    def test_get_users_by_contains_name(self, test_client):
        response = test_client.get("/api/users?contains=jane")
        assert response.status_code == 200
        users = json.loads(response.data)
        assert len(users) > 0
        for user in users:
            assert "jane" in user["username"].lower()

        # Now test for a user where just a part of the name is in the username
        response = test_client.get("/api/users?contains=wilson")
        assert response.status_code == 200
        users = json.loads(response.data)
        assert len(users) > 0
        for user in users:
            assert "wilson" in user["username"].lower()

    def test_create_user(self, test_client):
        user_data = {"username": "test_user", "email": "testuser@example.com"}
        response = test_client.post("/api/users", json=user_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        user_id = data["user"]["id"]
        assert user_id is not None

        # Now get the user back and check that it is the same
        response = test_client.get(f"/api/users/{user_id}")
        user = json.loads(response.data)
        assert user["username"] == user_data["username"]
        assert user["email"] == user_data["email"]
        test_client.delete(f"/api/users/{user_id}")

    def test_update_user(self, test_client, known_user):
        # Update the user
        updated_data = {"username": "updated_user", "email": "knownuser@example.com"}
        response = test_client.put(f"/api/users/{known_user}", json=updated_data)
        assert response.status_code == 200

        # Verify update
        response = test_client.get(f"/api/users/{known_user}")
        updated_user = json.loads(response.data)
        assert updated_user["username"] == "updated_user"

    def test_delete_user(self, test_client, known_user):
        # Delete the user
        response = test_client.delete(f"/api/users/{known_user}")
        assert response.status_code == 200

        # Verify deletion
        response = test_client.get(f"/api/users/{known_user}")
        assert response.status_code == 404


class TestMovieRoutes:
    def test_get_all_movies(self, test_client):
        response = test_client.get("/api/movies")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0

    def test_create_movie(self, test_client):
        movie_data = {
            "title": "test_movie",
            "genre": "test_genre",
            "release_year": 2024,
            "director": "Test Director",
        }
        response = test_client.post("/api/movies", json=movie_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        movie_id = data["movie"]["id"]
        assert movie_id is not None

        # Now get the movie back and check that it is the same
        response = test_client.get(f"/api/movies/{movie_id}")
        movie = json.loads(response.data)
        assert movie["title"] == movie_data["title"]
        assert movie["genre"] == movie_data["genre"]
        assert movie["release_year"] == movie_data["release_year"]
        assert movie["director"] == movie_data["director"]
        test_client.delete(f"/api/movies/{movie_id}")

    def test_delete_movie(self, test_client, new_movie):
        # Delete the movie
        response = test_client.delete(f"/api/movies/{new_movie}")
        assert response.status_code == 200

        # Verify deletion
        response = test_client.get(f"/api/movies/{new_movie}")
        assert response.status_code == 404

    def test_update_movie(self, test_client, new_movie):
        # Update the movie
        updated_data = {
            "title": "updated_movie",
            "genre": "test_genre",
            "release_year": 2024,
            "director": "Test Director",
        }
        response = test_client.put(f"/api/movies/{new_movie}", json=updated_data)
        assert response.status_code == 200

        # Verify update
        response = test_client.get(f"/api/movies/{new_movie}")
        updated_movie = json.loads(response.data)
        assert updated_movie["title"] == "updated_movie"

    def test_get_movie_by_criteria_all(self, test_client, new_movie):
        # Do the test
        response = test_client.get(
            "/api/movies?genre=test_genre&director=Test+Director&year=2024"
        )
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) > 0
        for movie in movies:
            assert movie["title"] == "test_movie"
            assert movie["genre"] == "test_genre"
            assert movie["release_year"] == 2024
            assert movie["director"] == "Test Director"

        # Now test for the opposite case, where we shouldn't get the movie back
        response = test_client.get(
            "/api/movies?genre=test_genre&director=Test+Director2&year=2024"
        )
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) == 0

    def test_movie_by_criteria_director(self, test_client, new_movie):
        # Do the test
        response = test_client.get("/api/movies?director=Test+Director")
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) > 0
        for movie in movies:
            assert movie["title"] == "test_movie"

        # Now test for the opposite case, where we shouldn't get the movie back
        response = test_client.get("/api/movies?director=Test+Director2")
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) == 0

    def test_movie_by_criteria_genre(self, test_client, new_movie):
        # Do the test
        response = test_client.get(f"/api/movies?genre=test_genre")
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) > 0
        for movie in movies:
            assert movie["title"] == "test_movie"

        # Now test for the opposite case, where we shouldn't get the movie back
        response = test_client.get("/api/movies?genre=test_genre2")
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) == 0

    def test_movie_by_criteria_multiple(self, test_client, new_movie):
        # Do the test
        response = test_client.get(
            f"/api/movies?director=Test+Director&genre=test_genre"
        )
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) > 0
        for movie in movies:
            assert movie["title"] == "test_movie"

        response = test_client.get(f"/api/movies?genre=test_genre&year=2024")
        assert response.status_code == 200
        movies = json.loads(response.data)
        assert len(movies) > 0
        for movie in movies:
            assert movie["title"] == "test_movie"
