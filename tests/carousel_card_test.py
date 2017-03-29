import os
from testlib import *
from pli.service_util import get_db, get_gridfs, get_obj_id
from flask import current_app
from pli import list_cards

class CardImg(PliEntireDbTestCase):
    @with_test_client
    def test_card_image_from_url(self, client):
        res = client.get('/card-img/' + str(ex.wn_card0["background"]))
        with open(os.path.join(os.path.dirname(__file__), "testlib", "examples", "res", "mongodb.png"), "r") as img:
          self.assertEquals(res.data, img.read()) # not the correct way to compare image data from response

    @with_test_client
    def test_card_image_from_url_invalid_id(self, client):
        res = client.get('/card-image/DEADBEEFBEEF')
        self.assertEqual(404, res.status_code)

    @with_test_client
    def test_card_image_from_url_invalid_id_short(self, client):
        res = client.get('/card-image/DEADBEEF')
        self.assertEqual(404, res.status_code)

class CardList(PliEntireDbTestCase):
    @with_test_client
    def test_list_all_cards(self, client):
        cards = list_cards()
        self.assertEqual(len(cards), 3)
        self.assertTrue(ex.wn_card0 in cards)
        self.assertTrue(ex.wn_card1 in cards)
        self.assertTrue(ex.wn_card2 in cards)
