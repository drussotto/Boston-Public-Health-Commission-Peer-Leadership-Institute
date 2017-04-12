from wtforms import StringField, IntegerField, validators, Form, FileField, validators

class WnCardInfoAddForm(Form):
    background = FileField("Background Image")
    caption = StringField('Image caption')
    sub_caption = StringField('Image sub-caption')
    hyperlink = StringField('Link')

    def extract(self):
        return {
            "caption": self.caption.data,
            "sub_caption": self.sub_caption.data,
            "hyperlink": self.hyperlink.data
        }
