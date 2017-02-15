from application import application as pli
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

def check_index_page(f, r):
    f("PLI has answers to all your health-related questions" in r.data)
    f("Index-Page" in r.data)
    f("Choose a category or search below." in r.data)

def assert_index_page(tr, r):
    check_index_page(lambda x: tr.assertTrue(x, "Is index page"), r)
def assert_not_index_page(tr, r):
    check_index_page(lambda x: tr.assertFalse(x, "Not index page"), r)
    
def check_login_page(f, r):
    # I'm satisfied with these deciding this is the login page
    f("Email Address" in r.data)
    f("Login" in r.data)
    f("Password" in r.data)

def assert_login_page(tr, r):
    check_login_page(lambda x: tr.assertTrue(x, "Is login page"), r)

def assert_not_login_page(tr, r):
    check_login_page(tr.assertFalse(x, "Is not login page"), r)

    
class LoginTestCase(unittest.TestCase):

    def setUp(self):
        pli.config['db'] = mocked_users()
        self.app = pli.test_client()

    def test_good_login(self):
        with pli.app_context():
            self.assertEqual(user1["_id"],validate_login(user1["email_address"], user1["password"]))
            self.assertEqual(user2["_id"],validate_login(user2["email_address"], user2["password"]))

    def test_bad_login(self):
        with pli.app_context():
            self.assertEqual(None,validate_login(32, user1["password"]))
            self.assertEqual(None,validate_login(user2["email_address"], user1["password"]))
            self.assertEqual(None,validate_login(user3["email_address"], user1["password"]))
            self.assertEqual(None,validate_login(43.2, 4))
            self.assertEqual(None,validate_login("{ $gt : \"*\" }", "{ $gt : \"*\" }"))
            self.assertEqual(None,validate_login(user2["email_address"], user3["password"]))
            self.assertEqual(None,validate_login("", ""))
            self.assertEqual(None,validate_login(None, None))

    def test_login_page(self):
        with pli.app_context():
            r = self.app.get("/login")
            assert_login_page(self, r)

    def test_good_login_post(self):
        with pli.app_context():
            assert_index_page(self, self.do_login(user1["email_address"], user1["password"]))
            assert_index_page(self, self.do_login(user2["email_address"], user2["password"]))
            assert_index_page(self, self.do_login(user3["email_address"], user3["password"]))

    def test_bad_login_post(self):
        with pli.app_context():
            assert_login_page(self, self.do_login(user1["email_address"], user2["password"]))
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"]))
            assert_login_page(self, self.do_login(user3["email_address"], user1["password"]))

    def do_login(self, user, passwd, to=None):

        if to is not None:
            param = "?next=%s" % str(to)
        else:
            param = ""
            
        return self.app.post('/login'+param, data=dict(
            email=user,
            password=passwd
        ), follow_redirects=True)

