import os
from testlib import *
from pli.service_util import get_db, get_gridfs
from mongomock.object_id import ObjectId
class WnDisplay(PliEntireDbTestCase):

    @with_test_client
    def test_displaying_cards(self, client):
        index = client.get('/')
        assert_index_page(self, index)
        for card in get_show_list():
            self.assertTrue(card["caption"] in index.data)
            self.assertTrue(card["sub_caption"] in index.data)
            self.assertTrue(str(card["background"]) in index.data)
            self.assertTrue(card["hyperlink"] in index.data)




    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_wn_card(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(200, res.status_code)
        l = get_db().cards.find_one({"caption": "Caption"})
        self.assertEqual(str(l["_id"]), res.data)
        bytez = get_gridfs().get(l["background"]).read()
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            self.assertEquals(bytez, f.read())

    @with_login(user2["email_address"], user2["real_pass"])
    def test_add_wn_card_noauth(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(403, res.status_code)

def post_add_wn_card(client, f, caption, sub_caption, hyperlink):
    data = {
        "caption": caption,
        "sub_caption": sub_caption,
        "hyperlink": hyperlink,
        "background": f
    }
    return client.post("/add-wn-card", data=data, follow_redirects=True)
