from flask import current_app, send_file, request
from pli import get_db
from bson import ObjectId
from pli.service_util import get_gridfs, get_db
from pli.images import add_new_img, get_img_file
class CarouselCard(object):

    def __init__(self, db_doc):
        # Read our attributes out of the database document
        self.bg = db_doc["background"]
        self.caption = db_doc["caption"]
        self.sub_caption = db_doc["sub_caption"]
        self.hyperlink = db_doc["hyperlink"]

    # Loads the card with the given card_id
    @classmethod
    def load(cls, card_id):
        card = get_db().cards.find_one({"_id": card_id})
        if card is None:
            return None
        return cls(card)

    # Returns a send_file response with the data
    # from the cards background image
    @classmethod
    def send_picture(cls, card_id):
        if not isinstance(card_id, ObjectId):
            card_id = ObjectId(card_id)
        file_obj, content_type = get_img_file(card_id)
        # No picture => 404
        if file_obj is None:
            return "", 404
        return send_file(file_obj, mimetype=content_type)

    @classmethod
    def new_card(cls, doc):
        bg_file = add_new_img(request.files["background"], "image/png")
        doc["background"] = bg_file
        return cls(doc)

    def get_bg(self):
        return str(self.bg)

    def get_caption(self):
        return self.caption

    def get_sub_caption(self):
        return self.sub_caption

    def get_hyperlink(self):
        return self.hyperlink

    def _as_db_doc(self):
        return {
            "background": self.get_bg(),
            "caption": self.get_caption(),
            "sub_caption": self.get_sub_caption(),
            "hyperlink": self.get_hyperlink()
        }

    # Saves this Carousel card to the mongo db, returns the ObjectId
    # of the created document
    def save_to_db(self):
        # inserted_id is the ObjectId of the newly-inserted document
        result = get_db().cards.insert_one(self._as_db_doc())
        self.store_card_id(result)
        return str(result.inserted_id)

def list_cards():
    return list(get_db().cards.find({}))

def card_exists(cid):
    return get_db().cards.find_one({"_id": cid}) is not None
