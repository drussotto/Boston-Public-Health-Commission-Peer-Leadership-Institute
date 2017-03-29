from flask import request, render_template
from flask_login import current_user
from new_blog_page_form import AddBlogPageForm
from pli.images import add_new_img
import mimetypes
import blog_db

# Performs the actual addition to the DB
def _post_add_page():
    form = AddBlogPageForm(request.form)
    if form.validate():
        new_doc = {
            "title": form.title.data,
            "body" : form.body.data,
            # Owner is the current user (the one making it)
            "owner": current_user.get_id(),
            "required_roles": form.requiredPerms.data,
            # Construct the attachments from the form attachments
            "attachments": _build_file_list(request.files)
        }
        # Now that we've made the new doc
        # we can add it
        blog_db.add_new_document(new_doc)
        return render_template("redir_success.html")
    else:
        return "", 400

# Constructs a list of ObjectIds for the files in the current request
def _build_file_list(files):
    output = []
    # For all the files they add, we add them to gridfs
    # and include the objectid
    for name in files:
        mtype = mimetypes.guess_type(name)
        output.append({name: add_new_img(files[name], mtype)})
    return output

# Just render the editor page.
def _get_add_page():
    return render_template("editor.html")

# Endpoint to add an actual user content page
# accepts POST and GET
def add_blog_page():
    if request.method == "POST":
        return _post_add_page()
    else:
        return _get_add_page()
