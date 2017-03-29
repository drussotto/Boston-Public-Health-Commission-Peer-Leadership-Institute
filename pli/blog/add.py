from flask import request, render_template, redirect
from flask_login import current_user
from new_blog_page_form import AddBlogPageForm
from pli.images import add_new_img
from util import build_file_list, dict_from_page_form

import mimetypes
import blog_db

# Performs the actual addition to the DB
def _post_add_page():
    form = AddBlogPageForm(request.form)
    if form.validate():
        new_doc = dict_from_page_form(form)
        
        # Now that we've made the new doc
        # we can add it
        new_id = blog_db.add_new_document(new_doc)
        return redirect("/uc/show?page="+str(new_id))
    else:
        return abort(400)


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
