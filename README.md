# Movie Reviews
## Description
This project demonstrates the use of a simple movie review system. The system allows users to add movies and review them. The system also allows users to view the reviews of a movie and the average rating of a movie. The system is implemented using Python and SQLite.

The intent of this project is demonstrate how to deploy an API to an Azure Function App. The API function is implemented using Python and Flask. The API function is deployed to an Azure Function App using the Azure CLI.

## Installation
1. Clone the repository
2. Create virtual environment
```bash
python -m venv venv
```
3. Install the required packages
```bash
pip install -r requirements.txt
```
4. Load the sample data
```bash
python utility/load_data.py
```
## Running the application
```bash
python run.py
```
The api will be accessible at http://localhost:5000

## Features
- Add a movie
- Review a movie
- View reviews of a movie
- View average rating of a movie
- View all movies

## Documentation
There is also an [API Documentation](docs/api_documentation.md) document that describes how to use the API.
A [Data Dictionary](docs/data_dictionary.md) document is also available that describes the fields in the database.
A short description of how the testig is done is available in the [Testing](docs/testing.md) document.

## Sample project structure
Students have said that it is helpful to understand how a project of this type can be structured.  Here is a simple example of how the project could be structured.  This is not the only way to structure the project, but it is a way that has worked for many students in the past.

```
MovieRatings/
│
├── api/
│   ├── __init__.py               # Package initializer for the 'api' directory
│   ├── models.py                 # Database models/classes (e.g. User, Movie, Rating)
│   ├── routes.py                 # API route definitions and request handling
│   └── services.py               # Service functions, handling business logic, and database operations
│
├── data/
│   └── movie_data.db             # SQLite database file 
│
├── docs/
│   ├── api_documentation.md      # Documentation for API usage
|   └── data_dictionary.md        # Data dictionary for the database
│
├── tests/                        # Optional directory for unit tests
│   ├── __init__.py               # Package initializer for 'tests'
│   ├── test_db.py                # Unit tests for database operations
│   ├── test_routes.py            # Unit tests for API routes
│   └── test_services.py          # Unit tests for service layer
│
├── utility/
│   ├── helpers.py                # Utility functions used across the project
│   └── config.py                 # Configuration settings for the application
│
├── .gitignore                    # Specifies files and folders to be ignored by Git
├── LICENSE                       # License information for the project
├── README.md                     # General overview and setup instructions for the project
└── run.py                        # Entry point script to start the Flask application
```

### Recommended Responsibilities for Each File:
`models.py`: This is where you define your data models. Typically, these models represent tables in your database and contain methods related to the database schema, such as relationships and validation. The models are generally only responsible for mapping data and not directly interacting with the database.

`services.py`: This file is responsible for the business logic and database access code. Any code that interacts with the database (like querying, inserting, updating, and deleting records) should go here. This is where you'd put functions like `get_user_by_id()`, `create_user()`, or `update_movie()`. By placing all your database access logic here, you keep it separate from routing and can easily reuse this logic in different parts of your application.

`routes.py`: This file is used to define API routes. The routes should handle HTTP requests (e.g., GET, POST, PUT, DELETE), parse input, and return responses. They should not contain direct database access code. Instead, they should call functions in `services.py` to perform the necessary actions. This keeps the routes lightweight and focused on dealing with request/response operations.

