from flask import request, abort, url_for, render_template
from add_staff_form import AddStaffForm
from staff_db import add_new_staff

def _get_add_staff():
    form = AddStaffForm()
    return render_template('add_staff.html', form=form)

def _add_pic_with_default_photo(obj):
    f = request.files.get('picture', None)
    obj_id = None
    if f:
        obj_id = get_gridfs().put(f)
    obj["picture"] = obj_id

def _post_add_staff():
    form = AddStaffForm(request.form)
    if form.validate():
        obj = request.form.to_dict()
        obj["active"] = form.active.data
        _add_pic_with_default_photo(obj)
        add_new_staff(obj, pic)
        return render_template('staff.html')
    else:
        return abort(400)

def add_staff():
    if request.method == "GET":
        return _get_add_staff()
    else:
        return _post_add_staff()
