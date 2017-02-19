from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])

    # Returns this form as a login-tuple (email, password).
    # If hash_fun is provided, will return (email, hash_fun(password))
    def as_args(self, hash_fun=None):
        return email, password if hash_fun is None else hash_fun(password)
