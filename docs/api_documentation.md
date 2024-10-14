# User and Movie API Documentation

This document provides an overview of the API routes for managing users and movies. These routes are part of a RESTful API that allows creating, updating, deleting, and retrieving information about users and movies.

## Base URL
The base URL for all the routes is `/api`.

## API Endpoints

### 1. Home Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Displays a welcome message for the API.
- **Response**:
  - **200 OK**: Returns a plain text message: "Welcome to the User API!"

### 2. Test Connection Endpoint
- **URL**: `/api/connection`
- **Method**: `GET`
- **Description**: Tests the connection to the API.
- **Response**:
  - **200 OK**: Returns a JSON message indicating a successful connection: `{"message": "Successfully connected to the API"}`

### 3. User Routes

#### Get All Users
- **URL**: `/api/users`
- **Method**: `GET`
- **Description**: Retrieve all users or filter users by name using query parameters.
- **Query Parameters**:
  - `starts_with` (optional): Filter users whose names start with this string.
  - `contains` (optional): Filter users whose names contain this string.
- **Response**:
  - **200 OK**: Returns a list of users.

#### Get User by ID
- **URL**: `/api/users/{user_id}`
- **Method**: `GET`
- **Description**: Retrieve a user by their unique ID.
- **Path Parameter**:
  - `user_id` (required): The ID of the user to retrieve.
- **Response**:
  - **200 OK**: Returns user details.
  - **404 Not Found**: User not found.

#### Add New User
- **URL**: `/api/users`
- **Method**: `POST`
- **Description**: Add a new user to the system.
- **Request Body**:
  ```json
  {
    "username": "new_user",
    "email": "new_user@example.com"
  }
  ```
- **Response**:
  - **201 Created**: Returns a message and details of the newly created user.

#### Update Existing User
- **URL**: `/api/users/{user_id}`
- **Method**: `PUT`
- **Description**: Update an existing user.
- **Path Parameter**:
  - `user_id` (required): The ID of the user to update.
- **Request Body**:
  ```json
  {
    "username": "updated_user",
    "email": "updated_user@example.com"
  }
  ```
- **Response**:
  - **200 OK**: Returns a message and updated user details.

#### Delete User
- **URL**: `/api/users/{user_id}`
- **Method**: `DELETE`
- **Description**: Delete a user by their ID.
- **Path Parameter**:
  - `user_id` (required): The ID of the user to delete.
- **Response**:
  - **200 OK**: Returns a message indicating the user was deleted.

### 4. Movie Routes

#### Get All Movies
- **URL**: `/api/movies`
- **Method**: `GET`
- **Description**: Retrieve all movies or filter movies by title.
- **Query Parameter**:
  - `title` (optional): Filter movies by title.
- **Response**:
  - **200 OK**: Returns a list of movies.

#### Get Movie by ID
- **URL**: `/api/movies/{movie_id}`
- **Method**: `GET`
- **Description**: Retrieve a movie by its unique ID.
- **Path Parameter**:
  - `movie_id` (required): The ID of the movie to retrieve.
- **Response**:
  - **200 OK**: Returns movie details.
  - **404 Not Found**: Movie not found.

#### Add New Movie
- **URL**: `/api/movies`
- **Method**: `POST`
- **Description**: Add a new movie to the system.
- **Request Body**:
  ```json
  {
    "title": "Inception",
    "genre": "Sci-Fi",
    "release_year": 2010,
    "director": "Christopher Nolan"
  }
  ```
- **Response**:
  - **201 Created**: Returns a message and details of the newly created movie.

#### Update Existing Movie
- **URL**: `/api/movies/{movie_id}`
- **Method**: `PUT`
- **Description**: Update an existing movie.
- **Path Parameter**:
  - `movie_id` (required): The ID of the movie to update.
- **Request Body**:
  ```json
  {
    "title": "Updated Movie Title",
    "genre": "Updated Genre",
    "release_year": 2024,
    "director": "Updated Director"
  }
  ```
- **Response**:
  - **200 OK**: Returns a message and updated movie details.

#### Delete Movie
- **URL**: `/api/movies/{movie_id}`
- **Method**: `DELETE`
- **Description**: Delete a movie by its ID.
- **Path Parameter**:
  - `movie_id` (required): The ID of the movie to delete.
- **Response**:
  - **200 OK**: Returns a message indicating the movie was deleted.

## Swagger UI Documentation

The API is documented using **Swagger UI**, which provides an interactive user interface to explore and test the API endpoints.

### Accessing Swagger UI
- **URL**: `http://localhost:5000/apidocs/`
- **Description**: Swagger UI provides a visual representation of the API routes, allowing you to send test requests and view the responses directly from the browser.

### Steps to Access Swagger UI
1. **Run the Flask application**: Start your server by running the `run.py` file:
   ```sh
   python run.py
   ```
2. **Open your browser**: Navigate to `http://localhost:5000/apidocs/` to see the Swagger UI.
3. **Interact with the API**: You can view all available endpoints, see the required parameters, and send requests to test each endpoint.

