from flask import request
from flask_login import current_user

# Constructs a list of ObjectIds for the files in the current request
def build_file_list(files):
    output = []
    # For all the files they add, we add them to gridfs
    # and include the objectid
    for name in files:
        mtype = mimetypes.guess_type(name)
        output.append({name: add_new_img(files[name], mtype)})
    return output

# Dict from page form.
def dict_from_add_page_form(form):
    return {
        "title": form.title.data,
        "body" : form.body.data,
        # Owner is the current user (the one making it)
        "owner": current_user.get_id(),
        "required_role": form.required_role.data,
        # Construct the attachments from the form attachments
        "attachments": build_file_list(request.files)
    }

# Dict from page form.
def dict_from_edit_page_form(form):
    return {
        "title": form.edit_title.data,
        "body" : form.edit_body.data,
        # Owner is the current user (the one making it)
        "owner": current_user.get_id(),
        "required_role": form.edit_required_role.data,
        # Construct the attachments from the form attachments
        "attachments": build_file_list(request.files)
    }
