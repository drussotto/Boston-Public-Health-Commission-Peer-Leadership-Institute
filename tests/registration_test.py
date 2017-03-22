from application import mail
from urllib import quote_plus
from testlib import *
from pli import validate_login, encode_uid, decode_uid, is_confirmed_uid
from pli.register import send_confirmation_email

def reg_form_from_user(d):
    return dict(
        first_name=d["first_name"],
        last_name=d["last_name"],
        email=d["email_address"],
        password=d["real_pass"]
    )

    
class RegistrationTest(PliEntireDbTestCase):
    
    @with_test_client
    def test_reg_post1(self, client):
        r = client.get('/register')
        assert_reg_page(self, r)

    @with_test_client
    def test_form_confirmed(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data=reg_form_from_user(user1),
                            follow_redirects=True)
            assert_alr_reg_page(self, r)
            self.assertEqual(0, len(outbox))

    @with_test_client
    def test_form_unconfirmed(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data=reg_form_from_user(user2),
                            follow_redirects=True)
            assert_mail_sent_page(self, r)
            self.assertEqual(1, len(outbox))

    @with_test_client
    def test_form_invalid(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data={},
                            follow_redirects=True)
            assert_reg_page(self, r)
            self.assertEqual(0, len(outbox))

    @with_app_ctxt
    @with_test_client
    def test_new_user(self, client):
        with mail.record_messages() as outbox:
            r = client.post('/register',
                            data=dict(
                                first_name="idontknow",
                                last_name="none",
                                email="email@example.com",
                                password="thisismypassword"),
                            follow_redirects=True)
            assert_mail_sent_page(self, r)
            self.assertNotEqual(None,
                               validate_login("email@example.com",
                                              "thisismypassword"))
            self.assertEqual(1, len(outbox))
        


class ValidationTest(PliEntireDbTestCase):
    
    @with_app_ctxt
    def test_encode_decode_uid(self):
        self.assertEqual(user1["_id"], decode_uid(encode_uid(user1["_id"])))

    @with_app_ctxt
    def test_decode_bad_uid(self):
        self.assertEqual(None, decode_uid("garbage"))

    @with_app_ctxt
    def test_encode_not_same_uid(self):
        self.assertNotEqual(user1["_id"], encode_uid(user1["_id"]))
        self.assertNotEqual(str(user1["_id"]), encode_uid(user1["_id"]))

    @with_app_ctxt
    def test_encode_uid_urlsafe(self):
        # URL encoding tokens should do nothing.
        encoded_id = encode_uid(user1["_id"])
        self.assertEqual(encoded_id, quote_plus(encoded_id))
    

    @with_app_ctxt
    @with_test_client
    def test_valid_token1(self, client):
        r = client.get('/validate?user='+
                       quote_plus(encode_uid(user2["_id"])))
        assert_good_vtok_page(self, r)
        # Call should have "validated" user2
        self.assertTrue(is_confirmed_uid(user2["_id"]))

    @with_app_ctxt
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


