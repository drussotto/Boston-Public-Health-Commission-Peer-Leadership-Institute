from flask import request, abort, render_template, redirect
from blog_db import get_page_to_edit, update_document
from new_blog_page_form import EditBlogPageForm
from flask_login import current_user
from util import build_file_list, dict_from_edit_page_form

# Commits a page edit for the page with the given id
def _edit_blog_page_post():
    page_id = request.args.get('id')
    page = get_page_to_edit(page_id)

    if page is None:
        return abort(403)

    form = EditBlogPageForm(request.form)
    if form.validate():
        update_document(page["_id"], dict_from_edit_page_form(form))
        return redirect("/blog/show?id="+page_id)
    else:
        return abort(400)

# Returns the editting page for the page given
# as an id (performs user validation)
def _edit_blog_page_get():
    page_id = request.args.get('id')
    page = get_page_to_edit(page_id)
    if page is not None:
        return render_template("blog_post_new.html", edit=page_id)
    else:
        return abort(403)

# Endpoint for /blog/edit
def edit_blog_page():
    if request.method == "GET":
        return _edit_blog_page_get();
    else:
        return _edit_blog_page_post();
