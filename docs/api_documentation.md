# Movie Review Management API Documentation

This document provides an overview of the endpoints available in the Movie Review Management API, which allows for managing users, movies, and user reviews, including creating, retrieving, updating, and deleting records. All routes are part of the `/api` Blueprint, and they need to be accessed with the `/api` prefix.

## Base URL

```
/api
```

## User API Documentation

## Endpoints

### 1. Home Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: A welcome message for the User API.
- **Response**:
  - `200 OK`: Returns a welcome message.

### 2. Get All Users or Filter Users by Name

- **URL**: `/users`
- **Method**: `GET`
- **Query Parameter**:
  - `starts_with` (optional): Filter users whose names start with the given string.
- **Description**: Retrieves a list of all users or filters users by the given name prefix.
- **Response**:
  - `200 OK`: Returns a JSON array of users.

### 3. Look Up Users by Name

- **URL**: `/users/<string:user_name>`
- **Method**: `GET`
- **Path Parameter**:
  - `user_name` (str): The name of the user to look up.
- **Description**: Looks up users by their name and returns their details in JSON format. The `user_name` can be matched anywhere within the user's name.
- **Response**:
  - `200 OK`: Returns a JSON list of users if found.
  - `404 Not Found`: Returns an error message if no users are found.

### 4. Get User by ID

- **URL**: `/users/<int:user_id>`
- **Method**: `GET`
- **Path Parameter**:
  - `user_id` (int): The unique identifier of the user.
- **Description**: Retrieves user information by user ID.
- **Response**:
  - `200 OK`: Returns a JSON object with user information.
  - `404 Not Found`: Returns an error message if the user is not found.

### 5. Add a New User

- **URL**: `/users`
- **Method**: `POST`
- **Request Body** (JSON):
  ```json
  {
    "username": "new_user",
    "email": "new_user@example.com"
  }
  ```
- **Description**: Adds a new user to the system.
- **Response**:
  - `201 Created`: Returns a JSON response containing a success message and the added user.

### 6. Update an Existing User

- **URL**: `/users/<int:user_id>`
- **Method**: `PUT`
- **Path Parameter**:
  - `user_id` (int): The ID of the user to be updated.
- **Request Body** (JSON):
  ```json
  {
    "username": "updated_user",
    "email": "updated_user@example.com"
  }
  ```
- **Description**: Updates an existing user with the provided user ID.
- **Response**:
  - `200 OK`: Returns a JSON response containing a success message and the updated user.

### 7. Delete a User

- **URL**: `/users/<int:user_id>`
- **Method**: `DELETE`
- **Path Parameter**:
  - `user_id` (int): The ID of the user to be removed.
- **Description**: Removes a user by their user ID.
- **Response**:
  - `200 OK`: Returns a JSON response indicating the user has been deleted.

## Movie API Documentation

### 1. Get All Movies

- **URL**: `/movies`
- **Method**: `GET`
- **Description**: Retrieves a list of all movies.
- **Response**:
  - `200 OK`: Returns a JSON array of movies.

### 2. Get Movie by ID

- **URL**: `/movies/<int:movie_id>`
- **Method**: `GET`
- **Path Parameter**:
  - `movie_id` (int): The unique identifier of the movie.
- **Description**: Retrieves movie information by movie ID.
- **Response**:
  - `200 OK`: Returns a JSON object with movie information.
  - `404 Not Found`: Returns an error message if the movie is not found.

### 3. Add a New Movie

- **URL**: `/movies`
- **Method**: `POST`
- **Request Body** (JSON):
  ```json
  {
    "title": "new_movie",
    "director": "director_name",
    "release_year": 2023
  }
  ```
- **Description**: Adds a new movie to the system.
- **Response**:
  - `201 Created`: Returns a JSON response containing a success message and the added movie.

### 4. Update an Existing Movie

- **URL**: `/movies/<int:movie_id>`
- **Method**: `PUT`
- **Path Parameter**:
  - `movie_id` (int): The ID of the movie to be updated.
- **Request Body** (JSON):
  ```json
  {
    "title": "updated_movie",
    "director": "updated_director",
    "release_year": 2024
  }
  ```
- **Description**: Updates an existing movie with the provided movie ID.
- **Response**:
  - `200 OK`: Returns a JSON response containing a success message and the updated movie.

### 5. Delete a Movie

- **URL**: `/movies/<int:movie_id>`
- **Method**: `DELETE`
- **Path Parameter**:
  - `movie_id` (int): The ID of the movie to be removed.
- **Description**: Removes a movie by its movie ID.
- **Response**:
  - `200 OK`: Returns a JSON response indicating the movie has been deleted.

## Ratings API Documentation

### 1. Get All Ratings

- **URL**: `/ratings`
- **Method**: `GET`
- **Description**: Retrieves a list of all ratings.
- **Response**:
  - `200 OK`: Returns a JSON array of ratings.

### 2. Get Rating by ID

- **URL**: `/ratings/<int:rating_id>`
- **Method**: `GET`
- **Path Parameter**:
  - `rating_id` (int): The unique identifier of the rating.
- **Description**: Retrieves rating information by rating ID.
- **Response**:
  - `200 OK`: Returns a JSON object with rating information.
  - `404 Not Found`: Returns an error message if the rating is not found.

### 3. Add a New Rating

- **URL**: `/ratings`
- **Method**: `POST`
- **Request Body** (JSON):
  ```json
  {
    "user_id": 1,
    "movie_id": 2,
    "rating": 4.5
  }
  ```
- **Description**: Adds a new rating to the system.
- **Response**:
  - `201 Created`: Returns a JSON response containing a success message and the added rating.

### 4. Update an Existing Rating

- **URL**: `/ratings/<int:rating_id>`
- **Method**: `PUT`
- **Path Parameter**:
  - `rating_id` (int): The ID of the rating to be updated.
- **Request Body** (JSON):
  ```json
  {
    "user_id": 1,
    "movie_id": 2,
    "rating": 4.0
  }
  ```
- **Description**: Updates an existing rating with the provided rating ID.
- **Response**:
  - `200 OK`: Returns a JSON response containing a success message and the updated rating.

### 5. Delete a Rating

- **URL**: `/ratings/<int:rating_id>`
- **Method**: `DELETE`
- **Path Parameter**:
  - `rating_id` (int): The ID of the rating to be removed.
- **Description**: Removes a rating by its rating ID.
- **Response**:
  - `200 OK`: Returns a JSON response indicating the rating has been deleted.