from api import models
from api.models import Rating, Movie, User

def test_create_user_from_dict():
    user_dict = {
        "id": 10000,
        "username": "test_user",
        "email": "test_user@example.com"
    }
    user = models.create_user_from_dict(user_dict)
    assert user.username == user_dict["username"]
    assert user.email == user_dict["email"]
    assert user.id == user_dict["id"]

def test_user_to_dict():
    user = User(10000, username="test_user", email="test_user@example.com")
    user_dict = user.to_dict()
    assert user_dict["username"] == user.username
    assert user_dict["email"] == user.email
    assert user_dict["id"] == user.id

def test_create_movie_from_dict():
    movie_dict = {
        "movie_id": 10000,
        "title": "test_movie",
        "genre": "test_genre",
        "release_year": 2024,
        "director": "Test Director"
    }
    movie = Movie.from_dict(movie_dict)
    assert movie.movie_id == movie_dict["movie_id"]
    assert movie.title == movie_dict["title"]
    assert movie.genre == movie_dict["genre"]
    assert movie.release_year == movie_dict["release_year"]
    assert movie.director == movie_dict["director"]

def test_movie_to_dict_without_ratings():
    movie = Movie(10000, title="test_movie", genre="test_genre", release_year=2024, director="Test Director")
    movie_dict = movie.to_dict()
    assert movie_dict["title"] == movie.title
    assert movie_dict["genre"] == movie.genre
    assert movie_dict["release_year"] == movie.release_year
    assert movie_dict["director"] == movie.director
    assert movie_dict["movie_id"] == movie.movie_id    


def test_movie_to_dict_with_ratings():
    movie = models.Movie(
        10000,
        title="test_movie",
        genre="test_genre",
        release_year=2024,
        director="Test Director",
    )
    sample_rating_1 = Rating(
        user_id=101,
        movie_id=movie.movie_id,
        rating=5,
        review="Great movie!",
        date="2022-01-01",
        rating_id=100,
    )
    sample_rating_2 = Rating(
        user_id=100,
        movie_id=movie.movie_id,
        rating=5,
        review="Great movie!",
        date="2022-01-01",
        rating_id=102,
    )

    movie.ratings = [sample_rating_1, sample_rating_2]
    movie_dict = movie.to_dict()
    assert movie_dict["title"] == movie.title
    assert movie_dict["genre"] == movie.genre
    assert movie_dict["release_year"] == movie.release_year
    assert movie_dict["director"] == movie.director
    assert movie_dict["movie_id"] == movie.movie_id
    for rating in movie.ratings:
        assert rating.to_dict() in movie_dict["ratings"]
