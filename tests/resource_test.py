from pli import get_db
from testlib import *

# add
# activate
# deactivate
# query_by_type
# query_by_category


class AddResourceTestCase(PliEntireDbTestCase):

    @with_login(user1)
    def test_add1(self, client):
        f = make_add_form_data()
        res = client.post('/resources/add', data=f)
        self.assertEqual(200, res.status_code)
        doc = get_db().resources.find_one({"link": f["link"]})
        del doc["_id"]
        self.assertEqual(f, doc)

    @with_login(user2)
    def test_add2(self, client):
        f = make_add_form_data()
        res = client.post('/resources/add', data=f)
        self.assertEqual(403, res.status_code)
        doc = get_db().resources.find_one({"link": f["link"]})
        self.assertIsNone(doc)

    @with_test_client
    def test_add3(self, client):
        f = make_add_form_data()
        res = client.post('/resources/add', data=f)
        self.assertEqual(302, res.status_code)

    @with_login(user1)
    def test_add4(self, client):
        f = make_add_form_data()
        l = ["link", "name", "category", "rtype"]
        ll = len(l)
        for idx, x in enumerate(l):
            fnew = dict(f)
            del fnew[x]
            res = client.post('/resources/add', data=fnew)
            self.assertEqual(400, res.status_code)
            key = l[(idx+1) % ll]
            doc = get_db().resources.find_one({key: f[key]})
            self.assertIsNone(doc)

            
class ActivateDeactivateResourceTestCase(PliEntireDbTestCase):


    @with_login(user1)
    def test_activate1(self, client):
        d = get_res(ex.resource3["_id"])
        self.assertFalse(d["active"])
        res = client.post('/resources/activate?id='+str(ex.resource3["_id"]))
        self.assertEqual(200, res.status_code)
        d = get_res(ex.resource3["_id"])
        self.assertTrue(d["active"])

    @with_login(user1)
    def test_activate2(self, client):
        d = get_res(ex.resource1["_id"])
        self.assertTrue(d["active"])
        res = client.post('/resources/activate?id='+str(ex.resource1["_id"]))
        self.assertEqual(200, res.status_code)
        d = get_res(ex.resource1["_id"])
        self.assertTrue(d["active"])

    @with_login(user1)
    def test_deactivate1(self, client):
        d = get_res(ex.resource1["_id"])
        self.assertTrue(d["active"])
        res = client.post('/resources/deactivate?id='+str(ex.resource1["_id"]))
        self.assertEqual(200, res.status_code)
        d = get_res(ex.resource1["_id"])
        self.assertFalse(d["active"])

    @with_login(user1)
    def test_deactivate2(self, client):
        d = get_res(ex.resource3["_id"])
        self.assertFalse(d["active"])
        res = client.post('/resources/deactivate?id='+str(ex.resource3["_id"]))
        self.assertEqual(200, res.status_code)
        d = get_res(ex.resource3["_id"])
        self.assertFalse(d["active"])
    
    @with_login(user2)
    def test_activate3(self, client):
        d = get_res(ex.resource3["_id"])
        self.assertFalse(d["active"])
        res = client.post('/resources/activate?id='+str(ex.resource3["_id"]))
        self.assertEqual(403, res.status_code)
        d = get_res(ex.resource3["_id"])
        self.assertFalse(d["active"])

    @with_login(user2)
    def test_deactivate3(self, client):
        d = get_res(ex.resource1["_id"])
        self.assertTrue(d["active"])
        res = client.post('/resources/deactivate?id='+str(ex.resource1["_id"]))
        self.assertEqual(403, res.status_code)
        d = get_res(ex.resource1["_id"])
        self.assertTrue(d["active"])
        
    @with_test_client
    def test_activate4(self, client):
        d = get_res(ex.resource3["_id"])
        self.assertFalse(d["active"])
        res = client.post('/resources/activate?id='+str(ex.resource3["_id"]))
        self.assertEqual(302, res.status_code)
        d = get_res(ex.resource3["_id"])
        self.assertFalse(d["active"])

    @with_test_client
    def test_deactivate4(self, client):
        d = get_res(ex.resource1["_id"])
        self.assertTrue(d["active"])
        res = client.post('/resources/deactivate?id='+str(ex.resource1["_id"]))
        self.assertEqual(302, res.status_code)
        d = get_res(ex.resource1["_id"])
        self.assertTrue(d["active"])

    @with_login(user1)
    def test_activate5(self, client):
        res = client.post('/resources/activate?id=dslkdjsk')
        self.assertEqual(404, res.status_code)

    @with_login(user1)
    def test_deactivate5(self, client):
        res = client.post('/resources/deactivate?id=dslkdjsk')
        self.assertEqual(404, res.status_code)
        
    @with_login(user1)
    def test_activate6(self, client):
        res = client.post('/resources/activate')
        self.assertEqual(404, res.status_code)

    @with_login(user1)
    def test_deactivate7(self, client):
        res = client.post('/resources/deactivate')
        self.assertEqual(404, res.status_code)


class QueryResourceTestCase(PliEntireDbTestCase):
    pass

def make_add_form_data():
    return {
        "link": rand_string(50),
        "name": rand_string(50),
        "category": rand_string(50),
        "rtype": rand_string(50),
        "active": True
    }

def get_res(id):
    return get_db().resources.find_one({"_id": id})
