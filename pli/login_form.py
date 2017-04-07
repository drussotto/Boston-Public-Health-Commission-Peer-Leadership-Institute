from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

    # Returns this form as a login-tuple (email, password).
    def as_args(self):
        return self.email.data, self.password.data

def get_login_form():
  return LoginForm();