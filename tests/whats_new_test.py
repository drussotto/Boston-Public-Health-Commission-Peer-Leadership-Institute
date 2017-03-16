import os
from testlib import *
from pli.service_util import get_db, get_gridfs
from bson import ObjectId
from flask import current_app 
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

            
class WnAdd(PliEntireDbTestCase):

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_wn_card(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(200, res.status_code)
        l = get_db().cards.find_one({"caption": "Caption"})
        self.assertEqual(str(l["_id"]), res.data)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_add_wn_card_noauth(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_add_wn_card_not_logged_in(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(403, res.status_code)


class WnSet(PliEntireDbTestCase):
    
    @with_login(user1["email_address"], user1["real_pass"])
    def test_set_wn_card(self, client):
        res = post_set_wn_cards(client, [get_wn_card1(), get_wn_card0()])
        self.assertEqual(200, res.status_code)
        third_party = current_app.test_client()
        
        index = third_party.get('/')
        assert_index_page(self, index)
        
        for card in [get_wn_card1(), get_wn_card0()]:
            self.assertTrue(card["caption"] in index.data)
            self.assertTrue(card["sub_caption"] in index.data)
            self.assertTrue(str(card["background"]) in index.data)
            self.assertTrue(card["hyperlink"] in index.data)


def post_add_wn_card(client, f, caption, sub_caption, hyperlink):
    data = {
        "caption": caption,
        "sub_caption": sub_caption,
        "hyperlink": hyperlink,
        "background": f
    }
    return client.post("/add-wn-card", data=data, follow_redirects=True)

def post_set_wn_cards(client, cards):
    data = {}
    for idx, card in enumerate(cards):
        data["cards-"+str(idx)] = str(card["_id"])
    return client.post("/set-wn-cards", data=data, follow_redirects=True)
