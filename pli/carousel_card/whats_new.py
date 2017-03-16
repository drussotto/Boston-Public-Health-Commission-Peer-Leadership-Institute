from flask import render_template, request
from wn_card_form import WnCardInfoAddForm
from card import CarouselCard, card_exists
from set_wn_cards_form import SetWnCardsForm
from pli.service_util import get_db
from bson import ObjectId

class WhatsNewCard(CarouselCard):

    def __init__(self, db_doc):
        super(WhatsNewCard, self).__init__(db_doc)

    @classmethod
    def get_frontpage_cards(cls):
        # Only one doc in this collection
        # It has a list of card ids under
        # its "show" field.
        ids = get_db().whatsnew.find_one({})
        if ids is None or ("show" not in ids):
            # Not in the db, most likely a local instance
            return []

        # Map the card loading over the ids
        return map(WhatsNewCard.load, ids["show"])

def add_wn_card():
    form = WnCardInfoAddForm(request.form)
    if request.method == "POST" and form.validate():
        card = WhatsNewCard.new_card(form.extract())
        obj_id = card.save_to_db()
        return str(obj_id)
    return render_template('index.html')

def set_wn_cards():
    form = SetWnCardsForm()
    new_wn_list = []
    if form.validate_on_submit():
        for id_field in form.cards.data:
            oid = ObjectId(str(id_field.data))
            if not card_exists(oid):
                return "", 400
            new_wn_list.append(oid)
        get_db().whatsnew.update({}, {"$set": { "show" : new_wn_list }})
        return "",200
    return "", 400
