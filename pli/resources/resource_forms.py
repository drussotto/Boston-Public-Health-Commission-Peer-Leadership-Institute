from wtforms import Form, StringField, IntegerField, validators, BooleanField

class AddResourceForm(Form):
    link = StringField('link', [validators.DataRequired()])
    name = StringField('name', [validators.DataRequired()])
    category = StringField('category', [validators.DataRequired()])
    rtype = StringField('rtype', [validators.DataRequired()])
    active = BooleanField('active', [validators.DataRequired()])
