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
        self.try_add(client, ["What's New"], status_code=200, **form)
        u = get_site_title(title)
        # check_page(u, title, body, self.assertTrue)


    @with_login(user2["email_address"], user2["real_pass"])
    def test_add_bad_auth(self, client):
        title, body, form = make_post_form()
        self.try_add(client, ["Not Authorized"], status_code=403, **form)
        self.assertIsNone(get_site_title(title))

    @with_test_client
    def test_add_no_auth(self, client):
        title, body, form = make_post_form()
        self.try_add(client, ["Login"], status_code=200, **form)
        self.assertIsNone(get_site_title(title))

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_get_auth(self, client):
        res = client.get("/blog/add")
        self.assertEqual(200, res.status_code)
        self.assertTrue("Title" in res.data)
        self.assertTrue("Attach" in res.data)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_add_get_no_auth(self, client):
        res = client.get("/blog/add")
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_add_get_not_logged_in(self, client):
        res = client.get("/blog/add")
        self.assertEqual(302, res.status_code)
        self.assertTrue("login" in res.data)

        
def make_post_form(**kwargs):
    # TODO make proper form with files and stuff.
    data = dict(**kwargs)
    if "title" not in data:
        data["title"] = rand_string(15)
    if "body" not in data:
        data["body"] = rand_string(100)
    return data["title"], data["body"], data

def post_add_blog(client, **kwargs):
    return client.post('/blog/add',
                       data=kwargs,
                       follow_redirects=True)

def get_site_title(title):
    return get_db().usercontent.find_one({"title":title})

def check_page(doc, title, body, check):
    check(title == doc["title"])
    check(body == doc["body"])
