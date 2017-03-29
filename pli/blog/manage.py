from flask import request, render_template, jsonify
from blog_db import get_page_to_edit

def _view_my_pages_get():
    return render_template("my_pages.html")

def view_my_pages():
    if request.method == "GET":
        return _view_my_pages_get()
    else:
        return "", 500 # TODO lol

def get_page_dict():
    pg = get_page_to_edit(request.args.get("page"))
    if pg is not None:
        del pg["_id"]
    return jsonify(pg)
