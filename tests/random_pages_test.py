from testlib import *
from application import application as pli
from flask_login import current_user, logout_user, login_user
import unittest

class TestRemainingPages(PliTestCase):

    def mocked_db(self):
        return mocked_users()
        
    @with_login(user1["email_address"], user1["real_pass"])
    def test_hello(self, client, res):
        assert_index_page(self, res)
        self.assert_logged_in()
        self.assertEquals("hello", client.get("/hello", follow_redirects=True).data)

    @with_login(user2["email_address"], user1["real_pass"])
    def test_hello2(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, client.get("/hello", follow_redirects=True))

    
