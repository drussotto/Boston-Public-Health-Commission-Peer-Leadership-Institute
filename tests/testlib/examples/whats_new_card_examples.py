
import mongomock
import os
from mongomock import gridfs
from bson import ObjectId
<<<<<<< HEAD
from pli.service_util import get_db
=======
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey

def get_image_bytes(file_name):
    path = os.path.join(os.path.dirname(__file__), "res", file_name)
    return open(path, "r")

wn_card0 = None
wn_card0 = None
wn_card0 = None
show_list = None

def build_and_assign_cards(db, gridfs):
    global wn_card0, wn_card1, wn_card2, show_list

    wn_card0 = {
        "_id": ObjectId(),
        "background": gridfs.put(get_image_bytes("mongodb.png"), content_type="image/png"),
        "caption": "This is in mongo",
        "sub_caption": "This is the sub-caption",
        "hyperlink": "example.com"
    }
    wn_card1 = {
        "_id": ObjectId(),
        "background": gridfs.put(get_image_bytes("FlaskLogo.png"), content_type="image/png"),
        "caption": "This is a flask app",
        "sub_caption": "Flask is cool.",
        "hyperlink": "example.com"
    }
    wn_card2 = {
        "_id": ObjectId(),
        "background": gridfs.put(get_image_bytes("stack-overflow.png"), content_type="image/png"),
        "caption": "Powered by stack-overflow",
        "sub_caption": "Teaching me how to do css",
        "hyperlink": "example.com"
    }

    show_list = [wn_card1, wn_card2]
    db.cards.insert_many([wn_card0, wn_card1, wn_card2])
    db.whatsnew.insert({"show" : map((lambda x: x["_id"]), show_list) })


def add_mocked_wn_cards(db):
    build_and_assign_cards(db, gridfs.MockGridFS(db))

<<<<<<< HEAD
def _card_from_id(others, id):
    return others + [get_db().cards.find_one({"_id": id})]
    
def get_show_list():
    return reduce(_card_from_id, get_db().whatsnew.find_one({})["show"], [])

def get_wn_card0():
    return wn_card0

def get_wn_card1():
    return wn_card1

def get_wn_card2():
    return wn_card2
=======
def get_show_list():
    return show_list
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey
