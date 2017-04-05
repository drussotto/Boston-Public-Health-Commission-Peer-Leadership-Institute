from pli import get_db, get_gridfs, get_obj_id

# Takes in the staff document without the picture field
# and the stream for the picture object.
# returns the objectid of the new user
def add_new_staff(staff_doc, picture):
    if picture is None:
        pic_id = _default_picture()
    else:
        pic_id = get_gridfs().put(picture, content_type="image")

    staff_doc["picture"] = pic_id
    return get_db().staff.insert_one(staff_doc).inserted_id


def update_staff(id, doc):
    get_db().staff.update_one({"_id": get_obj_id(id)}, {"$set": doc})

def list_active_staff():
    return get_db().staff.find({"active": True})

def get_staff_by_id(id):
    if id is None:
        return id
    if not isinstance(id, get_obj_id()):
        id = get_obj_id(id)
    return get_db().staff.find_one({"_id": id})
# staff1 = {
    #     "_id": ObjectId(),
    #     "name": "Peggy Gibson",
    #     "title": "The Boss",
    #     "bio": "Peggy Gibson is a weird name but I got it from a random name generator, don't judge me. Peggy is the boss for this example and I need to write a bunch of words here because bios are supposed to be sorta long. Like a few sentences or so. Though it doesn't really matter I guess.",
    #     "picture": gridfs.put(get_image_bytes("howard.png"), content_type="image/png"),
    #     "email": "theboss@notarealemail.com",
    #     "phone": "555-555-5555",
    #     "active": True
    # }

# TODO
def _default_picture():
    pass
