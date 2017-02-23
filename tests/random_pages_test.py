from testlib import *
from application import application as pli
from flask_login import current_user, logout_user, login_user
import unittest


class TestRemainingPages(unittest.TestCase):

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

    
    @with_req_ctxt
    @with_login(user1["email_address"], user1["real_pass"])
    def test_hello(self, client, res):
        assert_index_page(self, res)
        self.assert_logged_in()
        self.assertEquals("hello", client.get("/hello", follow_redirects=True).data)

    @with_req_ctxt
    @with_login(user2["email_address"], user1["real_pass"])
    def test_hello2(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, client.get("/hello", follow_redirects=True))

    
