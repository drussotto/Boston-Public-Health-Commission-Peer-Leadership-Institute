from flask import request, render_template, redirect
from flask_login import current_user
from new_blog_page_form import AddBlogPageForm
from pli.images import add_new_img
from util import build_file_list, dict_from_page_form

import mimetypes
from blog_db import add_new_document

# Performs the actual addition to the DB
def _post_add_page():
    form = AddBlogPageForm(request.form)
    if form.validate():
        new_id = add_new_document(dict_from_page_form(form))
        return redirect("/blog/show?id="+str(new_id))
    else:
        return render_template("blog_new_post.html", form=form)


# Just render the editor page.
def _get_add_page():
    return render_template("blog_new_post.html")

# Endpoint to add an actual user content page
# accepts POST and GET
def add_blog_page():
    if request.method == "POST":
        return _post_add_page()
    else:
        return _get_add_page()
