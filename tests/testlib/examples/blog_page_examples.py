import os
import mongomock
import pli
from mongomock import ObjectId
from mongomock import gridfs
from pli.service_util import get_db
from users_examples import user1, user2, user3, user4

def get_image_bytes(file_name):
    path = os.path.join(os.path.dirname(__file__), "res", file_name)
    return open(path, "r")

blog_page_one = None
blog_page_two = None
blog_page_three = None
blog_page_four = None

def get_image_bytes(file_name):
    path = os.path.join(os.path.dirname(__file__), "res", file_name)
    return open(path, "r")

def put_gridfs(name, mime_type, gridfs):
    gridfs.put(get_image_bytes(name), content_type=mime_type)

def build_and_assign_blogs(db, gridfs):

    blog_page_one = {
        "_id": ObjectId(),
        "title":"Page one",
        "body":"Body one",
        "required_role": pli.roles.all_roles._ADMIN_ROLE,
        "owner": user1["_id"],
        "attachments": [],
    }

    blog_page_two = {
        "_id": ObjectId(),
        "title": "Page two",
        "body": "Body two",
        "required_role": pli.roles.all_roles._PEERLEADER_ROLE,
        "owner": user2["_id"],
        "attachments": [
            {"picture": put_gridfs("mongodb.png", "image/png", gridfs)}
        ]
    }

    blog_page_three = {
        "_id": ObjectId(),
        "title": "Page three",
        "body": "Body three",
        "required_role": None,
        "owner": user3["_id"],
        "attachments": [
            {"picture": put_gridfs("FlaskLogo.png", "image/png", gridfs)}
        ]
    }

    blog_page_four = {
        "_id": ObjectId(),
        "title": "For the public",
        "body": "A post",
        "required_role": None,
        "owner": user2["_id"],
        "attachments": []
    }

    db.usercontent.insert_many(
        [blog_page_one,
         blog_page_two,
         blog_page_three,
         blog_page_four])
    ex.add(blog_page_one=blog_page_one,
           blog_page_two=blog_page_two,
           blog_page_three=blog_page_three,
           blog_page_four=blog_page_four)

def add_mocked_blogs(db):
    build_and_assign_blogs(db, gridfs.MockGridFS(db))

def list_all_pages():
    return list(get_db().usercontent.find({}))
