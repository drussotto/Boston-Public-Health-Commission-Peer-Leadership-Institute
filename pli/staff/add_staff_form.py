from wtforms import Form, StringField, IntegerField, BooleanField, validators
from wtforms.widgets import TextArea, CheckboxInput

class AddStaffForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    title = StringField('Title', [validators.DataRequired()])
    bio = StringField('Bio', [validators.DataRequired()], widget=TextArea())
    email = StringField('Email', [validators.Email()])
    phone = StringField('Phone')
    active = BooleanField('Are they active?', widget=CheckboxInput())
    # picture = file field.
