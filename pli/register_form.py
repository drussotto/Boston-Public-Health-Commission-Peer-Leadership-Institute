from wtforms import Form, StringField, PasswordField, validators
from passwords import gen_hash

class PliRegistrationForm(Form):
    first_name = StringField('First Name', [
        validators.DataRequired("First name is required.")
    ])
    last_name = StringField('Last Name', [
        validators.DataRequired("Last name is required.")
    ])
    register_email = StringField('Email Address', [
        validators.DataRequired("Email is required."), 
        validators.Regexp('^[^@]+@[^@]+\.[^@]+$', 0, message="Invalid email."),
    ])
    register_password = PasswordField('Password', [
        validators.DataRequired("Password is required."),
        validators.EqualTo("register_confirm_password", message="Password confirmation does not match."),
        validators.Length(min=8, max=64, message="Password must be between %(min)s and %(max)s characters.")
    ])
    register_confirm_password = PasswordField('Confirm Password')

    # Converts this form into a mongo document representing the
    # user being registered. (No _id yet)
    def as_mongo_doc(self):
        return {
            "first_name":self.first_name.data,
            "last_name":self.last_name.data,
            "email_address":self.register_email.data,
            "password": gen_hash(self.register_password.data)
        }
