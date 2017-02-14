from application import application as app
import mongomock
from pli import validate_login
import unittest
user1 = {
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
    "password": "iamasecret",
    "first_name": "Bob",
    "last_name": "Smith",
    "organization": {
        "name": "Boston Latin",
        "type": "School",
        "region": "Dorchester"
    }
}
user2 = {
    "_id": 23456,
    "email_address": "iloveindoortennis@gmail.com",
    "password": "youcantseeme",
    "first_name": "Alice",
    "last_name": "Da Example",
    "organization": {
    "name": "Squashbusters",
        "type": "Community Organization",
        "region": "Roxbury"
    }
}
user3 = {
    "_id": 34567,
    "email_address": "iamastudent@someschool.org",
    "password": "passw0rd",
    "first_name": "Eve",
    "last_name": "Fakename",
    "organization": None
}
users = [user1,user2,user3]
def mocked_users():
    collection = mongomock.MongoClient().db.collection
    collection.insert_many(users)
    return collection

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config['db'] = mocked_users()
        self.app = app.test_client()

    def test_good_login(self):
        with app.app_context():
            self.assertEqual(user1["_id"],
                             validate_login(user1["email_address"], user1["password"]))
    def test_bad_login(self):
        with app.app_context():
            self.assertEqual(user1["_id"],
                             validate_login(user2["email_address"], user1["password"]))
