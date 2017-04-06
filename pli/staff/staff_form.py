from wtforms import Form, StringField, IntegerField, BooleanField, validators
from wtforms.widgets import TextArea, CheckboxInput

class AddStaffForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    title = StringField('Title', [validators.DataRequired()])
    bio = StringField('Bio', [validators.DataRequired()], widget=TextArea())
    email = StringField('Email')
    phone = StringField('Phone')
    active = BooleanField('Are they active?', widget=CheckboxInput())
    order = IntegerField('Order')
    # picture = file field.

class EditStaffForm(Form):
    name = StringField('Name')
    title = StringField('Title')
    bio = StringField('Bio', widget=TextArea())
    email = StringField('Email')
    phone = StringField('Phone')
    active = BooleanField('Are they active?', widget=CheckboxInput())
    order = IntegerField('Order')
    # picture = file field.

def form_to_dict(req) :
    o = {}
    if 'name' in req:
        o['name'] = req['name']
    if 'title' in req:
        o['title'] = req['title']
    if 'bio' in req:
        o['bio'] = req['bio']
    if 'email' in req:
        o['email'] = req['email']
    if 'phone' in req:
        o['phone'] = req['phone']
    if 'active' in req:
        o['active'] = as_bool(req['active'])
    if 'order' in req:
        o['order'] = req['order']
    return o

def as_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise Exception("Not a boolean literal")
