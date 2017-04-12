from testlib import *
import uuid

class RemoveBlogPageTest(PliEntireDbTestCase):
    # Admins allowed to remove everyone's content
    # Otherwise you can only remove your own content

    def try_remove_suc(self, client, page):
        res = client.post('/blog/remove?id='+str(page), follow_redirects=True)
        self.assertEqual(200, res.status_code)
        #self.assertTrue("Success" in res.data)

    def try_remove_fail(self, client, page, logged_in=True):
        res = client.post('/blog/remove?id='+str(page))
        if logged_in:
            self.assertEqual(403, res.status_code)
            self.assertTrue("Not Authorized" in res.data)
        else:
            self.assertEqual(302, res.status_code)
            self.assertTrue("login" in res.data)


    @with_login(user1["email_address"], user1["real_pass"])
    def test_admin_remove_all(self, client):
        for p in [ex.blog_page_one,
                  ex.blog_page_two,
                  ex.blog_page_three,
                  ex.blog_page_four]:
            self.try_remove_suc(client, p["_id"])

        # All pages were removed.
        self.assertEqual(0, len(list_all_pages()))

    @with_login(user2["email_address"], user2["real_pass"])
    def test_own_remove_all(self, client):
        # User2 owns page 2 and page 4
        self.try_remove_suc(client, ex.blog_page_two["_id"])
        self.try_remove_suc(client, ex.blog_page_four["_id"])
        # And they don't own these
        self.try_remove_fail(client, ex.blog_page_three["_id"])
        self.try_remove_fail(client, ex.blog_page_one["_id"])

        # The only pages that are left are 1 & 3
        pleft = map(lambda x: str(x["_id"]), list_all_pages())
        self.assertEqual(2, len(pleft))
        self.assertTrue(str(ex.blog_page_three["_id"]) in pleft)
        self.assertTrue(str(ex.blog_page_one["_id"]) in pleft)

    @with_test_client
    def test_remove_not_logged_in(self, client):
        self.try_remove_fail(client, ex.blog_page_one["_id"], logged_in=False)
        self.try_remove_fail(client, ex.blog_page_two["_id"], logged_in=False)
        self.try_remove_fail(client, ex.blog_page_three["_id"], logged_in=False)
        self.try_remove_fail(client, ex.blog_page_four["_id"], logged_in=False)
        # We've been redirected to login for each call,
        # so all the content should still be there.
        self.assertEqual(4, len(list_all_pages()))

    def do_bad_reqs(self, client, logged_in=True):
        self.try_remove_fail(client, "abc3498943", logged_in=logged_in)
        self.try_remove_fail(client, uuid.uuid1(), logged_in=logged_in)

    @with_test_client
    def test_remove_bad_page_no_login(self, client):
        self.do_bad_reqs(client, logged_in=False)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_remove_bad_page_logged_in_not_admin(self, client):
        self.do_bad_reqs(client)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_remove_bad_page_logged_in_admin(self, client):
        self.do_bad_reqs(client)


def get_site_id(id):
    return get_db().usercontent.find_one({"_id":id})
