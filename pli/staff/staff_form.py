from wtforms import Form, StringField, IntegerField, BooleanField, validators
from wtforms.widgets import TextArea, CheckboxInput

class AddStaffForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    title = StringField('Title', [validators.DataRequired()])
    bio = StringField('Bio', [validators.DataRequired()], widget=TextArea())
    email = StringField('Email')
    phone = StringField('Phone')
    active = BooleanField('Are they active?', widget=CheckboxInput())
    # picture = file field.


class EditStaffForm(Form):
    name = StringField('Name')
    title = StringField('Title')
    bio = StringField('Bio', widget=TextArea())
    email = StringField('Email')
    phone = StringField('Phone')
    active = BooleanField('Are they active?', widget=CheckboxInput())
    # picture = file field.
