import inspect
from application import application as pli
from flask_login import current_user, logout_user, login_user
import mongomock
from pli import validate_login, PliUser
import unittest
pli.testing = True

# Note that the "real_pass" field for these won't be present in the actual db
# just there for convinience during testing.
user1 = {
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
    "real_pass":"iamsecret",
    "password": 'pbkdf2:sha1:1000$FmjdX5b2$c23a5cefc39cc669f3e193670c3c122041266f26',
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
    "real_pass":"youcantseeme",
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
    "real_pass":"passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "Eve",
    "last_name": "Fakename",
    "organization": None
}

users = [user1,user2,user3]

def mocked_users():
    db = mongomock.MongoClient().pli
    db.users.insert_many(users)
    return db

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
assert_res_page, assert_not_res_page = check_page(["Resources-Page"], "resources")
assert_surv_page, assert_not_surv_page = check_page(["Survey-Page"], "surveys")

def get_u(uid):
    return PliUser(uid, False)

def with_login(username, passwd, to=None):
    def decorator(f):
        def actual_function(s, client):
            n = ("?next="+to) if to is not None else ""
            r = client.post('/login'+n, data=dict(
                email=username, 
                password=passwd
            ), follow_redirects=True)
            p_len = len(inspect.getargspec(f).args)
            if p_len == 1:
                f(s)
            elif p_len == 2:
                f(s, client)
            elif p_len == 3:
                f(s, client, r)
            else:
                # TODO
                pass
        return actual_function
    return decorator

def with_req_ctxt(f):
    def run_test(s):
        with pli.test_client() as client:
            f(s, client)
    return run_test

def with_app_ctxt(f):
    def run_test(s):
        with pli.app_context():
            f(s)
    return run_test

class LoginTestCase(unittest.TestCase):
    def assert_logged_in(self):
        self.assertTrue(current_user.is_authenticated,
                        "Not logged in, but should be")
    
    def assert_not_logged_in(self):
        try:
            self.assertFalse(current_user.is_authenticated,
                             "Logged in, but should not be")
        except AttributeError:
            # If we get an attribute error, we are not in request context
            # and therefore could not be logged in
            pass

    def assert_cur_uid(self, uid):
        self.assertTrue(current_user.same_uid(uid))
        
    def setUp(self):
        pli.config['db'] = mocked_users()
        self.app = pli.test_client()

    @with_app_ctxt
    def test_good_login(self):
        # validate_login shouldn't log anyone in.
        self.assertEqual(user1["_id"],validate_login(user1["email_address"], user1["real_pass"]))
        self.assert_not_logged_in()
        self.assertEqual(user2["_id"],validate_login(user2["email_address"], user2["real_pass"]))
        self.assert_not_logged_in()


    @with_req_ctxt
    @with_login(32, user1["real_pass"])
    def test_bad_login1(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(43.2, 4)
    def test_bad_login2(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login("{ $gt : \"*\" }", "{ $gt : \"*\" }")
    def test_bad_login3(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login("", "")
    def test_bad_login4(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(None, None)
    def test_bad_logi5(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_app_ctxt
    def test_login_page(self):
        r = self.app.get("/login")
        assert_login_page(self, r)

    @with_req_ctxt
    @with_login(user1["email_address"], user1["real_pass"])
    def test_good_login_post1(self, client):
        self.assert_logged_in()
        self.assert_cur_uid(get_u(user1["_id"]))
        

    @with_req_ctxt
    @with_login(user2["email_address"], user2["real_pass"])
    def test_good_login_post2(self, client):
        self.assert_logged_in()
        self.assert_cur_uid(get_u(user2["_id"]))

    @with_req_ctxt
    @with_login(user3["email_address"], user3["real_pass"])
    def test_good_login_post3(self, client, res):
        self.assert_logged_in()
        self.assert_cur_uid(get_u(user3["_id"]))
        assert_index_page(self, res)

    @with_req_ctxt
    @with_login(user3["email_address"], user2["real_pass"])
    def test_failed_log_in(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(user1["email_address"], user1["real_pass"], to="resources")
    def test_good_login_post_red1(self, client, res):
        self.assert_logged_in()
        assert_res_page(self, res)

    @with_req_ctxt
    @with_login(user2["email_address"], user2["real_pass"], to="surveys")
    def test_good_login_post_redirect1(self, client, res):
        self.assert_logged_in()
        self.assert_cur_uid(get_u(user2["_id"]))
        assert_surv_page(self, res)

    @with_req_ctxt
    @with_login(user1["email_address"], user2["real_pass"], to="resources")
    def test_bad_login_redirect1(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(user2["email_address"], user3["real_pass"], to="resources")
    def test_bad_login_redirect2(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(32, user1["real_pass"],to="resources")
    def test_bad_login_redirect3(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login("", "",to="resources")
    def test_bad_login_redirect4(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(None, None, to="resources")
    def test_bad_login_redirect5(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login("{ $gt : \"*\" }", "{ $gt : \"*\" }", to="resources")
    def test_bad_login_redirect6(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)
