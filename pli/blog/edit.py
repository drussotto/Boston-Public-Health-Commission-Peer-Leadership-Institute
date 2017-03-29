from flask import request, abort, render_template, redirect

from blog_db import get_page_to_edit, update_document
from new_blog_page_form import AddBlogPageForm
from flask_login import current_user
from util import build_file_list, dict_from_page_form

# Commits a page edit for the page with the given id
def _edit_blog_page_post():
    page_str = request.args.get('page')
    page = get_page_to_edit(page_str)

    if page is None:
        return abort(403)

    form = AddBlogPageForm(request.form)
    if form.validate():
        new_doc = dict_from_page_form(form)
        # Now that we've made the new doc
        # we can add it
        update_document(page["_id"], new_doc)
        return redirect("/uc/show?page="+page_str)
    else:
        return abort(400)

# Returns the editting page for the page given
# as an id (performs user validation)
def _edit_blog_page_get():
    page_str = request.args.get('page')
    page = get_page_to_edit(page_str)
    if page is not None:
        return render_template("editor.html", edit=page_str)
    else:
        return abort(403)

# Endpoint for /uc/edit
def edit_blog_page():
    if request.method == "GET":
        return _edit_blog_page_get();
    else:
        return _edit_blog_page_post();
