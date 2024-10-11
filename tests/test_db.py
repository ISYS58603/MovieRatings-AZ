import pytest
import api.services as services
from api.models import User, Rating, Movie


@pytest.fixture
def known_user():
    # Create a known user for testing purposes
    user = User(None, "known_user", "knownuser@example.com")
    user.id = services.create_user(user)
    yield user
    # Delete the known user after the test
    services.delete_user(user.id)


@pytest.fixture
def new_movie():
    # Create a new movie for testing purposes
    movie = Movie(
        None, "test_movie", "test_genre", release_year=2024, director="Test Director"
    )
    movie.id = services.create_movie(movie)
    yield movie
    # Delete the movie after the test
    services.delete_movie(movie.id)


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


def test_get_user_by_id():
    user = services.get_user_by_id(1)
    assert user is not None
    assert user.id == 1
    assert user.username == "jane_doe"


def test_get_users_by_starts_with_name():
    users = services.get_users_by_name("jane")
    assert len(users) > 0
    for user in users:
        assert "jane" in user.username.lower()

    # Now test for the opposite case, where we shouldn't get the user back
    users = services.get_users_by_name("wilson")
    assert len(users) == 0


def test_get_users_by_contains_name():
    users = services.get_users_by_name("jane", starts_with=False)
    assert len(users) > 0
    for user in users:
        assert "jane" in user.username.lower()

    # Now test for a user where just a part of the name is in the username
    users = services.get_users_by_name("wilson", starts_with=False)
    assert len(users) > 0
    for user in users:
        assert "wilson" in user.username.lower()


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


def test_get_all_movies():
    all_movies = services.get_all_movies()
    assert len(all_movies) > 0


def test_create_movie():
    movie = Movie(
        None, "test_movie", "test_genre", release_year=2024, director="Test Director"
    )
    movie.id = services.create_movie(movie)
    assert movie.id is not None

    # Now get the movie back and check that it is the same
    retrieved_movie = services.get_movie_by_id(movie.id)
    assert retrieved_movie.title == movie.title
    assert retrieved_movie.genre == movie.genre
    assert retrieved_movie.release_year == movie.release_year
    assert retrieved_movie.director == movie.director
    services.delete_movie(movie.id)


def test_delete_movie(new_movie):
    # Delete the movie
    services.delete_movie(new_movie.id)
    deleted_movie = services.get_movie_by_id(new_movie.id)
    assert deleted_movie is None


def test_update_movie(new_movie):
    # Update the movie
    new_movie.title = "updated_movie"
    services.update_movie(new_movie)
    updated_movie = services.get_movie_by_id(new_movie.id)
    assert updated_movie.title == "updated_movie"


def test_get_movie_by_criteria_all(new_movie):
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


def test_movie_by_criteria_director(new_movie):
    # Do the test
    movies = services.get_movies_matching_criteria(director="Test Director")
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == "test_movie"

    # Now test for the opposite case, where we shouldn't get the movie back
    movies = services.get_movies_matching_criteria(director="Test Director2")
    assert len(movies) == 0


def test_movie_by_criteria_genre(new_movie):
    # Do the test
    movies = services.get_movies_matching_criteria(genre=new_movie.genre)
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == new_movie.title

    # Now test for the opposite case, where we shouldn't get the movie back
    movies = services.get_movies_matching_criteria(genre="test_genre2")
    assert len(movies) == 0


def test_movie_by_criteria_multiple(new_movie):
    # Do the test
    movies = services.get_movies_matching_criteria(
        director=new_movie.director, genre=new_movie.genre
    )
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == new_movie.title

    movies = services.get_movies_matching_criteria(
        genre=new_movie.genre,
        year=new_movie.release_year,
    )
    assert len(movies) > 0
    for movie in movies:
        assert movie.title == new_movie.title
