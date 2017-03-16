
from wtforms import StringField, IntegerField, validators, Form, FileField

class WnCardInfoAddForm(Form):
    background = FileField("background")
    caption = StringField('Caption')
    sub_caption = StringField('Sub-caption')
    hyperlink = StringField('Link to')

    def extract(self):
        return {
            "background": self.background,
            "caption": self.caption.data,
            "sub_caption": self.sub_caption.data,
            "hyperlink": self.hyperlink.data
        }
