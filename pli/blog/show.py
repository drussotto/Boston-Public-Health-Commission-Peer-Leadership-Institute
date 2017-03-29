from flask import request, render_template, abort, redirect
from flask_login import current_user
from blog_db import get_page_to_view
import urllib

# Endpoint to get the page whose id is provided as a query argument under the name
# "page". Enforces viewing permissions by redirecting if the user is not logged in, or
# gives 403 if they can't view.
def show_blog_page():
    page_str = request.args.get("page")
    page = get_page_to_view(page_str)
    if page:
        return render_template("user_content.html",
                               page=page)
    elif not current_user.is_authenticated:
        # Hax to redirect user to login
        return redirect("/login?"+urllib.urlencode({"next": "/uc/show?page="+str(page_str)}))
    else:
        return abort(403)
