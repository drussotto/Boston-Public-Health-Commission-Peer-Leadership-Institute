from testlib import *
import uuid

class EditBlogPageTest(PliEntireDbTestCase):

    def try_edit_suc(self, client, page):
        new_body = rand_string(1000)
        new_title = rand_string(1000)
        form = {"title": new_title, "body": new_body}
        res = client.post('/uc/edit?page='+str(page["_id"]), data=form)

        # We get redirected to the page.
        self.assertEqual(302, res.status_code)
        check_page(get_site_id(page["_id"]), new_title, new_body, self.assertTrue)

    def try_edit_fail(self, client, page, status_code=403, do_chk=True):
        new_body = rand_string(1000)
        new_title = rand_string(1000)
        form = {"title": new_title, "body": new_body}
        res = client.post('/uc/edit?page='+str(page["_id"]), data=form)

        # We get redirected to the page.
        self.assertEqual(status_code, res.status_code)
        if do_chk:
            check_page(get_site_id(page["_id"]), new_title, new_body, self.assertFalse)


        
    @with_login(user1["email_address"], user1["real_pass"])
    def test_admin_edit_all(self, client):
        for p in [ex.blog_page_one,
                  ex.blog_page_two,
                  ex.blog_page_three,
                  ex.blog_page_four]:
            self.try_edit_suc(client, p)
            
    @with_login(user2["email_address"], user2["real_pass"])
    def test_own_edit_all(self, client):
        # User2 owns page 2 and page 4
        self.try_edit_suc(client, ex.blog_page_two)
        self.try_edit_suc(client, ex.blog_page_four)
        # # And they don't own these
        self.try_edit_fail(client, ex.blog_page_three)
        self.try_edit_fail(client, ex.blog_page_one)

    @with_test_client
    def test_remove_not_logged_in(self, client):
        self.try_edit_fail(client, ex.blog_page_one, status_code=302)
        self.try_edit_fail(client, ex.blog_page_two, status_code=302)
        self.try_edit_fail(client, ex.blog_page_three, status_code=302)
        self.try_edit_fail(client, ex.blog_page_four, status_code=302)

    def spoof_doc(self, id):
        return {
            "_id": id,
            "title": rand_string(1000),
            "body": rand_string(1000)
        }
    
    def do_bad_reqs(self, client, status_code=302):
        self.try_edit_fail(client, self.spoof_doc("abc3498943"), status_code=status_code, do_chk=False)
        self.try_edit_fail(client, self.spoof_doc(str(uuid.uuid1())), status_code=status_code, do_chk=False)

    @with_test_client
    def test_remove_bad_page_no_login(self, client):
        self.do_bad_reqs(client)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_remove_bad_page_logged_in_not_admin(self, client):
        self.do_bad_reqs(client, status_code=403)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_remove_bad_page_logged_in_admin(self, client):
        self.do_bad_reqs(client, status_code=403)

        
def get_site_id(id):
    return get_db().usercontent.find_one({"_id":id})
