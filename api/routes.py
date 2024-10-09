from flask import jsonify, request, Flask
from services import get_all_users, get_user_by_id, get_users_by_name, create_user, update_user, delete_user
from models import User, create_user_from_dict


app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the User API!'

@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve a list of all users or filter users by name.

    Returns:
        tuple: A tuple containing a JSON response with all users and an HTTP status code 200.
    """
    user_name = request.args.get("user_name")  # Accessing query string parameter
    if not user_name:
        user_list = get_all_users()
    else:
        user_list = get_users_by_name(user_name)
        
    user_dict_list = [user.to_dict() for user in user_list]
    return (jsonify(user_dict_list), 200)

@app.route('/users/<int:user_id>', methods=['GET'])
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
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users/<string:user_name>', methods=['GET'])
def lookup_user_by_name(user_name):
    """
    Look up users by their name and return their details in JSON format.

    Args:
        user_name (str): The name of the user to look up.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            - If users are found, returns a JSON list of users and a 200 status code.
            - If no users are found, returns a JSON message indicating the user was not found and a 404 status code.
    """
    users = get_users_by_name(user_name)
    if users:
        user_dict_list = [user.to_dict() for user in users]
        return jsonify(users), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def add_new_user():
    """
    Adds a new user to the system.

    This function retrieves user data from a JSON request, creates a new User object,
    and adds it to the system using the create_user function.

    Returns:
        Response: A JSON response containing a success message and the added user,
                  with a status code of 201 (Created).
    """
    new_user_dict = request.get_json()
    # We can also use the create_user_from_dict function to create a User object
    new_user = User(new_user_dict['id'], new_user_dict['user_name'], new_user_dict['email'])
    create_user(new_user)
    return jsonify({'message': 'User added', 'user': new_user}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
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
    user = create_user_from_dict(user_dict)
    update_user(user_id, user)
    return jsonify({'message': 'User updated', 'user': user}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
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
    delete_user(user_id)
    return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
