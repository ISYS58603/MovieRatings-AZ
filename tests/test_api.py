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

    # Purpose: This test ensures that the GET /api/users route returns a 200 status code and a list of users.
    # Notice that this test method takes the test_client fixture as an argument. This allows the test method to access the test client and make requests to the API.
    def test_get_all_users(self, test_client):
        # Use the test client to make a GET request to the /api/users route
        response = test_client.get("/api/users")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0

    # Purpose: This test ensures that the GET /api/users/<user_id> route returns a 200 status code and the correct user.
    def test_create_user_route(self, test_client):
        # Create a sample user data
        user_data = {"username": "test_user", "email": "testuser@example.com"}
        # Use the test client to make a GET request to the /api/users route
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

    # Purpose: This test ensures that the PUT /api/users/<user_id> route returns a 200 status code and updates the user correctly.
    def test_update_user_route(self, test_client):
        # We start by creating a user to update, then we update the user and verify the update.
        # Create a user to update
        user_data = {"username": "update_user", "email": "updateuser@example.com"}
        # Use the test client to make a GET request to the /api/users route
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

    # Purpose: This test ensures that the DELETE /api/users/<user_id> route returns a 200 status code and the correct user.
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


# The TestMovieRoutes class contains test methods for the movie routes.  It's a bit more complex than the TestUserRoutes class
# we'll use function level fixtures to create a movie and clean up after the tests.
class TestMovieRoutes:

    # This fixture creates a movie and provides the movie object. The movie is deleted after the test is run.
    @pytest.fixture(scope="class")
    def movie_fixture(test_client):
        # Create a movie
        movie = Movie(movie_id=None,
            title="Test Movie", 
            genre="Horror", 
            director="Wes Kraven", 
            release_year=2021
        )
        movie_data = movie.to_dict()
        response = test_client.post("/api/movies", json=movie_data)
        data = json.loads(response.data)
        # Get the id returned from the insert and assign it to the movie object
        movie.id = data["id"]

        # Yield the movie ID
        yield movie

        # Clean up
        test_client.delete(f"/api/movies/{movie.id}")

    # This test ensures that the GET /api/movies route returns a 200 status code and a list of movies.
    def test_get_all_movies(self, test_client):
        response = test_client.get("/api/movies")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0
    
    # This test ensures that the GET /api/movies?title=<movie_title> route returns a 200 status code and the correct movie.
    def test_get_movie_by_name(self, test_client, movie_fixture):
        response = test_client.get(f"/api/movies?title={movie_fixture.title}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["title"] == movie_fixture.title
        assert data[0]["genre"] == movie_fixture.genre
        assert data[0]["director"] == movie_fixture.director
        assert data[0]["release_year"] == movie_fixture.release_year

    # def test_get_movie_by_id(self, test_client, movie_fixture):
    #     response = test_client.get(f"/api/movies/{movie_fixture.id}")
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data["title"] == movie_fixture.title
    #     assert data["genre"] == movie_fixture.genre
    #     assert data["director"] == movie_fixture.director
    #     assert data["release_year"] == movie_fixture.release_year

    # This test ensures that the GET /api/movies/<movie_id> route returns a 200 status code and the correct movie.
    def test_create_movie(self, test_client):
        movie_data = {"title": "Inception", "release_year": 2010}
        response = test_client.post("/api/movies", json=movie_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["title"] == movie_data["title"]
        assert data["year"] == movie_data["year"]
        # Clean up
        test_client.delete(f"/api/movies/{data['id']}")


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
