from flask import jsonify, request, Blueprint
import api.services as services
from api.models import User, create_user_from_dict, Movie, Rating

# Create a Blueprint instance
# This will allow us to group related routes together. All the routes in this file will be part of the 'api' Blueprint.
# This means that the routes will be accessible at '/api/' followed by the route path.
# For instance, the route '/users' will be accessible at '/api/users'.
# We can then register the Blueprint with the Flask app in the main.py file.

api_bp = Blueprint("api", __name__)

@api_bp.route('/')
def home():
    return 'Welcome to the User API!', 200

@api_bp.route('/connection')
def test_connection():
    """
    Test the database connection.

    Returns:
        tuple: A tuple containing a JSON response with a message and an HTTP status code.
    """
    services.get_db_connection()
    return jsonify({'message': 'Successfully connected to the API'}), 200
    return "Connection successful!"

# ---------------------------------------------------------
# Users
# ---------------------------------------------------------
@api_bp.route("/users", methods=["GET"])
def get_users():
    """
    Retrieve a list of all users or filter users by name.
    If the query string parameter "starts_with" is provided, filter users by name.
    If the query string parameter "contains" is provided, filter users by name containing the string.

    Returns:
        tuple: A tuple containing a JSON response with all users and an HTTP status code 200.
    """
    # Example: /api/users?starts_with=A
    # Example: /api/users?contains=John
    # Example: /api/users
    
    # Get the query string parameter "starts_with" from the request if it's there
    user_name = request.args.get("starts_with")  # Accessing query string parameter
    # If user_name is not provided
    if not user_name:
        # See if the query string parameter "contains" is provided
        contains_user_name = request.args.get("contains")
        if contains_user_name:
            user_list = services.get_users_by_name(contains_user_name, starts_with=False)
        # If neither "starts_with" nor "contains" is provided, get all users
        else:
            user_list = services.get_all_users()
    else:
        # If user_name is provided, filter users by name
        user_list = services.get_users_by_name(user_name)

    # Convert the list of User objects to a list of dictionaries so that we can jsonify it
    user_dict_list = [user.to_dict() for user in user_list]
    return (jsonify(user_dict_list), 200)

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def lookup_user_by_id(user_id):
    """
    Retrieve user information by user ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            - If the user is found, returns a JSON object with user information and status code 200.
            - If the user is not found, returns a JSON object with an error message and status code 404.
    """
    
    # Example: /api/users/1
    
    # Using the database services to get the user by ID
    user = services.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404

@api_bp.route('/users/<int:user_id>/ratings', methods=['GET'])
def lookup_ratings_for_user(user_id):
    """
    Retrieve all ratings for a specific user by user ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        tuple: A tuple containing a JSON response with all ratings for the user and an HTTP status code.
    """
    return jsonify('Not implemented yet'), 501
    # ratings = services.get_user_ratings(user_id)
    # rating_list = [rating.to_dict() for rating in ratings]
    # rating_list.user_id = user_id
    # return jsonify(rating_list), 200

@api_bp.route('/users', methods=['POST'])
def add_new_user():
    """
    Adds a new user to the system.

    This function retrieves user data from a JSON request, creates a new User object,
    and adds it to the system using the create_user function.
    
    {
        "username": "new_user",
        "email": "new_user@example.com"
    }

    Returns:
        Response: A JSON response containing a success message and the added user,
                  with a status code of 201 (Created).
    """
    new_user_dict = request.get_json()
    # We can also use the create_user_from_dict function to create a User object
    new_user = User(None, new_user_dict['username'], new_user_dict['email'])
    new_user.id = services.create_user(new_user)
    return jsonify({'message': 'User added', 'user': new_user.to_dict()}), 201

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_existing_user(user_id):
    """
    Update an existing user with the provided user ID.

    This function retrieves user data from the request's JSON payload,
    creates a user object from the dictionary, and updates the user
    in the database.

    Args:
        user_id (int): The ID of the user to be updated.

    Returns:
        Response: A JSON response containing a message and the updated user object,
                  along with an HTTP status code 200.
    """
    user_dict = request.get_json()
    # We can also just create a user directly from the dictionary if we want
    user_dict['id'] = user_id
    user = create_user_from_dict(user_dict)
    services.update_user(user)
    return jsonify({'message': 'User updated', 'user': user.to_dict()}), 200

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    """
    Remove a user by their user ID.

    This function deletes a user from the database and returns a JSON response
    indicating that the user has been deleted.

    Args:
        user_id (int): The ID of the user to be removed.

    Returns:
        tuple: A tuple containing a JSON response with a message and an HTTP status code.
    """
    services.delete_user(user_id)
    return jsonify({'message': 'User deleted'}), 200

# ---------------------------------------------------------
# Movies
# ---------------------------------------------------------
@api_bp.route('/movies', methods=['GET'])
def get_movies():
    """
    Retrieve a list of all movies.
    If the query string parameter "title" is provided, filter movies by title.
    
    Returns:
        tuple: A tuple containing a JSON response with all movies and an HTTP status code 200.
    """
    movie_name = request.args.get("title")
    # If a "start_with" query parameter is provided, filter movies by name otherwise get all movies
    movies = services.get_movies_by_name(movie_name, starts_with=True) if movie_name else services.get_all_movies()
    
    # Convert the list of Movie objects to a list of dictionaries so that we can jsonify it
    movie_list = [movie.to_dict() for movie in movies]
    return jsonify(movie_list), 200

