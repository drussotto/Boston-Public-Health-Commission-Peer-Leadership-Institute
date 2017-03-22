from wtforms import Form, StringField, IntegerField, validators

class RoleInfoForm(Form):
    user = IntegerField('uid', [validators.DataRequired()])
    role = StringField('role', [validators.DataRequired()])
