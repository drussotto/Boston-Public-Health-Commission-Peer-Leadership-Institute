from wtforms import Form, StringField, HiddenField, validators

class AddBlogPageForm(Form):
    title = StringField("title", [validators.DataRequired("required")])
    body = StringField("body", [validators.DataRequired("required")])
    required_role = HiddenField("role", filters = [lambda role: role or None])