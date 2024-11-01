import pytest
import api.services as services
from api.models import User, Rating, Movie

# This set of tests will test the database connection and the services module
# It is important to test the database connection and the services module to ensure that the database is set up correctly and that the services module is working as expected
# The way this file is setup is to just use a list of functions as the tests, there are no classes in this module
# It is a simple way to write tests and keep everything in one file


# Fixtures are used to set up the test environment before running the tests
# They are used to create objects that are used in the tests
# The objects created by the fixtures are passed to the test functions as arguments
@pytest.fixture
def known_user():
    # Create a known user for testing purposes
    user = User(None, "known_user", "knownuser@example.com")
    user.id = services.create_user(user)
    yield user
    # Delete the known user after the test
    services.delete_user(user.id)


@pytest.fixture
def known_movie():
    # Create a new movie for testing purposes
    movie = Movie(
        None, "test_movie", "test_genre", release_year=2024, director="Test Director"
    )
    movie.movie_id = services.create_movie(movie)
    yield movie
    # Delete the movie after the test
    services.delete_movie(movie.movie_id)

@pytest.fixture
def new_rating():
    rating = Rating(
        user_id=101,
        movie_id=1,
        rating=5,
        review="Great movie!",
        date="2022-01-01",
    )
    rating.rating_id = services.create_rating(rating)
    yield rating
    # Delete the rating after the test
    services.delete_rating(rating.rating_id)

def test_create_connection():
    conn = services.get_db_connection()
    assert conn is not None
    conn.close()


def test_run_query():
    results = services.run_query("SELECT * FROM users where username like '%%'")
    assert len(results) > 0


def test_get_all_users():
    all_users = services.get_all_users()
    assert len(all_users) > 0

# This test will use the known_user fixture to create a user and then test the get_user_by_id function
def test_get_user_by_id(known_user):
    """ Test the get_user_by_id function """
    user = services.get_user_by_id(known_user.id)
    assert user is not None
    assert user.id == known_user.id
    assert user.username == known_user.username


def test_get_users_by_starts_with_name(known_user):
    # We're going to take just the first three characters of the username and search for users
    users = services.get_users_by_name(known_user.username[:3], starts_with=True)
    assert len(users) > 0
    for user in users:
        assert known_user.username[:3] in user.username[:3].lower()

    # Now test for the opposite case, where we shouldn't get the user back
    users = services.get_users_by_name("xyz", starts_with=True)
    assert len(users) == 0


def test_get_users_by_contains_name(known_user):
    users = services.get_users_by_name(known_user.username, starts_with=False)
    assert len(users) > 0
    for user in users:
        assert known_user.username in user.username.lower()

    # Now test for a user where just a part of the name is in the username
    users = services.get_users_by_name("xyz", starts_with=False)
    assert len(users) == 0
    for user in users:
        assert "xyz" in user.username.lower()


def test_create_user():
    new_user = User(None, "test_user", "testuser@example.com")
    new_user.id = services.create_user(new_user)
    assert new_user.id is not None

    # Now get the user back and check that it is the same
    user = services.get_user_by_id(new_user.id)
    assert user.username == new_user.username
    assert user.email == new_user.email
    services.delete_user(new_user.id)


def test_update_user(known_user):
    # Update the user
    known_user.username = "updated_user"
    services.update_user(known_user)
    updated_user = services.get_user_by_id(known_user.id)
    assert updated_user.username == "updated_user"


def test_delete_user(known_user):
    # Delete the user
    services.delete_user(known_user.id)
    deleted_user = services.get_user_by_id(known_user.id)
    assert deleted_user is None

# ---------------------------------------------------------
# This set of tests will test the database connection and the services module for the MOVIES table
# ---------------------------------------------------------
def test_get_all_movies():
    all_movies = services.get_all_movies()
    assert len(all_movies) > 0


def test_get_movie_by_id(known_movie):
    movie = services.get_movie_by_id(known_movie.movie_id)
    assert movie is not None
    assert movie.title == "test_movie"
    assert movie.genre == "test_genre"
    assert movie.release_year == 2024
    assert movie.director == "Test Director"


def test_create_movie():
    movie = Movie(
        None, "test_movie", "test_genre", release_year=2024, director="Test Director"
    )
    movie.movie_id = services.create_movie(movie)
    assert movie.movie_id is not None

    # Now get the movie back and check that it is the same
    retrieved_movie = services.get_movie_by_id(movie.movie_id)
    assert retrieved_movie.title == movie.title
    assert retrieved_movie.genre == movie.genre
    assert retrieved_movie.release_year == movie.release_year
    assert retrieved_movie.director == movie.director
    services.delete_movie(movie.movie_id)


def test_delete_movie(known_movie):
    # Delete the movie
    services.delete_movie(known_movie.movie_id)
    deleted_movie = services.get_movie_by_id(known_movie.movie_id)
    assert deleted_movie is None


def test_update_movie(known_movie):
    # Update the movie
    known_movie.title = "updated_movie"
    services.update_movie(known_movie)
    updated_movie = services.get_movie_by_id(known_movie.movie_id)
    assert updated_movie.title == "updated_movie"


