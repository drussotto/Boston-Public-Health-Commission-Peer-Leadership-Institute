from wtforms import Form, StringField, IntegerField, BooleanField, HiddenField, FileField, validators
from wtforms.widgets import TextArea, CheckboxInput

class AddStaffForm(Form):
    name = StringField('Staff Name', [validators.DataRequired()])
    title = StringField('Title', [validators.DataRequired()])
    bio = StringField('Bio', [validators.DataRequired()], widget=TextArea())
    email = StringField('Email (optional)')
    phone = StringField('Phone (optional)')
    picture = FileField("Picture")
    active = BooleanField('Active', widget=CheckboxInput())
    order = HiddenField('Order')

class EditStaffForm(Form):
    edit_name = StringField('Name')
    edit_title = StringField('Title')
    edit_bio = StringField('Bio', widget=TextArea())
    edit_email = StringField('Email (optional)')
    edit_phone = StringField('Phone (optional)')
    edit_picture = FileField("Picture")
    edit_active = BooleanField('Active', widget=CheckboxInput())
    edit_order = HiddenField('Order')

def edit_form_to_dict(req) :
    o = {}
    if 'edit_name' in req:
        o['name'] = req['edit_name']
    if 'edit_title' in req:
        o['title'] = req['edit_title']
    if 'edit_bio' in req:
        o['bio'] = req['edit_bio']
    if 'edit_email' in req:
        o['email'] = req['edit_email']
    if 'edit_phone' in req:
        o['phone'] = req['edit_phone']
    if 'edit_active' in req:
        o['active'] = as_bool(req['edit_active'])
    else:
        o['active'] = False
    if 'edit_order' in req:
        o['order'] = req['edit_order']
    return o

def as_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        return bool(s)
