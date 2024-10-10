import pytest
from run import create_app
from api.models import User, Movie, Rating
from flask import json

# Purpose: The test_client fixture sets up a Flask test client that allows you to make requests to your API routes without actually running the server.
# It simulates HTTP requests and allows you to easily test API endpoints.
# Scope: The scope='module' indicates that this fixture is created once per module and shared among all the tests in the module.
# This helps reduce setup and teardown time when running multiple tests in a single module.
@pytest.fixture(scope="module")
def test_client():
    # Set up Flask test client
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as testing_client:
        yield testing_client


class TestUserRoutes:

    def test_get_all_users(self, test_client):
        response = test_client.get("/api/users")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0

    def test_create_user_route(self, test_client):
        user_data = {"username": "test_user", "email": "testuser@example.com"}
        response = test_client.post("/api/users", json=user_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        user_data = data.get("user")
        if user_data:
            assert user_data["username"] == user_data["username"]
            assert user_data["email"] == user_data["email"]
        else:
            # Throw an error if the user data is not found
            assert False
        # Clean up
        test_client.delete(f"/api/users/{user_data['id']}")

    def test_update_user_route(self, test_client):
        # Create a user to update
        user_data = {"username": "update_user", "email": "updateuser@example.com"}
        response = test_client.post("/api/users", json=user_data)
        data = json.loads(response.data)
        user_id = json.loads(response.data)["user"]["id"]

        # Update the user
        updated_data = {"username": "updated_user", "email": user_data["email"]}
        response = test_client.put(f"/api/users/{user_id}", json=updated_data)
        assert response.status_code == 200

        # Verify update
        response = test_client.get(f"/api/users/{user_id}")
        data = json.loads(response.data)
        assert data["username"] == "updated_user"

        # Clean up
        test_client.delete(f"/api/users/{user_id}")

    def test_delete_user_route(self, test_client):
        # Create a user to delete
        user_data = {"username": "delete_user", "email": "deleteuser@example.com"}
        response = test_client.post("/api/users", json=user_data)
        data = json.loads(response.data)
        user_id = json.loads(response.data)["user"]["id"]

        # Delete the user
        response = test_client.delete(f"/api/users/{user_id}")
        assert response.status_code == 200

        # Verify deletion
        response = test_client.get(f"/api/users/{user_id}")
        assert response.status_code == 404


# class TestMovieRoutes:

#     def test_get_all_movies(self, test_client):
#         response = test_client.get("/api/movies")
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert len(data) > 0

#     def test_create_movie(self, test_client):
#         movie_data = {"title": "Inception", "year": 2010}
#         response = test_client.post("/api/movies", json=movie_data)
#         assert response.status_code == 201
#         data = json.loads(response.data)
#         assert data["title"] == movie_data["title"]
#         assert data["year"] == movie_data["year"]
#         # Clean up
#         test_client.delete(f"/api/movies/{data['id']}")


# class TestRatingRoutes:

#     def test_create_rating(self, test_client):
#         # Create user and movie for rating
#         user_data = {"user_name": "rating_user", "email": "ratinguser@example.com"}
#         movie_data = {"title": "The Matrix", "year": 1999}
#         user_response = test_client.post("/api/users", json=user_data)
#         movie_response = test_client.post("/api/movies", json=movie_data)
#         user_id = json.loads(user_response.data)["id"]
#         movie_id = json.loads(movie_response.data)["id"]

#         # Create a rating
#         rating_data = {
#             "user_id": user_id,
#             "movie_id": movie_id,
#             "rating": 5,
#             "review": "Great movie!",
#         }
#         response = test_client.post("/api/ratings", json=rating_data)
#         assert response.status_code == 201
#         data = json.loads(response.data)
#         assert data["rating"] == rating_data["rating"]
#         assert data["review"] == rating_data["review"]

#         # Clean up
#         test_client.delete(f"/api/users/{user_id}")
#         test_client.delete(f"/api/movies/{movie_id}")
