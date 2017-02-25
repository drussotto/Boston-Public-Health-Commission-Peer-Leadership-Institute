import testlib
from application import application as pli
from flask_login import current_user, logout_user, login_user
import unittest

class PliTestCase(unittest.TestCase):
    
    def setUp(self):
        pli.config['db'] = self.mocked_db()
        self.app = pli.test_client()

    def mocked_db(self):
        raise NotImplementedError("You must implement mocked_db to return a mongomock database")

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


class PliUsersTestCase(PliTestCase):
    def mocked_db(self):
        return testlib.mocked_users()

class PliQotdTestCase(PliTestCase):
    def mocked_db(self):
        return testlib.mocked_questions()
