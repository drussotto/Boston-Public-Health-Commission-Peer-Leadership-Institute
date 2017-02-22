from wtforms import Form, StringField, PasswordField, validators

class PliRegistrationForm(Form):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])
    # TODO organization

    # Converts this form into a mongo document representing the
    # user being registered. The _id field should be set to the next
    # open UID
    def as_mongo_doc(self):
        pass
