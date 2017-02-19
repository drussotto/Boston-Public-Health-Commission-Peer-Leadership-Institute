from application import application as pli
from flask_login import current_user, logout_user
import mongomock
from pli import validate_login, PliUser
import unittest
pli.testing = True
user1 = {
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
    "password": "pbkdf2:sha1:1000$cGAZqve1$9b311ca4d8e6d59733f859345c620c431420844c",
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
    "password": "pbkdf2:sha1:1000$HDOj8diN$62524eb1619b6ee167aeb1d6116ad6075a5bf3cb",
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
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
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


def get_u(uid):
    return PliUser(uid, False)
    
class LoginTestCase(unittest.TestCase):
    def assert_logged_in(self):
        self.assertTrue(current_user.is_authenticated(),
                        "Not logged in, but should be")
    
    def assert_not_logged_in(self):
        self.assertFalse(current_user.is_authenticated(),
                         "Logged in, but should not be")

    def setUp(self):
        pli.config['db'] = mocked_users()
        self.app = pli.test_client()

    def assert_lin_cur_user(self, other):
        self.assert_logged_in()
        self.assertEqual(current_user.same_uid(other))

    def test_good_login(self):
        with pli.app_context():
            # validate_login shouldn't log anyone in.
            self.assertEqual(user1["_id"],validate_login(user1["email_address"], user1["password"]))
            self.assert_not_logged_in()
            self.assertEqual(user2["_id"],validate_login(user2["email_address"], user2["password"]))
            self.assert_not_logged_in()

    def test_bad_login(self):
        with pli.app_context():
            # validate_login shouldn't log anyone in.
            self.assertEqual(None,validate_login(32, user1["password"]))
            self.assert_not_logged_in()
            self.assertEqual(None,validate_login(user2["email_address"], user1["password"]))
            self.assert_not_logged_in()
            self.assertEqual(None,validate_login(user3["email_address"], user1["password"]))
            self.assert_not_logged_in()
            self.assertEqual(None,validate_login(43.2, 4))
            self.assert_not_logged_in()
            self.assertEqual(None,validate_login("{ $gt : \"*\" }", "{ $gt : \"*\" }"))
            self.assert_not_logged_in()
            self.assertEqual(None,validate_login(user2["email_address"], user3["password"]))
            self.assert_not_logged_in()
            self.assertEqual(None,validate_login("", ""))
            self.assert_not_logged_in()
            self.assertEqual(None,validate_login(None, None))
            self.assert_not_logged_in()

    def test_login_page(self):
        with pli.app_context():
            r = self.app.get("/login")
            assert_login_page(self, r)

    def test_good_login_post(self):
        with pli.app_context():

            assert_index_page(self, self.do_login(user1["email_address"], user1["password"]))
            self.assert_lin_cur_user(get_u(user1["_id"]))
            logout_user()

            assert_index_page(self, self.do_login(user2["email_address"], user2["password"]))
            self.assert_lin_cur_user(get_u(user2["_id"]))
            logout_user()

            assert_index_page(self, self.do_login(user3["email_address"], user3["password"]))
            self.assert_lin_cur_user(get_u(user3["_id"]))
            logout_user()

    def test_bad_login_post(self):
        with pli.app_context():
            assert_login_page(self, self.do_login(user1["email_address"], user2["password"]));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"]));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user3["email_address"], user1["password"]));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(32, user1["password"]));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user2["email_address"], user1["password"]));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(43.2, 4));self.assert_not_logged_in()
            assert_login_page(self, self.do_login("{ $gt : \"*\" }", "{ $gt : \"*\" }"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"]));self.assert_not_logged_in()
            assert_login_page(self, self.do_login("", ""));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(None, None));self.assert_not_logged_in()

    def test_good_login_post_redirect(self):
        with pli.app_context():

            assert_login_page(self, self.do_login(user1["email_address"], user1["password"], to="login"))
            self.assert_lin_cur_user(get_u(user1["_id"]))
            logout_user()

            assert_res_page(self, self.do_login(user2["email_address"], user2["password"], to="resources.html"))
            self.assert_lin_cur_user(get_u(user2["_id"]))
            logout_user()

            assert_index_page(self, self.do_login(user3["email_address"], user3["password"]))
            self.assert_lin_cur_user(get_u(user3["_id"]))
            logout_user()


    def test_bad_login_post_no_redirect(self):
        with pli.test_request_context:
            assert_login_page(self, self.do_login(user1["email_address"], user2["password"], to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"], to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user3["email_address"], user1["password"], to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(32, user1["password"], to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user2["email_address"], user1["password"], to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(43.2, 4, to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login("{ $gt : \"*\" }", "{ $gt : \"*\" }", to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(user2["email_address"], user3["password"], to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login("", "", to="resources.html"));self.assert_not_logged_in()
            assert_login_page(self, self.do_login(None, None, to="resources.html"));self.assert_not_logged_in()

    def do_login(self, user, passwd, to=None):

        if to is not None:
            param = "?next=%s" % str(to)
        else:
            param = ""
            
        return self.app.post('/login'+param, data=dict(
            email=user,
            password=passwd
        ), follow_redirects=True)

