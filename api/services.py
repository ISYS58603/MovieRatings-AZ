import sqlite3
from typing import List
from api.models import User, Rating, Movie
from pathlib import Path

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.

    The connection uses 'data/movie_data.db' as the database file and sets the
    row factory to sqlite3.Row, allowing access to columns by name.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    DATABASE_PATH = Path(__file__).parents[1] / "data"
    connection = sqlite3.connect(DATABASE_PATH/'movie_data.db')
    connection.row_factory = sqlite3.Row  # This allows you to access columns by name
    return connection

def run_query(query, params=None):
    """
    Run a query on the database and return the results.

    Args:
        query (str): The SQL query to be executed.
        params (tuple, optional): The parameters to be passed to the query. Defaults to None.

    Returns:
        list of dict: A list of dictionaries representing the query results.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ---------------------------------------------------------
# Users
# ---------------------------------------------------------
def convert_rows_to_user_list(users):
    """
    Converts a list of user dictionaries to a list of User objects.

    Args:
        users (list): A list of dictionaries, where each dictionary contains
                      user information with keys 'user_id', 'username', and 'email'.

    Returns:
        list: A list of User objects created from the provided user dictionaries.
    """
    all_users = []
    # If nothing was passed in, return an empty list
    if users is None:
        return all_users
    for user in users:
        user = User(user["user_id"], user["username"], user["email"])
        all_users.append(user)
    return all_users


def get_all_users() -> List[User]:
    """
    Retrieve all users from the database.
    This function establishes a connection to the database, executes a query to
    fetch all users, and converts the result into a list of User objects.
    Returns:
        List[User]: A list of User objects representing all users in the database.
    """
    # We need to start by getting the connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for all users
    query = "SELECT user_id,username,email  FROM users"
    cursor.execute(query)
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects
    return convert_rows_to_user_list(users)


def get_user_by_id(user_id: int) -> User:
    """
    Retrieve a user from the database by their user ID.
    Args:
        user_id (int): The ID of the user to retrieve.
    Returns:
        User: The User object corresponding to the given user ID.
    Raises:
        Exception: If there is an issue with the database connection or query execution.
    """
    # We need to start by getting the connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for all users
    query = "SELECT user_id,username,email FROM users WHERE user_id = ?"
    # We need to pass the user_id as a tuple to be the parameters of the query
    cursor.execute(query, (user_id,))
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects, but only take the first object
    #  realy there should only ever be one or zero, but we will take the first one in case there are more
    user_list = convert_rows_to_user_list(users)
    if len(user_list) == 0:
        return None
    return user_list[0]

def get_users_by_name(username: str, starts_with: bool =True) -> List[User]:
    """
    Retrieve a list of users from the database whose usernames match the given pattern.
    Args:
        user_name (str): The username or partial username to search for.
        starts_with (bool, optional): If True, search for usernames that start with the given user_name.
                                        If False, search for usernames that contain the given user_name.
                                        Defaults to True.
    Returns:
        List[User]: A list of User objects that match the search criteria.
    """
    # We need to start by getting the connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for all users
    query = "SELECT user_id,username,email FROM users WHERE username like ?"
    
    # We use the % symbol as a wildcard to match any characters before or after the user_name
    params = f'{username}%' if starts_with else f'%{username}%'
    cursor.execute(query, (params,))
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects
    return convert_rows_to_user_list(users)

# Add a user to the database
def create_user(user: User) -> int:
    """
    Creates a new user in the database.
    Args:
        user (User): An instance of the User class containing the user's details.
    Returns:
        int: The ID of the newly created user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO users (username, email) VALUES (?, ?)"
    cursor.execute(query, (user.username, user.email))
    # Get the ID of the newly created user
    user_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return user_id

# Update a user in the database
def update_user(user: User):
    """
    Updates the username and email of an existing user in the database.
    Args:
        user (User): An instance of the User class containing the updated user information.
            - user.user_name (str): The new username for the user.
            - user.email (str): The new email for the user.
            - user.id (int): The unique identifier of the user to be updated.
    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE users SET username = ?, email = ? WHERE user_id = ?"
    cursor.execute(query, (user.username, user.email, user.id))
    
    conn.commit()
    conn.close()

# Delete a user from the database
def delete_user(user_id: int):
    """
    Deletes a user from the database based on the provided user ID.
    Args:
        user_id (int): The ID of the user to be deleted.
    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM users WHERE user_id = ?"
    cursor.execute(query, (user_id,))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Movies
