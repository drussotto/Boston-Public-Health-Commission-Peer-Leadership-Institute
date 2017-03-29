from flask import request, redirect, render_template, abort
from blog_db import get_page_to_delete, remove_document
from flask_login import current_user

import urllib

def _remove_blog_page_get():
    return render_template("remove_user_content.html")

def _remove_blog_page_post():
    page_str = request.args.get("page")
    page = get_page_to_delete(page_str)
    if page is not None:
        remove_document(page["_id"])
        return render_template("redir_success.html")
    elif not current_user.is_authenticated:
        # Hax to redirect user to login
        return redirect("/login?"+urllib.urlencode({"next": "/uc/remove?page="+str(page_str)}))
    else:
        return abort(403)

def remove_blog_page():
    if request.method == "GET":
        return _remove_blog_page_get()
    else:
        return _remove_blog_page_post()
