from wtforms import Form, StringField, PasswordField, validators
from passwords import gen_hash

class PliRegistrationForm(Form):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])
    # TODO organization

    # Converts this form into a mongo document representing the
    # user being registered. (No _id yet)
    def as_mongo_doc(self):
        return {
            "first_name":self.first_name.data,
            "last_name":self.last_name.data,
            "email_address":self.email.data,
            "password": gen_hash(self.password.data)
        }
