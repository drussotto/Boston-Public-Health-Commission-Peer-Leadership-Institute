
import mongomock
from mongomock import ObjectId
import os
from mongomock import gridfs
from pli.service_util import get_db

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
    db.whatsnew.insert({"show" : map((lambda x: x["_id"]), show_list),
                        "cards": map((lambda x: x["_id"]), [wn_card0, wn_card1, wn_card2])})

    ex.add(wn_card0=wn_card0,
           wn_card1=wn_card1,
           wn_card2=wn_card2,
           show_list=show_list)


def add_mocked_wn_cards(db):
    build_and_assign_cards(db, gridfs.MockGridFS(db))
