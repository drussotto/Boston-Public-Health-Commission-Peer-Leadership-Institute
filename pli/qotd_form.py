from wtforms import Form, StringField, PasswordField, validators

class QotdSubmissionForm(Form):
    # Currently this is not used, but if we decided to use it in the future
    # we can
    qid = StringField('Question ID', [validators.DataRequired()])
    answer = StringField('Answer', [validators.DataRequired()])
