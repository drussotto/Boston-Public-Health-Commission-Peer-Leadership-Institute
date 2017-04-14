from flask import request, redirect, render_template, abort
from blog_db import get_page_to_delete, remove_document
from flask_login import current_user

import urllib

def remove_blog_page():
    page_id = request.args.get("id")
    page = get_page_to_delete(page_id)
    if page is not None:
        remove_document(page["_id"])
        return "", 200
    elif not current_user.is_authenticated:
        # Hax to redirect user to login
        return redirect("/login?"+urllib.urlencode({"next": "/blog/remove?id="+str(page_id)}))
    else:
        return abort(403)
