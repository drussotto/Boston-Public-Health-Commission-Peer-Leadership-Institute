from pli import get_db, get_gridfs

# Takes in the staff document without the picture field
# and the stream for the picture object.
# returns the objectid of the new user
def add_new_staff(staff_doc, picture):
    pic_id = get_gridfs().put(picture, content_type="image")
    staff_doc["picture"] = pic_id
    return get_db().staff.instert_one(staff_doc).inserted_id

def list_active_staff():
    return get_db().staff.find({"active": True})

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
