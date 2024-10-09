import sqlite3
from models import User, Rating, Movie
from typing import List
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
    for user in users:
        user = User(user['user_id'], user['username'], user['email'])
        all_users.append(user)
    return all_users

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
    for rating in ratings:
        rating = Rating(rating['rating_id'], rating['user_id'], rating['movie_id'], rating['rating'], rating['review'], rating['date'])
        all_ratings.append(rating)
    return all_ratings

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
    for movie in movies:
        movie = Movie(movie['movie_id'], movie['title'], movie['genre'], movie['release_year'], movie['director'])
        all_movies.append(movie)
    return all_movies

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
    return convert_rows_to_user_list(users)[0]

def get_users_by_name(user_name: str, starts_with: bool =True) -> List[User]:
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
    params = f'{user_name}%' if starts_with else f'%{user_name}%'
    cursor.execute(query, (params,))
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects
    return convert_rows_to_user_list(users)

# Add a user to the database
def create_user(user: User):
    """
    Creates a new user in the database.
    Args:
        user (User): An instance of the User class containing the user's details.
    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO users (username, email) VALUES (?, ?)"
    cursor.execute(query, (user.user_name, user.email))
    
    conn.commit()
    conn.close()

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
    cursor.execute(query, (user.user_name, user.email, user.id))
    
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

if __name__ == '__main__':
        
    # Usage
    ## Test to see if all users are returned
    # print("Get all users")
    # all_users = get_all_users()
    # for user in all_users:
    #    print(user)

    ## Test to get a single user by id
    # print(get_user_by_id(1))

    ## Test to get a list of users by name
    # Test to get a list of users by name that start with the provided string
    # print('Starts with')
    # print("-----------")
    # for n in get_users_by_name('l'):
    #     print(n)

    # # Test to get a list of users by name that start with the provided string
    # print('Contains')
    # print("-----------")
    # for name in get_users_by_name('luke', False):
    #     print(name)

    # Test to create a user
    print("Create a user")
    print("-----------")
    new_user = User(None, 'test_user', 'testuser@example.com')
    create_user(new_user)
    added_user = get_users_by_name('test_user')[0]
    print(added_user)

    # Test to update a user
    print("Update a user")
    print("-----------")
    # Start by getting the user to update
    user_to_update = get_users_by_name('test_user')[0]
    print(user_to_update)
    # Update the user
    user_to_update.user_name = 'updated_user'
    update_user(user_to_update)
    # Get the user again to see the changes
    updated_user = get_user_by_id(user_to_update.id)
    print(updated_user)

    # # Test to remove a user 
    # print('Now delete the user')
    # print("-----------")
    # # Start by getting the last user put into the database
    # last_user = get_all_users()[-1]
    # delete_user(last_user.id)
    # print(get_users_by_name(last_user.user_name))