# ---------------------------------------------------------
def convert_rows_to_movie_list(movies):
    """
    Converts a list of movie dictionaries to a list of Movie objects.

    Args:
        movies (list of dict): A list where each dictionary contains movie details
                               with keys 'movie_id', 'title', 'genre', 'release_year', and 'director'.

    Returns:
        list of Movie: A list of Movie objects created from the input dictionaries.
    """
    all_movies = []
    # If nothing was passed in, return an empty list
    if movies is None:
        return all_movies

    for movie in movies:
        movie = Movie(
            movie["movie_id"],
            movie["title"],
            movie["genre"],
            movie["release_year"],
            movie["director"],
        )
        all_movies.append(movie)
    return all_movies

def create_movie(movie: Movie) -> int:
    """
    Add a new movie to the database.
    Args:
        movie (Movie): A Movie object representing the movie to be added.
    Returns:
        int: The ID of the newly created movie.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO movies (title, genre, release_year, director) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (movie.title, movie.genre, movie.release_year, movie.director))
    movie_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return movie_id


def update_movie(movie: Movie):
    """
    Update a movie in the database.
    Args:
        movie (Movie): A Movie object containing the updated movie information.
    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE movies SET title = ?, genre = ?, release_year = ?, director = ? WHERE movie_id = ?"
    cursor.execute(
        query,
        (movie.title, movie.genre, movie.release_year, movie.director, movie.movie_id),
    )

    conn.commit()
    conn.close()


def delete_movie(movie_id: int):
    """
    Delete a movie from the database by its ID.
    Args:
        movie_id (int): The ID of the movie to be deleted.
    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM movies WHERE movie_id = ?"
    cursor.execute(query, (movie_id,))
    
    conn.commit()
    conn.close()

def get_all_movies() -> List[Movie]:
    """
    Retrieve all movies from the database.
    Returns:
        List[Movie]: A list of Movie objects representing all movies in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT movie_id,title,genre,release_year,director FROM movies"
    cursor.execute(query)

    movies = cursor.fetchall()
    conn.close()

    return convert_rows_to_movie_list(movies)


def get_movie_by_id(movie_id: int) -> Movie:
    """
    Retrieve a movie from the database by its ID.
    Args:
        movie_id (int): The ID of the movie to retrieve.
    Returns:
        Movie: A Movie object representing the movie with the given ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT movie_id,title,genre,release_year,director FROM movies WHERE movie_id = ?"
    cursor.execute(query, (movie_id,))

    movie = cursor.fetchone()
    conn.close()

    if movie is None:
        return None

    return Movie(
        movie["movie_id"],
        movie["title"],
        movie["genre"],
        movie["release_year"],
        movie["director"],
    )

def get_movies_by_name(title: str, starts_with: bool = True) -> List[Movie]:
    """
    Retrieve a list of movies from the database whose titles match the given pattern.
    Args:
        title (str): The movie title or partial title to search for.
        starts_with (bool, optional): If True, search for movie titles that start with the given title.
                                      If False, search for movie titles that contain the given title.
                                      Defaults to True.
    Returns:
        List[Movie]: A list of Movie objects that match the search criteria.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT movie_id,title,genre,release_year,director FROM movies WHERE title like ?"

    # If the starts_with value is True then we will search for movies that start with the title like (title%), 
    # otherwise we will search for movies that contain the title (%title%)
    params = f'{title}%' if starts_with else f'%{title}%'
    cursor.execute(query, (params,))

    movies = cursor.fetchall()
    conn.close()

    return convert_rows_to_movie_list(movies)

