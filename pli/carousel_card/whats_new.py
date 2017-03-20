from flask import render_template, request
from wn_card_form import WnCardInfoAddForm
from card import CarouselCard, card_exists
from set_wn_cards_form import SetWnCardsForm
from pli.service_util import get_db, get_obj_id

class WhatsNewCard(CarouselCard):

    def __init__(self, db_doc):
        super(WhatsNewCard, self).__init__(db_doc)
        if "_id" in db_doc:
            self.str_id = str(db_doc["_id"])

    @classmethod
    def store_card_id(cls, obj_id):
        get_db().whatsnew.update_one({},
                                     {"$addToSet" : {"cards": obj_id}})

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
    
    @classmethod
    def list_wn_cards(cls):
        ids = get_db().whatsnew.find_one({})
        if ids is None or ("cards" not in ids):
            # Not in the db, most likely a local instance
            return []

        return map(WhatsNewCard.load, ids["cards"])

def add_wn_card():
    form = WnCardInfoAddForm(request.form)
    if request.method == "POST":
        if form.validate():
            card = WhatsNewCard.new_card(form.extract())
            obj_id = card.save_to_db()
            card.str_id = str(obj_id)
            return render_template('redir_success.html')
        else:
            return "",400
    else:
        return render_template('add_wn_card.html', form=form)

def set_wn_cards():
    form = SetWnCardsForm(request.form)
    new_wn_list = []
    if request.method == "POST":
        if form.validate():
            for id_field in form.cards.data:
                if len(str(id_field)) == 0:
                    continue
                try:
                    oid = get_obj_id()(str(id_field))
                except Exception, e:
                    return "", 400
                
                if not card_exists(oid):
                    return "", 400
                new_wn_list.append(oid)
                get_db().whatsnew.update({}, {"$set": { "show" : new_wn_list }})
            return render_template('redir_success.html')
        else:
            return "", 400
    return render_template("set_wn_cards.html", form=form)
