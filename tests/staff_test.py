from testlib import *

# Tests for adding, removing, editing, activating/deactivating staff for the staff page

class StaffTest(PliEntireDbTestCase):

    def add_dummy_staff(self, client, active):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as picture:
            res = post_add_staff(client, "Dummy", "Test Title", "some bio", picture, "fakeemail@fakeemail.com", active)
        self.assertEqual(200, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_active_staff(self, client):
        self.add_dummy_staff(client, True)
        staff_page = client.get('/page/staff.html')
        self.assertTrue("Dummy" in staff_page)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_inactive_staff(self, client):
        self.add_dummy_staff(client, False)
        staff_page = client.get('/page/staff.html')
        self.assertFalse("Dummy" in staff_page)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_staff_missing_fields(self, client):
        res = post_add_staff(client, "Dummy", "Dummy Title", "Bio", None, None, None, True)
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
        self.assertFalse("Dummy" in staff_page)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_deactivate_staff(self, client):
        self.assertTrue(ex.staff1["active"])
        res = post_edit_staff(client, {"_id": staff1["_id"], "active": False})
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
        self.assertFalse(ex.staff1["name"] in staff_page)
        self.assertFalse(ex.staff1["active"])

    @with_login(user1["email_address"], user1["real_pass"])
    def test_activate_staff(self, client):
        self.assertFalse(ex.staff_inactive["active"])
        res = post_edit_staff(client, {"_id": staff1["_id"], "active": True})
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
        self.assertTrue(ex.staff_inactive["name"] in staff_page)
        self.assertTrue(ex.staff_inactive["active"])

    @with_login(user1["email_address"], user1["real_pass"])
    def test_edit_staff(self, client):
        res = post_edit_staff(client, {"_id": staff1["_id"], "name": "Dummy", "Title": "Dummy Title"})
        self.assertEqual(200, res.status_code)
        staff_page = client.get('/page/staff.html')
        self.assertEqual(staff1["name"], "Dummy")
        self.assertEqual(staff1["title"], "Dummy Title")
        self.assertFalse("Dummy" in staff_page)

    @with_login(user3["email_address"], user3["real_pass"])
    def test_add_staff_unauthorized(self, client):
        res = post_add_staff(client, "Dummy", "Dummy Title", "Bio", None, None, None, True)
        self.assertEqual(403, res.status_code)

    @with_login(user3["email_address"], user3["real_pass"])
    def test_edit_staff_unauthorized(self, client):
        res = post_edit_staff(client, {"_id": staff1["_id"], "name": "Dummy"})
        self.assertEqual(403, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_staff_invalid(self, client):
        res = post_add_staff(client, None, "Dummy Title", "Bio", None, None, None, None)
        self.assertEqual(400, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_edit_staff_invalid(self, client):
        # missing sending staff _id
        res = post_edit_staff(client, {"name": "Dummy"})
        self.assertEqual(400, res.status_code)

def post_add_staff(client, name, title, bio, picture, email, phone, active):
    data = {
        "name": name,
        "title": title,
        "bio": bio,
        "picture": picture,
        "email": email,
        "phone": phone,
        "active": active
    }
    return client.post("/staff/add", data=data, follow_redirects=True)

def post_edit_staff(client, data):
    return client.post("/staff/edit", data=data, follow_redirects=True)
