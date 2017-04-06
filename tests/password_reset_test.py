from testlib import *
from datetime import datetime
import pli

class TestPasswordReset(PliEntireDbTestCase):
    def try_relog(self, client, user, passwd):
        self.assertEqual(200, client.get('/logout').status_code)
        # Try logging in with the new password
        return post_login(client, username, passwd)

    def change_pass_to(self, client, token, new_pass, expect_email_count=1):
        with pli.get_mail().record_messages() as outbox:
            res = client.post('/reset-pass', data={
                "token": token,
                "new_pass": new_pass
            }, follow_redirects=True)
            self.assertEqual(expect_email_count, len(outbox))
        return res

    def perform_pass_change(self, client, user, uid=None, tkn=None, eq_chk=True):
        if tkn is None:
            tkn = generate_reset_token(uid)
        new_pass = rand_string(15)
        res = self.change_pass_to(client, tkn, new_pass)
        if eq_chk:
            self.assertEqual(200, res.status_code)
            assert_pass_reset_success(res)
        else:
            self.assertNotEqual(200, res.status_code)
            assert_not_pass_reset_success(res)

        return tkn, new_pass

    @with_login(user1)
    def test_reset(self, client):
        # Yes, this test is kinda dumb.
        # You can reset your password while you are logged in.
        # This can be leveraged for a "change password" feature.
        # First change
        tkn, new_pass = self.perform_pass_change(client, user1["email_address"], uid=user1["_id"])

        # Second time; won't work since we already used that token
        self.perform_pass_change(client, user1["email_address"], tkn=tkn, eq_chk=False)

        # Login with new password
        res = self.try_relog(client, user1["email_address"], new_pass)
        self.assertEqual(200, res.status_code)
        assert_index_page(res)

    @with_test_client
    def test_reset_not_logged_in(self, client):
        # We need to allow password reset when they are not logged in as well
        tkn, new_pass = self.perform_pass_change(client, user1["email_address"], uid=user1["_id"])

        # Second time; won't work since we already used that token
        self.perform_pass_change(client, user1["email_address"], tkn=tkn, eq_chk=False)

        # Login with new password
        res = self.try_relog(client, user1["email_address"], new_pass)
        self.assertEqual(200, res.status_code)
        assert_index_page(res)

def generate_reset_token(uid, time=None):
    if time is None:
        time = datetime.utcnow()
    return pli.get_signer().dumps((uid, time))
