# If you want to write your own tests, but don't necessarily want to learn the pytest framework, you can write your tests in a simple Python script.
# This requires a bit more setup, but can be a good way to get started with testing.
# The first few lines of the script will be used to let Python know where to find your api files

import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now we can import the modules we need
from api.services import get_db_connection, get_all_users

def get_db_connection_test():
    cnn = get_db_connection()
    print (cnn)

def get_all_users_test():
    users = get_all_users()
    for user in users:
        print(user)
    
get_db_connection_test()
get_all_users_test()
    
