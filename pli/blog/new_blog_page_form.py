from wtforms import Form, StringField, HiddenField, validators

class AddBlogPageForm(Form):
    title = StringField("title", [validators.DataRequired("Title is Required")])
    body = StringField("body", [validators.DataRequired("Body is Required")])
    required_role = HiddenField("role", [validators.DataRequired()])

class EditBlogPageForm(Form):
    edit_title = StringField("title")
    edit_body = StringField("body")
    edit_required_role = HiddenField("role")