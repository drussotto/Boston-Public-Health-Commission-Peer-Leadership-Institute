from testlib import *
import uuid

class AddBlogPageTest(PliEntireDbTestCase):

    def try_add(self, client, expect, trueFun=None, equalFun=None, **data):
        if trueFun is None:
            trueFun = self.assertTrue
        if equalFun is None:
            equalFun = self.assertEqual
        stat_code = data.pop("status_code", None)
        res = post_add_blog(client, **data)
        if stat_code is not None:
            equalFun(stat_code, res.status_code)
        for s in expect:
            trueFun(s, s in res.data)
        return res

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_good_auth(self, client):
        title, body, form = make_post_form()
        self.try_add(client, ["Success!"], status_code=200, **form)
        u = get_site(title)
        check_page(u, title, body, self.assertTrue)


    @with_login(user2["email_address"], user2["real_pass"])
    def test_add_bad_auth(self, client):
        title, body, form = make_post_form()
        self.try_add(client, ["Unauthorized"], status_code=403, **form)
        self.assertIsNone(get_site(title))

    @with_test_client
    def test_add_no_auth(self, client):
        title, body, form = make_post_form()
        self.try_add(client, ["Login"], status_code=200, **form)
        self.assertIsNone(get_site(title))



class RemoveBlogPageTest(PliEntireDbTestCase):
    # Admins allowed to remove everyone's content
    # Otherwise you can only remove your own content

    def try_remove_suc(self, client, page):
        res = client.post('/uc/remove?page='+str(page), follow_redirects=True)
        self.assertEqual(200, res.status_code)
        self.assertTrue("Success" in res.data)

    def try_remove_fail(self, client, page, logged_in=True):
        res = client.post('/uc/remove?page='+str(page))
        if logged_in:
            self.assertEqual(403, res.status_code)
            self.assertTrue("Forbidden" in res.data)
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
        # self.show_blog_four(client)
        # self.show_blog_three(client)
        # # This user cannot see blog one
        # self.show_blog_one(client, pg=["Unauthorized"], status_code=403)

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

def post_add_blog(client, **kwargs):
    return client.post('/uc/add',
                       data=kwargs,
                       follow_redirects=True)

def make_post_form(**kwargs):
    # TODO make proper form with files and stuff.
    data = dict(**kwargs)
    if "title" not in data:
        data["title"] = rand_string(15)
    if "body" not in data:
        data["body"] = rand_string(100)
    return data["title"], data["body"], data

def get_site(title):
    return get_db().usercontent.find_one({"title":title})

def check_page(doc, title, body, check):
    check(title == doc["title"])
    check(body == doc["body"])
