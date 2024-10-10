from flask import Flask
from api.routes import api_bp


# Using Blueprints to organize routes in a Flask application
# https://flask.palletsprojects.com/en/2.0.x/blueprints/
# We are using Blueprints to organize our routes in our Flask application.  This 
#  allows us to separate the routes into different files, which can help keep our
#  code organized and easier to maintain.  In this case, we have a single blueprint
#  that is defined in the api/routes.py file.  We import that blueprint here and
#  register it with our Flask application.  The blueprint is registered with a
#  prefix of "/api", which means that all routes defined in the blueprint will
#  be prefixed with "/api".  For example, a route defined in the blueprint as
#  "/users" will be accessible at "/api/users" in the application.

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    # Don't like the prefix?  You can remove it or change it to something else.
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
