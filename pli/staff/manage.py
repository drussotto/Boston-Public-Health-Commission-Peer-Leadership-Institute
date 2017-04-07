from flask import request, abort, url_for, render_template
from staff_form import AddStaffForm, EditStaffForm

def _get_manage_staff():
  add_form = AddStaffForm()
  edit_form = EditStaffForm()
  return render_template('staff_manage.html', add_form=add_form, edit_form=edit_form)

def manage_staff():
    return _get_manage_staff()