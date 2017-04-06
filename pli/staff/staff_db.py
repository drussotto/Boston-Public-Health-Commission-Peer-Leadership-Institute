from pli import get_db, get_gridfs, get_obj_id

# Takes in the staff document without the picture field
# and the stream for the picture object.
# returns the objectid of the new user
def add_new_staff(staff_doc, picture):
    pic_id = None
    if picture:
        pic_id = get_gridfs().put(picture, content_type="image")

    staff_doc["picture"] = pic_id
    return get_db().staff.insert_one(staff_doc).inserted_id

def update_staff(id, doc):
    get_db().staff.update_one({"_id": get_obj_id(id)}, {"$set": doc})

def list_active_staff():
    return get_db().staff.find({"active": True}).sort("order", 1)   

def list_inactive_staff():
    return get_db().staff.find({"active": False}).sort("name", 1)

def update_staff_order(ids):
    for index, id in enumerate(ids):
        update_staff(id, {"order": index})

def get_staff_by_id(id):
    if id is None:
        return id
    if not isinstance(id, get_obj_id()):
        id = get_obj_id(id)
    return get_db().staff.find_one({"_id": id})