def get_movies_matching_criteria(genre: str ="", director: str ="", year: int=0) -> List[Movie]:
    """
    Retrieve a list of movies from the database that match the given criteria.
    Args:
        genre (str, optional): The genre of the movie to search for. Defaults to an empty string.
        director (str, optional): The director of the movie to search for. Defaults to an empty string.
        year (int, optional): The release year of the movie to search for. Defaults to 0.
        
    Returns:

        List[Movie]: A list of Movie objects that match the search criteria.
    """
    query = "SELECT movie_id,title,genre,release_year,director FROM movies WHERE "
    where_clauses = [] # A list to store the WHERE clauses for the query
    params = []
    if genre:
        where_clauses.append("genre like ?")
        params.append(f"%{genre}%")
    if director:
        where_clauses.append("director like ?")
        params.append(f"%{director}%")
    if year > 0:
        where_clauses.append("release_year = ?")
        params.append(year)

    where_clause = " AND ".join(where_clauses) # Join the WHERE clauses with an AND statement
    query += where_clause
    movies = run_query(query, params=params)
    return convert_rows_to_movie_list(movies)

# ---------------------------------------------------------
# Ratings
# ---------------------------------------------------------


def convert_rows_to_rating_list(ratings):
    """
    Converts a list of rating dictionaries to a list of Rating objects.

    Args:
        ratings (list of dict): A list of dictionaries where each dictionary
                                contains the keys 'rating_id', 'user_id',
                                'movie_id', 'rating', 'review', and 'date'.

    Returns:
        list of Rating: A list of Rating objects created from the input dictionaries.
    """
    all_ratings = []
    if ratings is None:
        return None
    for rating in ratings:
        rating = Rating(
            rating_id=rating["rating_id"],
            user_id=rating["user_id"],
            movie_id=rating["movie_id"],
            rating=rating["rating"],
            review=rating["review"],
            date=rating["date"],
        )
        all_ratings.append(rating)
    return all_ratings

def create_rating(rating: Rating) -> int:
    """
    Add a new rating to the database.
    Args:
        rating (Rating): A Rating object representing the rating to be added.
    Returns:
        int: The ID of the newly created rating.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO ratings (user_id, movie_id, rating, review, date) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (rating.user_id, rating.movie_id, rating.rating, rating.review, rating.date))
    rating_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return rating_id

def update_rating(rating: Rating):
    """
    Update a rating in the database.
    Args:
        rating (Rating): A Rating object containing the updated rating information.
    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE ratings SET user_id = ?, movie_id = ?, rating = ?, review = ?, date = ? WHERE rating_id = ?"
    cursor.execute(
        query,
        (rating.user_id, rating.movie_id, rating.rating, rating.review, rating.date, rating.rating_id),
    )

    conn.commit()
    conn.close()

def get_rating_by_id(rating_id: int) -> Rating:
    """
    Retrieve a rating from the database by its ID.
    Args:
        rating_id (int): The ID of the rating to retrieve.
    Returns:
        Rating: A Rating object representing the rating with the given ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT rating_id,user_id,movie_id,rating,review,date FROM ratings WHERE rating_id = ?"
    cursor.execute(query, (rating_id,))

    ratings = cursor.fetchall()
    conn.close()

    rating_list = convert_rows_to_rating_list(ratings)

    if len(rating_list) == 0:
        return None
    return rating_list[0]

def delete_rating(rating_id: int):
    """
    Delete a rating from the database by its ID.
    Args:
        rating_id (int): The ID of the rating to be deleted.
    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM ratings WHERE rating_id = ?"
    cursor.execute(query, (rating_id,))

    conn.commit()
    conn.close()

def get_movie_ratings(movie_id: int) -> List[Rating]:
    """
    Retrieve all ratings for a specific movie by movie ID.
    Args:
        movie_id (int): The unique identifier of the movie.
    Returns:
        List[Rating]: A list of Rating objects representing the ratings for the movie.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT rating_id, user_id, movie_id, rating,review,date FROM ratings WHERE movie_id = ?"
    cursor.execute(query, (movie_id,))

    ratings = cursor.fetchall()
    conn.close()

    return convert_rows_to_rating_list(ratings)

def get_user_ratings(user_id: int) -> List[Rating]:
    """
    Retrieve all ratings by a specific user.
    Args:
        user_id (int): The unique identifier of the user.
    Returns:
        List[Rating]: A list of Rating objects representing the ratings by the user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT rating_id, user_id, movie_id, rating,review,date FROM ratings WHERE user_id = ?"
    cursor.execute(query, (user_id,))

    ratings = cursor.fetchall()
    conn.close()

    return convert_rows_to_rating_list(ratings)
