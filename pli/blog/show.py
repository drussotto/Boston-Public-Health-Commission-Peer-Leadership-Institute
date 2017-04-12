from flask import request, render_template, abort, redirect
from flask_login import current_user
from blog_db import get_page_to_view, get_page_with_id, check_blog_permissions
import urllib

# Endpoint to get the page whose id is provided as a query argument under the name
# "page". Enforces viewing permissions by redirecting if the user is not logged in, or
# gives 403 if they can't view.
def show_blog_page():
    page_id = request.args.get("id")

    page = get_page_with_id(page_id)
    # No page (bad id) => redirect to blog home page
    if page is None:
        return redirect("/blog")
    # Check if allowed to view page
    valid_page = check_blog_permissions(page)
    if valid_page is not None:
        return render_template("blog_post.html", page=page)
    elif not current_user.is_authenticated:
        # redirect user to login to try again
        return redirect("/login?"+urllib.urlencode({"next": "/blog/show?id="+str(page_id)}))
    else:
        return abort(403) # not authorized
