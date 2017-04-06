from flask import request, abort, url_for, render_template, redirect
from staff_form import AddStaffForm
from staff_db import add_new_staff
from pli import get_gridfs

def _post_add_staff():
    form = AddStaffForm(request.form)
    if form.validate():
        obj = request.form.to_dict()
        obj["active"] = form.active.data
        add_new_staff(obj, request.files.get('picture', None))
        return redirect("/manage/staff")
    else:
        return abort(400)

def add_staff():
    return _post_add_staff()
