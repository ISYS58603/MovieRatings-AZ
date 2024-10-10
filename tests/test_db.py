import unittest
import api.services as services
from api.models import User, Rating, Movie  

class TestDB(unittest.TestCase):
    def test_create_connection(self):
        conn = services.get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def setUp(self) -> None:
        return super().setUp()

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

    def test_create_user(self):
        new_user = User(None, "test_user", "testuser@example.com")
        new_user.id = services.create_user(new_user)
        self.assertIsNotNone(new_user.id)
        # Now get the user back and check that it is the same
        user = services.get_user_by_id(new_user.id)
        self.assertEqual(user.user_name, new_user.user_name)
        self.assertEqual(user.email, new_user.email)
        services.delete_user(new_user.id)
        
    # # Test to create a user
    # print("Create a user")
    # print("-----------")
    #
    # create_user(new_user)
    # added_user = get_users_by_name('test_user')[0]
    # print(added_user)

    # # Test to update a user
    # print("Update a user")
    # print("-----------")
    # # Start by getting the user to update
    # user_to_update = get_users_by_name('test_user')[0]
    # print(user_to_update)
    # # Update the user
    # user_to_update.user_name = 'updated_user'
    # update_user(user_to_update)
    # # Get the user again to see the changes
    # updated_user = get_user_by_id(user_to_update.id)
    # print(updated_user)

    # # # Test to remove a user
    # print('Now delete the user')
    # print("-----------")
    # # Start by getting the last user put into the database
    # last_user = get_all_users()[-1]
    # delete_user(last_user.id)
    # print(get_users_by_name(last_user.user_name))

if __name__ == '__main__':
    unittest.main()
