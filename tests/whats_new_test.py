import os
from testlib import *
from pli.service_util import get_db, get_gridfs
<<<<<<< HEAD
from bson import ObjectId
from flask import current_app 
from pli.carousel_card import WhatsNewCard

=======
from mongomock.object_id import ObjectId
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey
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

<<<<<<< HEAD
            
class WnAdd(PliEntireDbTestCase):
=======


>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey

    @with_login(user1["email_address"], user1["real_pass"])
    def test_add_wn_card(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(200, res.status_code)
        l = get_db().cards.find_one({"caption": "Caption"})
<<<<<<< HEAD
        self.assertTrue("Success" in res.data)
=======
        self.assertEqual(str(l["_id"]), res.data)
        bytez = get_gridfs().get(l["background"]).read()
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            self.assertEquals(bytez, f.read())
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey

    @with_login(user2["email_address"], user2["real_pass"])
    def test_add_wn_card_noauth(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(403, res.status_code)

<<<<<<< HEAD
    @with_test_client
    def test_add_wn_card_not_logged_in(self, client):
        with open(os.path.join(os.path.dirname(__file__), "res", "python-logo.png"), "r") as f:
            res = post_add_wn_card(client, f, "Caption", "Sub-caption", "http://test.example.com")
        self.assertEqual(403, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_display_add_wn_card(self, client):
        res = client.get('/add-wn-card')
        self.assertTrue("Add New" in res.data)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_display_add_wn_card_noauth(self, client):
        res = client.get('/add-wn-card')
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_display_add_wn_card_not_logged_in(self, client):
        res = client.get('/add-wn-card')
        self.assertEqual(403, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_invalid_add_wn_card_form(self, client):
        res = client.post("/add-wn-card", data={}, follow_redirects=True)
        self.assertEqual(400, res.status_code)


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

    @with_login(user1["email_address"], user1["real_pass"])
    def test_set_wn_card_empty(self, client):
        res = post_set_wn_cards(client, [])
        self.assertEqual(200, res.status_code)
        third_party = current_app.test_client()

        index = third_party.get('/')
        assert_index_page(self, index)
        self.assertTrue("No News" in res.data)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_set_wn_card_noauth(self, client):
        res = post_set_wn_cards(client, [get_wn_card1(), get_wn_card0(), get_wn_card2()])
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_set_wn_card_not_logged_in(self, client):
        res = post_set_wn_cards(client, [get_wn_card0(), get_wn_card2(), get_wn_card1()])
        self.assertEqual(403, res.status_code)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_display_set_wn_card(self, client):
        res = client.get('/set-wn-cards')
        self.assertTrue("Set Cards" in res.data)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_display_set_wn_card_noauth(self, client):
        res = client.get('/set-wn-cards')
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_display_set_wn_card_not_logged_in(self, client):
        res = client.get('/set-wn-cards')
        self.assertEqual(403, res.status_code)

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
        self.assertTrue(get_wn_card0() in cards)
        self.assertTrue(get_wn_card1() in cards)
        self.assertTrue(get_wn_card2() in cards)


=======
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey
def post_add_wn_card(client, f, caption, sub_caption, hyperlink):
    data = {
        "caption": caption,
        "sub_caption": sub_caption,
        "hyperlink": hyperlink,
        "background": f
    }
    return client.post("/add-wn-card", data=data, follow_redirects=True)
<<<<<<< HEAD

def post_set_wn_cards(client, cards):
    data = {}
    for idx, card in enumerate(cards):
        data["cards-"+str(idx)] = str(card["_id"])
    return client.post("/set-wn-cards", data=data, follow_redirects=True)
=======
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey
