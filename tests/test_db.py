import unittest
import api.services as services
from api.models import User, Rating, Movie  

class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_create_connection(self):
        conn = services.get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()

class TestUserDB(unittest.TestCase):

    def test_get_all_users(self):
        all_users = services.get_all_users()
        self.assertGreater(len(all_users), 0)

    def test_get_user_by_id(self):
        user = services.get_user_by_id(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.user_name, "jane_doe")

    def test_get_users_by_starts_with_name(self):
        users = services.get_users_by_name("jane")
        self.assertGreater(len(users), 0)
        for user in users:
            self.assertTrue("jane" in user.user_name.lower())
        # Now test for the opposite case, where we shouldn't get the user back
        users = services.get_users_by_name("wilson")
        self.assertEqual(len(users), 0)

    def test_get_users_by_contains_name(self):
        users = services.get_users_by_name("jane",starts_with=False)
        self.assertGreater(len(users), 0)
        for user in users:
            self.assertTrue("jane" in user.user_name.lower())
        # Now test for a user where just a part of the name is in the user_name
        users = services.get_users_by_name("wilson", starts_with=False)
        self.assertGreater(len(users), 0)
        for user in users:
            self.assertTrue("wilson" in user.user_name.lower())

    def setup_known_user(self) -> User:
        # Create a known user for testing purposes
        known_user = User(None, "known_user", "knownuser@example.com")
        known_user.id = services.create_user(known_user)
        return known_user

    def teardown_known_user(self, user_id):
        # Delete the known user after the test
        services.delete_user(user_id)

    def test_create_user(self):
        new_user = User(None, "test_user", "testuser@example.com")
        new_user.id = services.create_user(new_user)
        self.assertIsNotNone(new_user.id)
        # Now get the user back and check that it is the same
        user = services.get_user_by_id(new_user.id)
        self.assertEqual(user.user_name, new_user.user_name)
        self.assertEqual(user.email, new_user.email)
        services.delete_user(new_user.id)

    def test_update_user(self):
        # Create a new user
        known_user = self.setup_known_user()

        # Update the user
        known_user.user_name = "updated_user"
        services.update_user(known_user)
        updated_user = services.get_user_by_id(known_user.id)
        self.assertEqual(updated_user.user_name, "updated_user")

        # Delete the user
        self.teardown_known_user(known_user.id)
    
    def test_delete_user(self):
        # Create a new user
        known_user = self.setup_known_user()

        # Delete the user
        services.delete_user(known_user.id)
        deleted_user = services.get_user_by_id(known_user.id)
        self.assertIsNone(deleted_user)

    
if __name__ == '__main__':
    unittest.main()
