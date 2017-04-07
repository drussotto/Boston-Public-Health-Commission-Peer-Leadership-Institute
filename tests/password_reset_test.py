from testlib import *
#from datetime import datetime
import pli
import time
class TestPasswordReset(PliEntireDbTestCase):
    def try_relog(self, client, user, passwd):
        self.assertEqual(200, client.get('/logout', follow_redirects=True).status_code)
        # Try logging in with the new password
        return post_login(client, user, passwd)

    def change_pass_to(self, client, token, new_pass):
        res = client.post('/pass-reset', data={
            "reset_token": token,
            "reset_new_password": new_pass,
            "reset_confirm_password": new_pass
        }, follow_redirects=True)
        return res

    def perform_pass_change(self, client, user, uid=None, tkn=None, eq_chk=True):
        if tkn is None:
            tkn = generate_reset_token(uid)
        new_pass = rand_string(15)
        res = self.change_pass_to(client, tkn, new_pass)
        if eq_chk:
            self.assertEqual(200, res.status_code)
        else:
            self.assertNotEqual(200, res.status_code)

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

    @with_test_client
    def test_reset_not_logged_in(self, client):
        # We need to allow password reset when they are not logged in as well
        tkn, new_pass = self.perform_pass_change(client, user1["email_address"], uid=user1["_id"])

        # Second time; won't work since we already used that token
        self.perform_pass_change(client, user1["email_address"], tkn=tkn, eq_chk=False)

        # Login with new password
        res = self.try_relog(client, user1["email_address"], new_pass)
        self.assertEqual(200, res.status_code)

    @with_test_client
    def test_reset_old_token(self, client):
        tkn = generate_reset_token(user1["_id"], time.time() - (10 * 60)) # Token is going to be too old.
        # Reset won't work since we are using an old token
        self.perform_pass_change(client, user1["email_address"], tkn=tkn, eq_chk=False)

        # The password shouldn't have changed, so we try and log in with the old password
        res = self.try_relog(client, user1["email_address"], user1["real_pass"])
        self.assertEqual(200, res.status_code)

    @with_test_client
    def test_email_sent(self, client):
        with pli.get_mail().record_messages() as outbox:
            res = client.post('/init-pass-reset', data={"email":user1["email_address"]})
            self.assertEqual(200, res.status_code)
            self.assertEqual(1, len(outbox))
        


def generate_reset_token(uid, t=None):
    if t is None:
        t = time.time()
    return pli.get_signer().dumps((uid, t))