@api_bp.route('/movies/<int:movie_id>', methods=['GET'])
def lookup_movie_by_id(movie_id):
    """
    Retrieve movie information by movie ID.

    Args:
        movie_id (int): The unique identifier of the movie.
        
    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            - If the movie is found, returns a JSON object with movie information and status code 200.
            - If the movie is not found, returns a JSON object with an error message and status code 404.
    """
    movie = services.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie.to_dict()), 200
    return jsonify({'message': 'Movie not found'}), 404

@api_bp.route('/movies/<int:movie_id>/ratings', methods=['GET'])
def lookup_ratings_for_movie(movie_id): 
    """
    Retrieve all ratings for a specific movie by movie ID.

    Args:
        movie_id (int): The unique identifier of the movie.

    Returns:
        tuple: A tuple containing a JSON response with all ratings for the movie and an HTTP status code.
    """
    ratings = services.get_movie_ratings(movie_id)
    rating_list = ratings
    movie = services.get_movie_by_id(movie_id)
    movie.ratings = rating_list
    return jsonify(movie.to_dict()), 200


@api_bp.route('/movies', methods=['POST'])
def add_new_movie():
    """
    Adds a new movie to the system.

    This function retrieves movie data from a JSON request, creates a new Movie object,
    and adds it to the system using the create_movie function.

    Returns:
        Response: A JSON response containing a success message and the added movie,
                  with a status code of 201 (Created).
    """
    new_movie_dict = request.get_json()
    new_movie = Movie.from_dict(new_movie_dict)
    new_movie_id = services.create_movie(new_movie)
    new_movie.movie_id = new_movie_id
    return jsonify({'message': 'Movie added', 'movie': new_movie.to_dict()}), 201

@api_bp.route('/movies/<int:movie_id>', methods=['PUT'])
def update_existing_movie(movie_id):
    """
    Update an existing movie with the provided movie ID.

    This function retrieves movie data from the request's JSON payload,
    creates a movie object from the dictionary, and updates the movie
    in the database.

    Args:
        movie_id (int): The ID of the movie to be updated.

    Returns:
        Response: A JSON response containing a message and the updated movie object,
                  along with an HTTP status code 200.
    """
    movie_dict = request.get_json()
    movie = Movie.from_dict(movie_dict)
    movie.movie_id = movie_id
    services.update_movie(movie)
    return jsonify({'message': 'Movie updated', 'movie': movie.to_dict()}), 200

@api_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def remove_movie(movie_id):
    """
    Remove a movie by its movie ID.

    This function deletes a movie from the database and returns a JSON response
    indicating that the movie has been deleted.

    Args:
        movie_id (int): The ID of the movie to be removed.

    Returns:
        tuple: A tuple containing a JSON response with a message and an HTTP status code.
    """
    services.delete_movie(movie_id)
    return jsonify({'message': 'Movie deleted'}), 200

# ---------------------------------------------------------
# Ratings
# ---------------------------------------------------------
@api_bp.route('/ratings', methods=['POST'])
def add_new_rating():
    """
    Adds a new rating to the system.

    This function retrieves rating data from a JSON request, creates a new Rating object,
    and adds it to the system using the create_rating function.

    Returns:
        Response: A JSON response containing a success message and the added rating,
                  with a status code of 201 (Created).
    """
    new_rating_dict = request.get_json()
    new_rating = Rating.from_dict(new_rating_dict)
    new_rating_id = services.create_rating(new_rating)
    new_rating.rating_id = new_rating_id
    return jsonify({'message': 'Rating added', 'rating': new_rating.to_dict()}), 201

@api_bp.route('/ratings/<int:rating_id>', methods=['PUT'])
def update_existing_rating(rating_id):
    """
    Update an existing rating with the provided rating ID.

    This function retrieves rating data from the request's JSON payload,
    creates a rating object from the dictionary, and updates the rating
    in the database.

    Args:
        rating_id (int): The ID of the rating to be updated.

    Returns:
        Response: A JSON response containing a message and the updated rating object,
                  along with an HTTP status code 200.
    """
    rating_dict = request.get_json()
    rating = Rating.from_dict(rating_dict)
    rating.rating_id = rating_id
    services.update_rating(rating)
    return jsonify({'message': 'Rating updated', 'rating': rating.to_dict()}), 200

@api_bp.route('/ratings/<int:rating_id>', methods=['DELETE'])
def remove_rating(rating_id):
    """
    Remove a rating by its rating ID.

    This function deletes a rating from the database and returns a JSON response
    indicating that the rating has been deleted.

    Args:
        rating_id (int): The ID of the rating to be removed.

    Returns:
        tuple: A tuple containing a JSON response with a message and an HTTP status code.
    """
    services.delete_rating(rating_id)
    return jsonify({'message': 'Rating deleted'}), 200

@api_bp.route('/ratings/<int:rating_id>', methods=['GET'])
def lookup_rating_by_id(rating_id):
    """
    Retrieve rating information by rating ID.

    Args:
        rating_id (int): The unique identifier of the rating.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            - If the rating is found, returns a JSON object with rating information and status code 200.
            - If the rating is not found, returns a JSON object with an error message and status code 404.
    """
    rating = services.get_rating_by_id(rating_id)
    if rating:
        return jsonify(rating.to_dict()), 200
    return jsonify({'message': 'Rating not found'}), 404