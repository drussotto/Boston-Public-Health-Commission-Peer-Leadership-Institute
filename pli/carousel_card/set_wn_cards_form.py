<<<<<<< HEAD
from wtforms import Form, StringField, IntegerField, validators, FieldList

class SetWnCardsForm(Form):
    cards = FieldList(StringField("ids"), min_entries=3)
=======
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, validators, FieldList

class SetWnCardsForm(FlaskForm):
    cards = FieldList(StringField("ObjIds"), min_entries=1)
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey
