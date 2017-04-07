from wtforms import Form, PasswordField, HiddenField, validators

class ResetPasswordForm(Form):
    reset_new_password = PasswordField('New Password', [
        validators.DataRequired("Password is required."),
        validators.Length(min=8, max=64, message="New password must be between %(min)s and %(max)s characters."),
        validators.EqualTo("reset_confirm_password", message="New password confirmation does not match.")
    ])
    reset_confirm_password = PasswordField('Confirm Password')
    reset_token = HiddenField("token", [
        validators.DataRequired("Missing token. Reload this page by clicking the link in your password reset email.")
    ])

