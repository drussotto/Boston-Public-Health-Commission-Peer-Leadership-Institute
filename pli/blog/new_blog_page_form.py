from wtforms import Form, StringField, IntegerField, validators, FieldList, BooleanField

class AddBlogPageForm(Form):
    title = StringField("title")
    body = StringField("body")
    requiredPerms = FieldList(StringField("perms"))
