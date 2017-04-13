from flask import request, abort
from resource_forms import AddResourceForm
from pli import get_db

def add_resource():
    form = AddResourceForm(request.form)
    if form.validate():
        get_db().resources.insert_one(form.data)
        return "", 200
    else:
        return abort(400)
