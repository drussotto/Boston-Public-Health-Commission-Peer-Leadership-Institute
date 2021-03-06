import os
from testlib import *
from pli.service_util import get_db, get_gridfs
from bson import ObjectId
from flask import current_app
from pli.carousel_card import WhatsNewCard

class WnDisplay(PliEntireDbTestCase):

    @with_test_client
    def test_displaying_cards(self, client):
        index = client.get('/')
        assert_index_page(self, index)
        for card in ex.show_list:
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

    @with_login(user2["email_address"], user2["real_pass"])
    def test_add_wn_card_noauth(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_add_wn_card_not_logged_in(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(200, res.status_code)
        
    @with_login(user2["email_address"], user2["real_pass"])
    def test_display_add_wn_card_noauth(self, client):
        res = client.get('/manage/slideshow')
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_display_add_wn_card_not_logged_in(self, client):
        res = client.get('/manage/slideshow')
        self.assertEqual(302, res.status_code)
        
    @with_login(user1["email_address"], user1["real_pass"])
    def test_invalid_add_wn_card_form(self, client):
        res = client.post("/add-wn-card", data={})
        self.assertEqual(400, res.status_code)


class WnSet(PliEntireDbTestCase):

    @with_login(user1["email_address"], user1["real_pass"])
    def test_set_wn_card_empty(self, client):
        res = post_set_wn_cards(client, [])
        self.assertEqual(400, res.status_code)
        third_party = current_app.test_client()

        get_db().whatsnew.update({}, {"$set":{"show":[], "cards":[]}})
        index = third_party.get('/')
        assert_index_page(self, index)
        self.assertTrue("no news" in index.data)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_set_wn_card_noauth(self, client):
        res = post_set_wn_cards(client, [ex.wn_card1, ex.wn_card0, ex.wn_card2])
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_set_wn_card_not_logged_in(self, client):
        res = post_set_wn_cards(client, [ex.wn_card0, ex.wn_card2, ex.wn_card1])
        self.assertEqual(200, res.status_code)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_display_set_wn_card_noauth(self, client):
        res = client.post('/set-wn-cards')
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_display_set_wn_card_not_logged_in(self, client):
        res = client.post('/set-wn-cards')
        self.assertEqual(302, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_invalid_set_wn_card_form(self, client):
        res = client.post("/set-wn-cards", data={}, follow_redirects=True)
        self.assertEqual(400, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_set_wn_card_does_not_exist(self, client):
        res = post_set_wn_cards(client, [{ "_id" : "DEADBEEF" }])
        self.assertEqual(400, res.status_code)


class WnList(PliEntireDbTestCase):
    @with_app_ctxt
    def test_displaying_cards(self):
        cards = WhatsNewCard.list_wn_cards()
        self.assertEqual(len(cards), 3)
        for card in cards:
            self.assertTrue(card.str_id == str(ex.wn_card0["_id"]) or
                            card.str_id == str(ex.wn_card1["_id"]) or
                            card.str_id == str(ex.wn_card2["_id"]))


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
