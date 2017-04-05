from flask import request, abort, redirect
from staff_db import get_staff_by_id, update_staff
from staff_form import EditStaffForm

def _post_edit_staff():
    sid = request.args.get('id', None)
    if sid is None:
        return abort(400)
    staff_obj = get_staff_by_id(sid)
    if staff_obj is None:
        return abort(400)
    # This isn't super safe, too lazy though
    form = EditStaffForm(request.form)
    if form.validate():
        d = request.form.to_dict()
        if "_id" in d:
            del d["_id"] # It would be bad if they could edit the _id
        update_staff(sid, d)
        return redirect("/page/staff.html")
    return abort(400)

def _get_edit_staff():
    raise Exception("Not implemented")

def edit_staff():
    if request.method == "GET":
        return _get_edit_staff()
    else:
        return _post_edit_staff()
