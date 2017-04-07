from testlib import *
from pli import PliUser
import pli

ADMIN_PERM = pli.roles.all_roles._ADMIN_PERM
EDITOR_PERM = pli.roles.all_roles._EDITOR_PERM
PEERLEADER_PERM = pli.roles.all_roles._PEERLEADER_PERM
USER_PERM = pli.roles.all_roles._USER_PERM

ADMIN_ROLE = pli.roles.all_roles._ADMIN_ROLE
EDITOR_ROLE = pli.roles.all_roles._EDITOR_ROLE
PEERLEADER_ROLE = pli.roles.all_roles._PEERLEADER_ROLE
USER_ROLE = pli.roles.all_roles._USER_ROLE

class PermTest(PliEntireDbTestCase):

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin(self, client):
        self.assertTrue(pli.has_editor())
        self.assertTrue(pli.has_admin())
        self.assertTrue(pli.has_peerleader())
        self.assertTrue(pli.has_user())

    @with_login(user2["email_address"], user2["real_pass"])
    def test_check_participant(self, client):
        self.assertFalse(pli.has_editor())
        self.assertFalse(pli.has_admin())
        self.assertTrue(pli.has_peerleader())
        self.assertTrue(pli.has_user())

    @with_login(user3["email_address"], user3["real_pass"])
    def test_check_none(self, client):
        self.assertFalse(pli.has_editor())
        self.assertFalse(pli.has_admin())
        self.assertFalse(pli.has_peerleader())
        self.assertTrue(pli.has_user())

class AddPermTest(PliEntireDbTestCase):

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_not_add_bad_uid(self, client):
        self.assertTrue(pli.has_admin())

        # 400 => Not added
        # That UID doesn't exist.
        res = post_add_role(client, 'user', 543)
        self.assertEqual(400, res.status_code)


    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add(self, client):
        self.assertTrue(ADMIN_PERM.can())

        # 200 => we added the role.
        res = post_add_role(client, PEERLEADER_ROLE, user2["_id"])
        self.assertEqual(200, res.status_code)
        self.assertEqual(PEERLEADER_ROLE, PliUser.get(user2["_id"]).role)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add_self(self, client):
        self.assertTrue(pli.has_admin)

        # 200 => we added the role.
        res = post_add_role(client, PEERLEADER_ROLE, user1["_id"])
        self.assertEqual(200, res.status_code)
        # Check that the role caching isn't broken.
        self.assertTrue(pli.has_editor())
        self.assertEqual(PEERLEADER_ROLE, PliUser.get(user1["_id"]).role)


    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add_admin(self, client):
        self.assertTrue(pli.has_admin())

        # 200 => we added the role.
        res = post_add_role(client, ADMIN_ROLE, user2["_id"])
        self.assertEqual(200, res.status_code)
        self.assertEqual(ADMIN_ROLE, PliUser.get(user2["_id"]).role)


    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add2(self, client):
        self.assertTrue(pli.has_admin())
        # 200 => we added the role.
        res = post_add_role(client, EDITOR_ROLE, user3["_id"])
        self.assertEqual(200, res.status_code)
        self.assertEqual(EDITOR_ROLE, PliUser.get(user3["_id"]).role)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add2(self, client):
        self.assertTrue(pli.has_admin())
        # This isn't a role
        res = post_add_role(client, "not-a-role", user3["_id"])
        self.assertEqual(400, res.status_code)
        self.assertEqual(USER_ROLE, PliUser.get(user3["_id"]).role)


    @with_login(user2["email_address"], user2["real_pass"])
    def test_check_non_admin_add(self, client):
        self.assertFalse(pli.has_admin())
        # 403 => We couldn't add the role.
        res = post_add_role(client, EDITOR_ROLE, user3["_id"])
        self.assertEqual(403, res.status_code)
        self.assertEqual(USER_ROLE, PliUser.get(user3["_id"]).role)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_not_logged_in(self, client):
        res = post_add_role(client, "not-a-role", user3["_id"])
        self.assertEqual(400, res.status_code)
        self.assertEqual(USER_ROLE, PliUser.get(user3["_id"]).role)


class RemovePermTest(PliEntireDbTestCase):

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_edit_role_page(self, client):
        self.assertTrue(pli.has_admin())

        res = client.get('/change-roles')
        self.assertEqual(200, res.status_code)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_check_non_admin_edit_role_page(self, client):
        self.assertFalse(pli.has_admin())

        # 403 => Participant cannot access page
        res = client.get('/change-roles')
        self.assertEqual(403, res.status_code)    \

    @with_login(user4["email_address"], user4["real_pass"])
    def test_check_peer_leader_pl_resource_page(self, client):
        self.assertTrue(pli.has_peerleader())

        res = client.get('/peer-leader-resources')
        self.assertEqual(200, res.status_code)

    @with_login(user3["email_address"], user3["real_pass"])
    def test_check_non_admin_edit_role_page(self, client):
        self.assertFalse(pli.has_peerleader())

        # 403 => Participant cannot access page
        res = client.get('/peer-leader-resources')
        self.assertEqual(403, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_editor_create_survey_page(self, client):
        self.assertTrue(pli.has_editor())

        res = client.get('/surveys/create')
        self.assertEqual(200, res.status_code)

    @with_login(user3["email_address"], user3["real_pass"])
    def test_check_non_editor_create_survey_page(self, client):
        self.assertFalse(pli.has_editor())

        # 403 => Participant cannot access page
        res = client.get('/surveys/create')
        self.assertEqual(403, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_editor_create_question_page(self, client):
        self.assertTrue(pli.has_editor())

        res = client.get('/surveys/questions/create')
        self.assertEqual(200, res.status_code)

    @with_login(user3["email_address"], user3["real_pass"])
    def test_check_non_editor_create_question_page(self, client):
        self.assertFalse(pli.has_editor())

        # 403 => Participant cannot access page
        res = client.get('/surveys/questions/create')
        self.assertEqual(403, res.status_code)
