import os
from mongomock import ObjectId, gridfs

def get_image_bytes(file_name):
    path = os.path.join(os.path.dirname(__file__), "res", file_name)
    return open(path, "r")

def init(db, gridfs):
    staff1 = {
        "_id": ObjectId(),
        "name": "Peggy Gibson",
        "title": "The Boss",
        "bio": "Peggy Gibson is a weird name but I got it from a random name generator, don't judge me. Peggy is the boss for this example and I need to write a bunch of words here because bios are supposed to be sorta long. Like a few sentences or so. Though it doesn't really matter I guess.",
        "picture": gridfs.put(get_image_bytes("howard.png"), content_type="image/png"),
        "email": "theboss@notarealemail.com",
        "phone": "555-555-5555",
        "active": True
    }

    staff2 = {
        "_id": ObjectId(),
        "name": "Josh Arnold",
        "title": "Vice Boss",
        "bio": "Josh Arnold is a weird name but I got it from a random name generator, don't judge me. Josh is the vice boss for this example, and has no picture.",
        "picture": None,
        "email": "viceboss@notarealemail.com",
        "phone": "555-555-5555",
        "active": True
    }

    staff3 = {
        "_id": ObjectId(),
        "name": "Erik Maxwell",
        "title": "Regular Employee",
        "bio": "Another random name. Erik's a regular employee so I decided not to give him a phone number, since he's not important enough to get a phone. He's also Peggy's twin.",
        "picture": gridfs.put(get_image_bytes("howard.png"), content_type="image/png"),
        "email": None,
        "phone": None,
        "active": True
    }

    staff_inactive = {
        "_id": ObjectId(),
        "name": "Victoria Lamb",
        "title": "Regular Employee",
        "bio": "This randomly named person isn't active, and you shouldn't be able to read this. Unless you've made it active, in which case you should. Or if you're in the back-end doing tests or something.",
        "picture": gridfs.put(get_image_bytes("howard.png"), content_type="image/png"),
        "email": None,
        "phone": None,
        "active": False
    }

    staff = [ staff1, staff2, staff3, staff_inactive ]

    ex.add(staff1=staff1,
           staff2=staff2,
           staff3=staff3,
           staff_inactive=staff_inactive)

    db.staff.insert_many(staff)

def add_mocked_staff(db):
    init(db, gridfs.MockGridFS(db))
