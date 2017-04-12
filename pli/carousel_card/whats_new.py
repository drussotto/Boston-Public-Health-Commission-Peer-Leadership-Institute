from flask import redirect
from flask import render_template, request
from wn_card_form import WnCardInfoAddForm
from card import CarouselCard, card_exists
from set_wn_cards_form import SetWnCardsForm
from pli.service_util import get_db, get_obj_id

'''
Backend code for carousel on front page of website
'''
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


# Render forms for adding and setting cards
def manage_whats_new():
    add_form = WnCardInfoAddForm(request.form)
    set_form = SetWnCardsForm(request.form)
    active_card_ids = map(lambda card: card.str_id, WhatsNewCard.get_frontpage_cards())
    return render_template('slideshow_manage.html',
                           add_form=add_form,
                           set_form=set_form,
                           success=request.args.get('success', ''),
                           active_card_ids=active_card_ids)


# Handle API call for adding card
def add_wn_card():
    form = WnCardInfoAddForm(request.form)
    if request.method == "POST":
        if form.validate():
            card = WhatsNewCard.new_card(form.extract())
            obj_id = card.save_to_db()
            card.str_id = str(obj_id)
            return redirect('/manage/slideshow?success=yes')
        else:
            return redirect('/manage/slideshow?success=no')
    else:
        return "", 405


# Handle API call for setting card
def set_wn_cards():
    # form = SetWnCardsForm(request.form)
    new_wn_list = []
    data = request.get_json()
    ids = data['ids']
    if request.method == "POST":
        for id_field in ids:
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
        return "", 200
    else:
        return "", 405
