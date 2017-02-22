from application import application as pli, mail
from testlib import *
from pli import validate_login
import unittest

def reg_form_from_user(d):
    return dict(
        first_name=d["first_name"],
        last_name=d["last_name"],
        email=d["email_address"],
        password=d["real_pass"]
    )

    
class RegistrationTest(unittest.TestCase):
    def setUp(self):
        pli.config['db'] = mocked_users()
        
    @with_test_client
    def test_reg_post1(self, client):
        r = client.get('/register')
        assert_reg_page(self, r)

    @with_test_client
    def test_form_confirmed(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data=reg_form_from_user(user1))
            assert_alr_reg_page(self, r)
            self.assertEqual(0, len(outbox))

    @with_test_client
    def test_form_unconfirmed(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data=reg_form_from_user(user2))
            assert_mail_sent_page(self, r)
            self.assertEqual(1, len(outbox))

    @with_test_client
    def test_form_invalid(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data={})
            assert_reg_page(self, r)
            self.assertEqual(0, len(outbox))

    @with_req_ctxt
    def test_new_user(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data=dict(
                                first_name="idontknow",
                                last_name="none",
                                email="email@example.com",
                                password="thisismypassword"))
            assert_mail_sent_page(self, r)
            self.assertUnequal(None,
                               validate_login("email@example.com",
                                              "thisismypassword"))
            self.assertEqual(1, len(outbox))
        
