from flask import request, abort, redirect, render_template, jsonify, url_for
from staff_db import get_staff_by_id, update_staff, update_staff_order
from staff_form import EditStaffForm, edit_form_to_dict

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
        update_staff(sid, edit_form_to_dict(request.form))
        if request.is_xhr:
            return "", 200
        else:
            return redirect("/manage/staff")
    return abort(400)

def _post_edit_staff_order():
    data = request.get_json()
    ids = data["ids"]
    if ids is None:
        return abort(400)
    update_staff_order(ids)
    return "", 200

def edit_staff():
    return _post_edit_staff()

def edit_staff_order():
    return _post_edit_staff_order()

def get_staff_info():
    staff_id = request.args.get('id')
    info = get_staff_by_id(staff_id)
    if info is not None:
        del info["_id"]
        if info["picture"]:
            info["picture"] = '/card-img/' + str(info["picture"])
        else:
            info["picture"] = url_for('static', filename='images/no_image_staff.jpg')
        return jsonify(info)
    else:
        return abort(403)