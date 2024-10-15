import pytest
from run import create_app
from api.models import User, Rating, Movie, create_user_from_dict
from api import services
from flask import json


@pytest.fixture(scope="module")
def test_client():
    # Set up Flask test client
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as testing_client:
        yield testing_client


@pytest.fixture
def test_user():
    # Create a known user for testing purposes
    user = User(None, "known_user", "knownuser@example.com")
    user.id = services.create_user(user)
    yield user
    # Delete the known user after the test
    services.delete_user(user.id)

@pytest.fixture
def test_movie():
    # Create a new movie for testing purposes
    movie = Movie(None, "test_movie", "test_genre", release_year=2024, director="Test Director")
    movie.movie_id = services.create_movie(movie)
    yield movie
    # Delete the movie after the test
    services.delete_movie(movie.movie_id)

@pytest.fixture
def known_rating(test_user, test_movie):
    # Create a new rating for testing purposes via API
    rating = Rating(
            rating_id=None,
            user_id=test_user.id,
            movie_id=test_movie.movie_id,
            rating=4.5,
            review="Great movie!",
            date="03/03/2024",
        )
    rating_id = services.create_rating(rating)
    rating.rating_id = rating_id
    
    yield rating
    
    # Delete the rating after the test
    services.delete_rating(rating_id)
    

@pytest.fixture
def test_ratings(test_user, test_movie):
    """Fixture to set up multiple ratings for a movie."""
    ratings = [
        Rating(rating_id=None, user_id=test_user.id, movie_id=test_movie.movie_id, rating=4.5, review="Great movie!", date="03/03/2024"),
        Rating(rating_id=None, user_id=test_user.id, movie_id=test_movie.movie_id, rating=3.0, review="Not bad!", date="04/30/2024"),
        Rating(rating_id=None, user_id=test_user.id, movie_id=test_movie.movie_id, rating=5.0, review="Excellent movie!", date="8/13/2024"),
    ]
    for rating in ratings:
        rating_id = services.create_rating(rating)
        rating.rating_id = rating_id

    yield ratings

    # Clean up after tests
    for rating in ratings:
        services.delete_rating(rating.rating_id)


class TestDatabaseConnection:
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

    def test_get_user_by_id(self, test_client, test_user):
        response = test_client.get(f"/api/users/{test_user.id}")
        assert response.status_code == 200
        user = json.loads(response.data)
        assert user is not None
        assert user["id"] == test_user.id
        assert user["username"] == test_user.username

    def test_get_users_by_starts_with_name(self, test_client, test_user):
        partial_name = test_user.username[:3]
        response = test_client.get(f"/api/users?starts_with={partial_name}")
        assert response.status_code == 200
        users = json.loads(response.data)
        assert len(users) > 0
        for user in users:
            assert partial_name in user["username"].lower()

        # Now test for the opposite case, where we shouldn't get the user back
        response = test_client.get("/api/users?starts_with=xxxy")
        assert response.status_code == 200
        users = json.loads(response.data)
        assert len(users) == 0

    def test_get_users_by_contains_name(self, test_client, test_user):
        partial_name = test_user.username[3:]
        response = test_client.get(f"/api/users?contains={partial_name}")
        assert response.status_code == 200
        users = json.loads(response.data)
        assert len(users) > 0
        for user in users:
            assert partial_name in user["username"].lower()

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

    def test_update_user(self, test_client, test_user):
        # Update the user
        updated_data = {"username": "updated_user", "email": "knownuser@example.com"}
        response = test_client.put(f"/api/users/{test_user.id}", json=updated_data)
        assert response.status_code == 200

        # Verify update
        response = test_client.get(f"/api/users/{test_user.id}")
        updated_user = json.loads(response.data)
        assert updated_user["username"] == "updated_user"

    def test_delete_user(self, test_client, test_user):
        # Delete the user
        response = test_client.delete(f"/api/users/{test_user.id}")
        assert response.status_code == 200

        # Verify deletion
        response = test_client.get(f"/api/users/{test_user.id}")
        assert response.status_code == 404


class TestMovieRoutes:
    def test_get_all_movies(self, test_client):
        response = test_client.get("/api/movies")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0

    def test_get_movie_by_id(self, test_client,test_movie):
        response = test_client.get(f"/api/movies/{test_movie.movie_id}")
        assert response.status_code == 200
        movie = json.loads(response.data)
        assert movie is not None
        assert movie["movie_id"] == test_movie.movie_id
        assert movie["title"] == test_movie.title
        
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
        movie_id = data["movie"]["movie_id"]
        assert movie_id is not None

        # Now get the movie back and check that it is the same
        response = test_client.get(f"/api/movies/{movie_id}")
        movie = json.loads(response.data)
        assert movie["title"] == movie_data["title"]
        assert movie["genre"] == movie_data["genre"]
        assert movie["release_year"] == movie_data["release_year"]
        assert movie["director"] == movie_data["director"]
        test_client.delete(f"/api/movies/{movie_id}")

    def test_delete_movie(self, test_client, test_movie):
        # Delete the movie
        response = test_client.delete(f"/api/movies/{test_movie.movie_id}")
        assert response.status_code == 200

        # Verify deletion
        response = test_client.get(f"/api/movies/{test_movie.movie_id}")
        assert response.status_code == 404

    def test_update_movie(self, test_client, test_movie):
        # Update the movie
        updated_data = {
            "title": "updated_movie",
            "genre": "test_genre",
            "release_year": 2024,
            "director": "Test Director",
        }
        response = test_client.put(f"/api/movies/{test_movie.movie_id}", json=updated_data)
        assert response.status_code == 200

        # Verify update
        response = test_client.get(f"/api/movies/{test_movie.movie_id}")
        updated_movie = json.loads(response.data)
        assert updated_movie["title"] == "updated_movie"

class TestReviewRoutes:

    def test_create_review(self, test_client, test_movie, test_user):
        rating_data = {
            "user_id": test_user.id,
            "movie_id": test_movie.movie_id,
            "rating": 5,
            "review": "Great movie!",
            "date": "3/3/2024",
        }
        response = test_client.post("/api/ratings", json=rating_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        rating_id = data["rating"]["rating_id"]
        assert rating_id is not None

        # Now get the review back and check that it is the same
        response = test_client.get(f"/api/ratings/{rating_id}")
        rating = json.loads(response.data)
        assert rating["rating"] == 5
        assert rating["review"] == "Great movie!"
        test_client.delete(f"/api/ratings/{rating_id}")

    def test_get_review_by_id(self, test_client, known_rating):
        response = test_client.get(f"/api/ratings/{known_rating.rating_id}")
        assert response.status_code == 200
        rating = json.loads(response.data)
        assert rating is not None
        assert rating["rating_id"] == known_rating.rating_id
        assert rating["rating"] == known_rating.rating


    def test_get_ratings_by_movie(self, test_client, test_movie, test_ratings):
        """Test getting ratings for a specific movie by its ID."""
        response = test_client.get(f"/api/movies/{test_movie.movie_id}/ratings")
        assert response.status_code == 200
        data = response.get_json()
        ratings = data.get("ratings", None)
        assert len(ratings) == len(test_ratings)

        for rating, rating_data in zip(test_ratings, ratings):
            assert rating_data["rating"] == rating.rating
            assert rating_data["review"] == rating.review
