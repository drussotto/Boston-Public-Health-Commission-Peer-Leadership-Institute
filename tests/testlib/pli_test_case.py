import mongomock
import testlib
from flask import g
from application import application as pli
from flask_login import current_user, logout_user, login_user
import unittest
# This class should be extended to create a test case for the PLI
# site. It setups up the test db connection for each unit test
# You must implement the mocked_db method so that it retuns
# a mongomock for your database.
class PliTestCase(unittest.TestCase):
    
    def setUp(self):
        db = mongomock.MongoClient().pli

        # This function takes a collection initializing function
        # and a DB and calls the function, returning the DB
        def fold_cols(db, f):
            f(db)
            return db
        
        # We fold the db over the initializers, so we got all the collections
        pli.config['db'] = reduce(fold_cols, self.db_inits(), db)

        self.ctx = pli.app_context()
        self.ctx.push()
        
    def tearDown(self):
        self.ctx.pop()

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

# A convinience test case containing the "mocked users"
# From testlib in the db
class PliUsersTestCase(PliTestCase):
    def db_inits(self):
        return [testlib.add_mocked_users]
    
# A convinience test case containing the "mocked qotd's"
# From testlib in the db
class PliQotdTestCase(PliTestCase):
    def db_inits(self):
        return [testlib.add_mocked_questions]

# A convinience test case containing every mocked collection
# From testlib in the db
class PliEntireDbTestCase(PliTestCase):
    def db_inits(self):
        return testlib.get_db_mock_initializers()
