from flask import request, render_template

def _view_my_pages_get():
    return render_template("my_pages.html")

def view_my_pages():
    if request.method == "GET":
        return _view_my_pages_get()
    else:
        return "", 500 # TODO lol
    
