from flask import request, abort, redirect, render_template
from staff_db import get_staff_by_id, update_staff
from staff_form import EditStaffForm, form_to_dict

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
        update_staff(sid, form_to_dict(request.form))
        return redirect("/page/staff.html")
    return abort(400)

def _get_edit_staff():
    form = EditStaffForm()
    return render_template('staff_edit.html', form=form)

def edit_staff():
    if request.method == "GET":
        return _get_edit_staff()
    else:
        return _post_edit_staff()
