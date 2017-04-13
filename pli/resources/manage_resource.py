from flask import request, abort
from resource_forms import AddResourceForm
from pli import get_db, get_obj_id

def add_resource():
    form = AddResourceForm(request.form)
    if form.validate():
        get_db().resources.insert_one(form.data)
        return "", 200
    else:
        return abort(400)


def check_resource_id(id):
    if id is None:
        return None
    return get_db().resources.find_one({"_id": get_obj_id(id)})

def do_something_to_resource(should_activate):
    id = request.args.get("id", None)
    doc = check_resource_id(id)

    if doc is None:
        return abort(404)

    get_db().resources.update_one({"_id": doc["_id"]},
                                  {"$set": {"active": should_activate}})
    return "", 200


    
def activate_resource():
    return do_something_to_resource(True)

def deactivate_resource():
    return do_something_to_resource(False)

        
