from testlib import *
import uuid

class ShowBlogPageTest(PliEntireDbTestCase):
    # Users can always see their own posts
    # Admins can see all posts
    # If they aren't an admin, or the owner
    # they must have permissions to view the page
    # unless the page doesn't require any permissions,
    # in which case you don't need to be logged in.

    def try_show(self, client, expect, blog_id, status_code=200):
        res = client.get("/uc/show?page="+str(blog_id))
        self.assertEqual(status_code, res.status_code)
        for s in expect:
            self.assertTrue(s, s in res.data)

    def show_blog_four(self, client):
        self.try_show(client,
                      ["For the public", "A post"],
                      ex.blog_page_four["_id"])

    def show_blog_one(self, client, pg=["Page one", "Body one"], status_code=200):
        self.try_show(client, pg, ex.blog_page_one["_id"], status_code=status_code)

    def show_blog_two(self, client, pg=["Page two", "Body two", "mongodb.png"], status_code=200):
        self.try_show(client, pg, ex.blog_page_two["_id"], status_code=status_code)

    def show_blog_three(self, client, pg=["Page three", "Body three"], status_code=200):
        self.try_show(client, pg, ex.blog_page_three["_id"], status_code=status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_good_with_auth(self, client):
        self.show_blog_four(client)
        self.show_blog_three(client)
        # This user can also see blog one
        self.show_blog_one(client)
        # This user can't see page two
        # But is an admin
        self.show_blog_two(client)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_good_no_auth(self, client):
        self.show_blog_four(client)
        self.show_blog_three(client)
        # This user cannot see blog one
        self.show_blog_one(client, pg=["Unauthorized"], status_code=403)

        # This user doesn't have perms to see this post
        # But they own it, so they should see it anyways
        self.show_blog_two(client)

    @with_login(user4["email_address"], user4["real_pass"])
    def test_good_no_auth_perm(self, client):
        self.show_blog_four(client)
        self.show_blog_three(client)
        # This user cannot see blog one
        self.show_blog_one(client, pg=["Unauthorized"], status_code=403)
        # This user can see page two
        self.show_blog_two(client)

    @with_test_client
    def test_not_logged_in(self, client):
        self.show_blog_four(client)
        self.show_blog_three(client)
        # Since we aren't logged in
        # site should ask them to log in to view the post
        self.show_blog_one(client, pg=["Login"], status_code=302)
        self.show_blog_two(client, pg=["Login"], status_code=302)

    @with_test_client
    def test_show_bad_ids(self, client):
        self.try_show(client, ["login"], "abc3498943", status_code=302)
        self.try_show(client, ["login"], uuid.uuid1(), status_code=302)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_show_bad_ids_not_admin(self, client):
        self.try_show(client, ["Forbidden"], "abc3498943", status_code=403)
        self.try_show(client, ["Forbidden"], uuid.uuid1(), status_code=403)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_show_bad_ids_admin(self, client):
        self.try_show(client, ["Forbidden"], "abc3498943", status_code=403)
        self.try_show(client, ["Forbidden"], uuid.uuid1(), status_code=403)