def test_get_movie_by_criteria_all(known_movie):
    # Do the test
    movies = services.get_movies_matching_criteria(
        genre="test_genre", director="Test Director", year=2024
    )
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == "test_movie"
        assert movie.genre == "test_genre"
        assert movie.release_year == 2024
        assert movie.director == "Test Director"

    # Now test for the opposite case, where we shouldn't get the movie back
    movies = services.get_movies_matching_criteria(
        genre="test_genre", director="Test Director2", year=2024
    )
    assert len(movies) == 0


def test_movie_by_criteria_director(known_movie):
    # Do the test
    movies = services.get_movies_matching_criteria(director="Test Director")
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == "test_movie"

    # Now test for the opposite case, where we shouldn't get the movie back
    movies = services.get_movies_matching_criteria(director="Test Director2")
    assert len(movies) == 0


def test_movie_by_criteria_genre(known_movie):
    # Do the test
    movies = services.get_movies_matching_criteria(genre=known_movie.genre)
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == known_movie.title

    # Now test for the opposite case, where we shouldn't get the movie back
    movies = services.get_movies_matching_criteria(genre="test_genre2")
    assert len(movies) == 0

def test_movie_by_criteria_multiple(known_movie):
    # Do the test
    movies = services.get_movies_matching_criteria(
        director=known_movie.director, genre=known_movie.genre
    )
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == known_movie.title

    movies = services.get_movies_matching_criteria(
        genre=known_movie.genre,
        year=known_movie.release_year,
    )
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == known_movie.title
# ---------------------------------------------------------
# This set of tests will test the database connection and the services module for the RATINGS table
# ---------------------------------------------------------
def test_get_rating_by_id(new_rating):
    # Get the rating by id
    rating = services.get_rating_by_id(new_rating.rating_id)
    assert rating is not None
    assert rating.rating_id == new_rating.rating_id

def test_get_movie_ratings(known_movie):
    # Create a sample rating
    sample_rating = Rating(
        user_id=101,
        movie_id=known_movie.movie_id,
        rating=5,
        review="Great movie!",
        date="1/1/2024",
    )
    sample_rating.rating_id = services.create_rating(sample_rating)

    # Create a sample rating
    sample_rating2 = Rating(
        user_id=101,
        movie_id=known_movie.movie_id,
        rating=3,
        review="So so movie!",
        date="2/1/2024",
    )
    sample_rating2.rating_id = services.create_rating(sample_rating2)

    # Get the ratings for the movie
    ratings = services.get_movie_ratings(known_movie.movie_id)
    assert len(ratings) > 0
    for rating in ratings:
        assert rating.movie_id == known_movie.movie_id

    # Clean up
    services.delete_rating(sample_rating.rating_id)
    services.delete_rating(sample_rating2.rating_id)

def test_get_rating_by_user(new_rating):
    # Get the rating by user
    ratings = services.get_user_ratings(new_rating.user_id)
    assert len(ratings) > 0
    for rating in ratings:
        assert rating.user_id == new_rating.user_id


def test_delete_rating(new_rating):
    # Delete the rating
    services.delete_rating(new_rating.rating_id)
    deleted_rating = services.get_rating_by_id(new_rating.rating_id)
    assert deleted_rating is None

def test_update_rating(new_rating):
    # Update the rating
    new_rating.rating = 4
    services.update_rating(new_rating)
    updated_rating = services.get_rating_by_id(new_rating.rating_id)
    assert updated_rating.rating == 4

def test_create_rating():
    rating = Rating(
        user_id=101,
        movie_id=1,
        rating=5,
        review="Great movie!",
        date="2022-01-01",
    )
    rating.rating_id = services.create_rating(rating)
    assert rating.rating_id is not None

    # Now get the rating back and check that it is the same
    retrieved_rating = services.get_rating_by_id(rating.rating_id)
    assert retrieved_rating.user_id == rating.user_id
    assert retrieved_rating.movie_id == rating.movie_id
    assert retrieved_rating.rating == rating.rating
    assert retrieved_rating.review == rating.review
    assert retrieved_rating.date == rating.date
    services.delete_rating(rating.rating_id)

def test_get_user_ratings(known_user, known_movie):
    # Create a sample rating
    sample_rating = Rating(
        user_id=known_user.id,
        movie_id=known_movie.movie_id,
        rating=5,
        review="Great movie!",
        date="1/1/2024",
    )
    sample_rating.rating_id = services.create_rating(sample_rating)

    # Create a sample rating
    sample_rating2 = Rating(
        user_id=known_user.id,
        movie_id=known_movie.movie_id,
        rating=3,
        review="So so movie!",
        date="2/1/2024",
    )
    sample_rating2.rating_id = services.create_rating(sample_rating2)

    # Get the ratings for the user
    ratings = services.get_user_ratings(known_user.id)
    assert len(ratings) > 0
    for rating in ratings:
        assert rating.user_id == known_user.id

    # Clean up
    services.delete_rating(sample_rating.rating_id)
    services.delete_rating(sample_rating2.rating_id)
