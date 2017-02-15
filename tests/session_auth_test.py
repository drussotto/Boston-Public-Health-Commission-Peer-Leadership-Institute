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

def check_page(expected_content, *name):
        
    def _check_page(f, d, *msg):
        for s in expected_content:
            f(s in d, *msg)

    def assert_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertTrue, r.data, str(name[0]))
        else:
            _check_page(tr.assertTrue, r.data)
            
    def assert_not_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertFalse, r.data, "Not " + str(name[0]))
        else:
            _check_page(tr.assertFalse, r.data)

    return assert_page, assert_not_page

assert_index_page, assert_not_index_page = check_page(["PLI has answers to all your health-related questions","Index-Page","Choose a category or search below."],"index")
assert_login_page, assert_not_login_page = check_page(["Email Address","Login","Password"], "login")
assert_res_page, assert_not_res_page = check_page(["Resources-Page", "Resources go here ..."], "resources")
    
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
            assert_login_page(self, self.do_login(32, user1["password"]))
            assert_login_page(self, self.do_login(user2["email_address"], user1["password"]))
            assert_login_page(self, self.do_login(43.2, 4))
            assert_login_page(self, self.do_login("{ $gt : \"*\" }", "{ $gt : \"*\" }"))
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"]))
            assert_login_page(self, self.do_login("", ""))
            assert_login_page(self, self.do_login(None, None))

    def test_good_login_post_redirect(self):
        with pli.app_context():
            assert_login_page(self, self.do_login(user1["email_address"], user1["password"], to="login"))
            assert_res_page(self, self.do_login(user2["email_address"], user2["password"], to="resources.html"))
            assert_index_page(self, self.do_login(user3["email_address"], user3["password"]))

    def test_bad_login_post_no_redirect(self):
        with pli.app_context():
            assert_login_page(self, self.do_login(user1["email_address"], user2["password"], to="resources.html"))
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"], to="resources.html"))
            assert_login_page(self, self.do_login(user3["email_address"], user1["password"], to="resources.html"))
            assert_login_page(self, self.do_login(32, user1["password"], to="resources.html"))
            assert_login_page(self, self.do_login(user2["email_address"], user1["password"], to="resources.html"))
            assert_login_page(self, self.do_login(43.2, 4, to="resources.html"))
            assert_login_page(self, self.do_login("{ $gt : \"*\" }", "{ $gt : \"*\" }", to="resources.html"))
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"], to="resources.html"))
            assert_login_page(self, self.do_login("", "", to="resources.html"))
            assert_login_page(self, self.do_login(None, None, to="resources.html"))

    def do_login(self, user, passwd, to=None):

        if to is not None:
            param = "?next=%s" % str(to)
        else:
            param = ""
            
        return self.app.post('/login'+param, data=dict(
            email=user,
            password=passwd
        ), follow_redirects=True)

