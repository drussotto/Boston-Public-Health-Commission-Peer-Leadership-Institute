from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, validators, FieldList

class SetWnCardsForm(FlaskForm):
    cards = FieldList(StringField("ObjIds"), min_entries=1)
