from flask import request, render_template, abort, redirect
from flask_login import current_user
from blog_db import get_page_with_id, is_allowed_to_view
import urllib


def show_blog_page():
    try:
        page_str = request.args.get("page")
        if is_allowed_to_view(page_str):
            page = get_page_with_id(page_str)
            return render_template("user_content.html",
                                   page=page)
        elif not current_user.is_authenticated:
            return redirect("/login?"+urllib.urlencode({"next": "/uc/show?page="+str(page_str)}))
        else:
            return "", 403
    except Exception, e:
        print(e)
        return "", 400
