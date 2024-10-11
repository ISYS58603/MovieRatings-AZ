# Advanced Concepts
There are a few advanced concepts that you may want to consider when building your project.  These are not required, but they can help you to build a more robust and maintainable application.
I've tried to keep the project structure as simple as possible and there is plenty that you can avoid doing.  However, if you are interested in learning more about how to build a more complex application, here are a few ideas to get you started.

## Unit Testing
There is a whole description of how this works in the [Testing](docs/testing.md) document.  But in short, unit testing is a way to verify that your code is working as expected.  It is a good practice to write tests for your code as you build it.  This helps to ensure that you are not breaking existing functionality as you add new features.  It also helps to ensure that your code is robust and can handle a variety of inputs and conditions.

I've written unit tests here as a way to automate the testing process.  This is especially helpful as the project grows and it becomes more difficult to manually test all the functionality.  The tests are written using the `pytest` framework, which is a popular testing framework in Python.  You can run the tests by running the `pytest` command in the project's root directory.

## Decorators
Decorators are a powerful feature in Python that allow you to modify the behavior of functions or methods.  They are used extensively in Flask to define routes and to add functionality to routes.  For instance, you can use decorators to add authentication to a route, to log information about a request, or to handle errors.  Decorators are a great way to separate concerns in your code and to make it more modular and maintainable.  You can learn more about decorators in the [Python documentation](https://docs.python.org/3/library/functions.html#decorator-syntax) or in this [Real Python article](https://realpython.com/primer-on-python-decorators/).

### @classmethod
The `@classmethod` decorator tells Python that a method is a class method rather than an instance method.  This means that the method is bound to the class rather than the instance of the class.  Class methods can be called without creating an instance of the class.  This is useful when you want to create a method that operates on the class itself rather than on an instance of the class.  You can learn more about class methods in the [Python documentation](https://docs.python.org/3/library/functions.html#classmethod).

The biggest use case in our project is for creating new instances of objects from existing representations.  In other words, rather than use the initializer `__init__` method, we can use a class method to create new instances of objects.  This is useful when you want to create an object from a different representation, like a dictionary or a string.