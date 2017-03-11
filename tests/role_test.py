from testlib import *
from pli import ADMIN_PERM, PARTICIPANT_PERM, ORG_PERM, EDITOR_PERM, \
    ADMIN_ROLE, PARTICIPANT_ROLE, ORG_ROLE, EDITOR_ROLE, PliUser


class PermTest(PliEntireDbTestCase):
    
    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin(self, client):
        self.assertTrue(EDITOR_PERM.can())
        self.assertTrue(ADMIN_PERM.can())
        self.assertFalse(PARTICIPANT_PERM.can())
        self.assertFalse(ORG_PERM.can())
        
    @with_login(user2["email_address"], user2["real_pass"])
    def test_check_participant(self, client):
        self.assertFalse(EDITOR_PERM.can())
        self.assertFalse(ADMIN_PERM.can())
        self.assertTrue(PARTICIPANT_PERM.can())
        self.assertFalse(ORG_PERM.can())

    @with_login(user3["email_address"], user3["real_pass"])
    def test_check_none(self, client):
        self.assertFalse(EDITOR_PERM.can())
        self.assertFalse(ADMIN_PERM.can())
        self.assertFalse(PARTICIPANT_PERM.can())
        self.assertFalse(ORG_PERM.can())

class AddPermTest(PliEntireDbTestCase):

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_not_add_bad_uid(self, client):
        self.assertTrue(ADMIN_PERM.can())
        
        # 400 => Not added
        # That UID doesn't exist.
        self.assertEqual(400, post_add_role(client, ORG_ROLE, 543))

    
    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add(self, client):
        self.assertTrue(ADMIN_PERM.can())
        
        # 200 => we added the role.
        self.assertEqual(200, post_add_role(client, ORG_ROLE, user2["_id"]))
        self.assertEqual([PARTICIPANT_ROLE, ORG_ROLE], PliUser.get(user2["_id"]).roles)

        # 409 => Already added.
        self.assertEqual(409, post_add_role(client, ORG_ROLE, user2["_id"]))
        self.assertEqual([PARTICIPANT_ROLE, ORG_ROLE], PliUser.get(user2["_id"]).roles)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add_self(self, client):
        self.assertTrue(ADMIN_PERM.can())
        
        # 200 => we added the role.
        self.assertEqual(200, post_add_role(client, ORG_ROLE, user1["_id"]))
        # Check that the role caching isn't broken.
        self.assertTrue(EDITOR_PERM.can())
        self.assertEqual([ADMIN_ROLE, EDITOR_ROLE, ORG_ROLE], PliUser.get(user1["_id"]).roles)


    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add_admin(self, client):
        self.assertTrue(ADMIN_PERM.can())

        # 200 => we added the role.
        self.assertEqual(200, post_add_role(client, ADMIN_ROLE, user2["_id"]))
        self.assertEqual([PARTICIPANT_ROLE, ADMIN_ROLE], PliUser.get(user2["_id"]).roles)

        
    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_add2(self, client):
        self.assertTrue(ADMIN_PERM.can())
        # 200 => we added the role.
        self.assertEqual(200, post_add_role(client, ADMIN_ROLE, user3["_id"]))
        self.assertEqual([ADMIN_ROLE], PliUser.get(user3["_id"]).roles)


    @with_login(user2["email_address"], user2["real_pass"])
    def test_check_non_admin_add(self, client):
        self.assertFalse(ADMIN_PERM.can())
        # 403 => We couldn't add the role.
        self.assertEqual(403, post_add_role(client, ORG_ROLE, user3["_id"]))
        self.assertEqual([], PliUser.get(user3["_id"]).roles)

    @with_test_client
    def test_check_not_logged_in(self, client):
        self.assertEqual(403, post_add_role(client, ORG_ROLE, user3["_id"]))
        self.assertEqual([], PliUser.get(user3["_id"]).roles)


class RemovePermTest(PliEntireDbTestCase):

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_not_rm_bad_uid(self, client):
        self.assertTrue(ADMIN_PERM.can())
        
        # 400 => Not added
        # That UID doesn't exist.
        self.assertEqual(400, post_rm_role(client, ORG_ROLE, 543))

    
    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_rm(self, client):
        self.assertTrue(ADMIN_PERM.can())
        # 409 => Wasn't there.
        self.assertEqual(409, post_rm_role(client, ORG_ROLE, user2["_id"]))
        self.assertEqual([PARTICIPANT_ROLE], PliUser.get(user2["_id"]).roles)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_rm2(self, client):
        self.assertTrue(ADMIN_PERM.can())
        # 409 => Wasn't there.
        self.assertEqual(409, post_rm_role(client, ORG_ROLE, user3["_id"]))
        self.assertEqual([], PliUser.get(user3["_id"]).roles)


    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_rm_admin(self, client):
        self.assertTrue(ADMIN_PERM.can())

        # 200 => we added the role.
        self.assertEqual(200, post_rm_role(client, PARTICIPANT_ROLE, user2["_id"]))
        self.assertEqual([], PliUser.get(user2["_id"]).roles)

        
    @with_login(user1["email_address"], user1["real_pass"])
    def test_check_admin_rm2(self, client):
        self.assertTrue(ADMIN_PERM.can())
        # 200 => we removed the role.
        self.assertEqual(200, post_rm_role(client, EDITOR_ROLE, user1["_id"]))
        self.assertEqual([ADMIN_ROLE], PliUser.get(user1["_id"]).roles)

    @with_test_client
    def test_check_rm_not_logged_in(self, client):
        self.assertEqual(403, post_rm_role(client, ORG_ROLE, user3["_id"]))
        self.assertEqual([], PliUser.get(user3["_id"]).roles)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_check_non_admin_rm(self, client):
        self.assertFalse(ADMIN_PERM.can())
        # 403 => We couldn't rm the role.
        self.assertEqual(403, post_rm_role(client, ORG_ROLE, user2["_id"]))
        self.assertEqual([PARTICIPANT_ROLE], PliUser.get(user2["_id"]).roles)
