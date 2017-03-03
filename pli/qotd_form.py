from wtforms import Form, StringField, PasswordField, validators

class QotdSubmissionForm(Form):
    answer = StringField('Answer', [validators.DataRequired()])
