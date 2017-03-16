<<<<<<< HEAD
from wtforms import StringField, IntegerField, validators, Form, FileField

class WnCardInfoAddForm(Form):
    background = FileField("Background Image")
    caption = StringField('Image caption')
    sub_caption = StringField('Image sub-caption')
    hyperlink = StringField('Link')

    def extract(self):
        return {
=======

from wtforms import StringField, IntegerField, validators, Form, FileField

class WnCardInfoAddForm(Form):
    background = FileField("Background Image")
    caption = StringField('Image caption')
    sub_caption = StringField('Image sub-caption')
    hyperlink = StringField('Link')

    def extract(self):
        return {
            "background": self.background,
>>>>>>> fb0b451... Cards are rendered mock stuff is a little wonkey
            "caption": self.caption.data,
            "sub_caption": self.sub_caption.data,
            "hyperlink": self.hyperlink.data
        }
