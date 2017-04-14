from pli import get_db, get_resource_by_type, get_resource_by_category
from testlib import *

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

    @with_app_ctxt
    def test_query_type1(self):
        resources = get_resource_by_type("student")
        self.assertEqual(1, len(resources))
        self.assertEqual(ex.resource1, resources[0])
        
    @with_app_ctxt
    def test_query_type2(self):
        resources = get_resource_by_type("peerleader")
        self.assertEqual(2, len(resources))
        self.assertEqual([ex.resource2,
                          ex.resource3], resources)

    @with_app_ctxt
    def test_query_type3(self):
        resources = get_resource_by_type("bogus")
        self.assertEqual(0, len(resources))

    @with_app_ctxt
    def test_query_type4(self):
        resources = get_resource_by_type("PEErleader")
        self.assertEqual(2, len(resources))
        self.assertEqual([ex.resource2,
                          ex.resource3], resources)

    @with_app_ctxt
    def test_query_cat1(self):
        resources = get_resource_by_category("wellness")
        self.assertEqual(1, len(resources))
        self.assertEqual(ex.resource3, resources[0])

    @with_app_ctxt
    def test_query_cat2(self):
        resources = get_resource_by_category("sexual health")
        self.assertEqual(2, len(resources))
        self.assertEqual([ex.resource2,
                          ex.resource1], resources)

    @with_app_ctxt
    def test_query_cat3(self):
        resources = get_resource_by_category("sexual fl;dgkfld")
        self.assertEqual(0, len(resources))

    @with_app_ctxt
    def test_query_cat4(self):
        resources = get_resource_by_category("SEXual health")
        self.assertEqual(2, len(resources))
        self.assertEqual([ex.resource2,
                          ex.resource1], resources)

        


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
