from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])

    # Returns this form as a login-tuple (email, password).
    def as_args(self):
        return self.email.data, self.password.data
