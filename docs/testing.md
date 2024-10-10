# Testing our code
## Introduction
Testing is an important part of software development. It helps us to ensure that our code is working as expected and that we haven't introduced any bugs. The Movie Ratings project includes a set of unit tests that can be run to verify the correctness of the code. Unit tests are small, focused tests that verify the behavior of individual components of the code. For instance, we have unit tests for the database operations, API routes, and service functions in the project.  This helps to ensure as we build out the project that we are not breaking existing functionality.

## Running the tests
To run the tests, you can use the following command in the project's root directory:
```bash
pytest
```
This will run all the tests in the `tests` directory and display the results in the terminal.

## Writing new tests
If you want to write new tests for the project, you can create a new Python file in the `tests` directory and write your test cases using the `pytest` framework. You can refer to the existing test files in the project for examples on how to write tests for the database operations, API routes, and service functions.  The tests are written in a way that they can be run independently of each other.  This is important as it allows us to run the tests in any order and to run only the tests that we are interested in at any given time.

Note when writting tests:
- It is important to test both the expected behavior and the edge cases.  This will help to ensure that the code is robust and that it can handle a variety of inputs and conditions.  So if you are testing a function that takes a list as input, you should test it with an empty list, a list with one element, and a list with multiple elements.  Or if you are testing a function that should react differently if a value is None, you should test it with None as an input.
- It is also important to test for exceptions.  If a function is expected to raise an exception in certain conditions, you should write a test case to verify that the exception is raised.
- If you are testing a function that interacts with the database, it's a good practice to put the database back the way you found it when the test started.  You'll see in the tests that are already there, that we create new users, movies, and ratings, and then we delete them at the end of the test.  This is important because it ensures that the tests are independent of each other and that they don't interfere with each other.
  - There are other more robust ways to handle this, but for now, this is a good practice to follow.  If you get ambitious you can look into **mocking** the database, which is a way to simulate the database without actually interacting with it.
- Testing for performance is also important.  If you have a function that is expected to run in a certain amount of time, you should write a test case to verify that it does.  This is especially important for functions that are expected to run in real-time, like API routes.