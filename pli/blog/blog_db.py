from pli.service_util import get_db, get_obj_id
from pli import PliUser
from flask_login import current_user

def add_new_document(doc):
    get_db().userpages.insert_one(doc)

def get_page_with_id(id):
    oid = get_obj_id()(id)
    return get_db().usercontent.find_one({"_id": oid})

def get_page_title_body(id):
    page = get_page_with_id(id)
    return page["title"], page["body"]

def is_allowed_to_view(id):
    page = get_page_with_id(id)
    for role in page["required_roles"]:
        if role in current_user.roles:
            return True
    return False
        
