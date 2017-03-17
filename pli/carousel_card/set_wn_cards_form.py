from wtforms import Form, StringField, IntegerField, validators, FieldList

class SetWnCardsForm(Form):
    cards = FieldList(StringField("ids"), min_entries=3)
