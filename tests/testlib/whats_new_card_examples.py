import mongomock
import os
import gridfs
#from bson.objectid import ObjectId

def get_image_bytes(file_name):
    path = os.path.join(os.path.dirname(__file__), "res", file_name)
    return open(path, "r")

wn_card0 = None

def build_and_assign_cards(db, gridfs):
    global wn_card0
    wn_card0 = {
        "background": gridfs.put(get_image_bytes("mongodb.png")),
        "caption": "This is in mongo",
        "sub_caption": "This is the sub-caption"
    }

def add_mocked_wn_cards(db):
    build_and_assign_cards(db, gridfs.GridFS(db))
    
    
