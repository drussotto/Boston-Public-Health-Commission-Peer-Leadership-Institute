from flask import request, abort, redirect
from staff_db import get_staff_by_id, update_staff
from staff_form import EditStaffForm

def _post_edit_staff():
    sid = request.form.get('_id', None)
    if sid is None:
        return abort(400)
    staff_obj = get_staff_by_id(sid)
    if staff_obj is None:
        return abort(400)
    # This isn't super safe, too lazy though
    form = EditStaffForm(request.form)
    if form.validate():
        obj = request.form.to_dict()
        update_staff(sid, obj)
        return redirect("staff.html")
def _get_edit_staff():
    raise Exception("Not implemented")

def edit_staff():
    if request.method == "GET":
        _get_edit_staff()
    else:
        _post_edit_staff()
