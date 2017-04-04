from flask import request, abort, url_for, render_template
from staff_form import AddStaffForm
from staff_db import add_new_staff
from pli import get_gridfs

def _get_add_staff():
    form = AddStaffForm()
    return render_template('add_staff.html', form=form)

def _post_add_staff():
    form = AddStaffForm(request.form)
    if form.validate():
        obj = request.form.to_dict()
        obj["active"] = form.active.data
        # None is the default, add_new_staff will handle None with the default picture.
        add_new_staff(obj, request.files.get('picture', None))
        return render_template('staff.html')
    else:
        return abort(400)

def add_staff():
    if request.method == "GET":
        return _get_add_staff()
    else:
        return _post_add_staff()
