from pli.service_util import get_db, get_obj_id
from pli import PliUser, ADMIN_PERM
from flask_login import current_user

def add_new_document(doc):
    get_db().usercontent.insert_one(doc)

def get_page_with_id(id):
    if not isinstance(id, get_obj_id()):
        oid = get_obj_id()(id)
    else:
        oid = id
    return get_db().usercontent.find_one({"_id": oid})

def get_page_title_body(id):
    page = get_page_with_id(id)
    return page["title"], page["body"]

def is_allowed_to_view(id):

    # When not given an id, we can't authorize the page
    if not id:
        return False

    page = get_page_with_id(id)

    if current_user.is_authenticated and \
       (page["owner"] == current_user.get_id()) or \
       ADMIN_PERM.can():
        # Owners can always see their own pages.
        return True

    # No requirements => everyone is allowed
    if len(page["required_roles"]) == 0:
        return True

    for role in page["required_roles"]:
        if current_user.is_authenticated and \
           role in current_user.roles:
            return True

    # We've reached here if they don't meet any of the role reqs
    # or they aren't authenticated
    return False
