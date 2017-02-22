from application import application as pli, mail
from urllib import quote_plus
from testlib import *
from pli import validate_login, encode_uid
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
        


class ValidationTest(unittest.TestCase):

    def setUp(self):
        pli.config['db'] = mocked_users()

        
    @with_test_client
    def test_valid_token1(self, client):
        r = client.get('/validate?user='+
                       quote_plus(encode_uid(user2["_id"])))
        assert_good_vtok_page(self, r)
        # Call should have "validated" user2
        self.assertTrue(pli.is_confirmed_uid(user2["_id"]))

    @with_test_client
    def test_invalid_token1(self, client):
        r = client.get('/validate?user='+
                       quote_plus(encode_uid(0)))

        assert_bad_vtok_page(self, r)

    @with_test_client
    def test_invalid_token2(self, client):
        r = client.get('/validate?user=garbage')
        assert_bad_vtok_page(self, r)

    @with_test_client
    def test_invalid_token3(self, client):
        r = client.get('/validate?user=5')
        assert_bad_vtok_page(self, r)

    @with_test_client
    def test_invalid_token4(self, client):
        r = client.get('/validate')
        assert_bad_vtok_page(self, r)

    @with_test_client
    def test_invalid_token5(self, client):
        r = client.get('/validate?user=5.73')
        assert_bad_vtok_page(self, r)

    @with_test_client
    def test_invalid_token6(self, client):
        r = client.get('/validate?user=\"')
        assert_bad_vtok_page(self, r)

    @with_test_client
    def test_invalid_token7(self, client):
        r = client.get('/validate?user=True')
        assert_bad_vtok_page(self, r)


