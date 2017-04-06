from testlib import *
from pli import get_db

# Tests for adding, removing, editing, activating/deactivating staff for the staff page

class StaffTest(PliEntireDbTestCase):

    def add_dummy_staff(self, client, active):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as picture:
            res = post_add_staff(client, "Dummy", "Test Title", "some bio", picture, "fakeemail@fakeemail.com", "111-111-1111", active, 0)
        self.assertEqual(200, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_active_staff(self, client):
        self.add_dummy_staff(client, True)
        staff_page = client.get('/page/staff.html')
        self.assertTrue("Dummy" in staff_page.data)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_inactive_staff(self, client):
        self.add_dummy_staff(client, False)
        staff_page = client.get('/page/staff.html')
        self.assertFalse("Dummy" in staff_page.data)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_staff_missing_fields(self, client):
        res = post_add_staff(client, "Dummy", "Dummy Title", "Bio", None, None, None, True, 0)
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
        self.assertTrue("Dummy" in staff_page.data)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_deactivate_staff(self, client):
        self.assertTrue(ex.staff1["active"])
        res = post_edit_staff(client, ex.staff1["_id"], {"active": False})
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
#        print(staff_page.data)
        self.assertFalse(ex.staff1["name"] in staff_page.data)
        editted = get_db().staff.find_one({"_id": ex.staff1["_id"]})
        self.assertFalse(editted["active"])

    @with_login(user1["email_address"], user1["real_pass"])
    def test_activate_staff(self, client):
        self.assertFalse(ex.staff_inactive["active"])
        res = post_edit_staff(client, ex.staff1["_id"], {"active": True})
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
        self.assertFalse(ex.staff_inactive["name"] in staff_page.data)
        self.assertFalse(ex.staff_inactive["active"])

    @with_login(user1["email_address"], user1["real_pass"])
    def test_edit_staff(self, client):
        res = post_edit_staff(client, ex.staff1["_id"], {"name": "Dummy", "title": "Dummy Title"})
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
        editted = get_db().staff.find_one({"_id": ex.staff1["_id"]})
        self.assertEqual(editted["name"], "Dummy")
        self.assertEqual(editted["title"], "Dummy Title")
        self.assertTrue("Dummy" in staff_page.data)

    @with_login(user3["email_address"], user3["real_pass"])
    def test_add_staff_unauthorized(self, client):
        res = post_add_staff(client, "Dummy", "Dummy Title", "Bio", None, None, None, True, 0)
        self.assertEqual(403, res.status_code)

    @with_login(user3["email_address"], user3["real_pass"])
    def test_edit_staff_unauthorized(self, client):
        res = post_edit_staff(client, ex.staff1["_id"], {"name": "Dummy"})
        self.assertEqual(403, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_staff_invalid(self, client):
        res = post_add_staff(client, None, "Dummy Title", "Bio", None, None, None, None, 0)
        self.assertEqual(400, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_edit_staff_invalid(self, client):
        # missing sending staff _id
        res = client.post("/manage/staff/edit", data={"title":"nope"}, follow_redirects=True)
        self.assertEqual(400, res.status_code)
    @with_login(user1["email_address"], user1["real_pass"])
    def test_edit_staff_invalid_id(self, client):
        # bad staff _id
        res = post_edit_staff(client, ObjectId(), {"active": True})
        self.assertEqual(400, res.status_code)
        
def post_add_staff(client, name, title, bio, picture, email, phone, active, order):
    data = {}
    if name:
        data["name"] = name
    if title:
        data["title"] = title
    if bio:
        data["bio"] = bio
    if picture:
        data["picture"] = picture
    if email:
        data["email"] = email
    if phone:
        data["phone"] = phone
    if active:
        data["active"] = True
    if order:
        data["order"] = order
    return client.post("/manage/staff/add", data=data, follow_redirects=True)

def post_edit_staff(client, id, data):
    return client.post("/manage/staff/edit?id="+str(id), data=data, follow_redirects=True)
