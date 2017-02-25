from testlib import *
from application import application as pli
from flask_login import current_user, logout_user, login_user
pli.testing = True


class LoginTestCase(PliUsersTestCase):
    
    @classmethod
    def setUpClass(cls):
        def test_login():
            return str(current_user.is_authenticated), 200
        pli.add_url_rule("/test-login", endpoint="test_login", view_func=test_login)
        

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
    @with_login(user1["email_address"], user1["real_pass"], to="resources.html")
    def test_good_login_post_red1(self, client, res):
        self.assert_logged_in()
        assert_res_page(self, res)

    @with_req_ctxt
    @with_login(user2["email_address"], user2["real_pass"], to="surveys.html")
    def test_good_login_post_redirect1(self, client, res):
        self.assert_logged_in()
        self.assert_cur_uid(get_u(user2["_id"]))
        assert_surv_page(self, res)

    @with_req_ctxt
    @with_login(user1["email_address"], user2["real_pass"], to="resources.html")
    def test_bad_login_redirect1(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(user2["email_address"], user3["real_pass"], to="resources.html")
    def test_bad_login_redirect2(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(32, user1["real_pass"],to="resources.html")
    def test_bad_login_redirect3(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login("", "",to="resources.html")
    def test_bad_login_redirect4(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(None, None, to="resources.html")
    def test_bad_login_redirect5(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login("{ $gt : \"*\" }", "{ $gt : \"*\" }", to="resources.html")
    def test_bad_login_redirect6(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)

    @with_req_ctxt
    @with_login(user2["email_address"], user2["real_pass"])
    def test_logout1(self, client, res):
        self.assert_logged_in()
        assert_index_page(self, res)
        res = client.get('/logout')
        self.assert_not_logged_in()

    @with_req_ctxt
    @with_login(user1["email_address"], user2["real_pass"])
    def test_logout2(self, client, res):
        self.assert_not_logged_in()
        assert_login_page(self, res)
        res = client.get('/logout')
        self.assert_not_logged_in()
    
    def test_saved_login(self):
        # Tests whether the login persists accross requests
        client = pli.test_client()
        r = post_login(client, user1["email_address"], user1["real_pass"])
        assert_index_page(self, r)
        # route registered during test setup
        r = client.get("/test-login")
        self.assertTrue(r.data == "True")

    def test_bad_login_not_saved(self):
        client = pli.test_client()
        r = post_login(client, user1["email_address"], user2["real_pass"])
        assert_login_page(self, r)
        r = client.get("/test-login")
        self.assertTrue(r.data == "False")
