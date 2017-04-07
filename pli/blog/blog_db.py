from pli.service_util import get_db, get_obj_id
from pli import PliUser, has_admin, has_permission
from flask_login import current_user
from flask import jsonify, request

# Updates the document with the given ID
def update_document(id, doc):
    get_db().usercontent.update_one({"_id": id}, {"$set": doc})

# Adds the document (doc) to the database
# returns the id of the new document.
def add_new_document(doc):
    return get_db().usercontent.insert_one(doc).inserted_id

# Removes one document with the given id
def remove_document(doc_id):
    get_db().usercontent.delete_one({"_id": doc_id})

# Internal function which safely collects the document that corresponds
# the given id
def _get_page_with_id(id):
    try:
        # Allow users to pass in strings OR ObjectId's
        if not isinstance(id, get_obj_id()):
            oid = get_obj_id()(id)
        else:
            oid = id
    except:
        return None # Bad objid

    return get_db().usercontent.find_one({"_id": oid})

# Returns (title, body) for the page with the given id
def get_page_title_body(id):
    page = get_page_to_view(id)
    if page is None:
        return None
    return page["title"], page["body"]

# Safely collects the blog page with the given id, will return None
# if the current_user is not allowed to view the page
def get_page_to_view(id):
    # When not given an id, we can't authorize the page
    if not id:
        return None

    page = _get_page_with_id(id)

    # No page => can't view it ?
    if not page:
        return None

    if current_user.is_authenticated and \
       (page["owner"] == current_user.get_id()) or \
       has_admin():
        # Owners can always see their own pages.
        # (and so can admins)
        return page

    # No requirements => everyone is allowed
    if len(page["required_roles"]) == 0:
        return page

    for role in page["required_roles"]:
        if current_user.is_authenticated and \
           has_permission(role):
            return page

    # We've reached here if they don't meet any of the role reqs
    # or they aren't authenticated
    return None

def get_page_to_edit(id):
    # Editting a page has the same rules as deleting the page
    return get_page_to_delete(id)

# Safely collects the blog page with the given id, will return None
# if current_user does not have permission to delete.
def get_page_to_delete(id):
    # Easy case, no id (or not logged in) => nothing to/can delete
    if id is None or \
       not current_user.is_authenticated:
        return None

    page = _get_page_with_id(id)

    # If the page doesn't exist you can't remove it.
    if page is None:
        return None

    # If we own the page, we can delete it
    if page["owner"] == current_user.get_id():
        return page

    # Admins can always delete
    if has_admin():
        return page

    # Otherwise NO
    return None

def get_deletable_pages():
    if has_admin():
        return get_db().usercontent.find({})
    else:
        return get_my_pages()

def get_my_pages():
    if current_user.is_authenticated:
        return get_db().usercontent.find({"owner": current_user.get_id()})
    else:
        return []

        
def get_segmented_page_list():
    total = get_db().usercontent.count()
    def get(x, y):
        return list(get_db().usercontent
                    .find({})
                    .sort("_id", -1)
                    .skip(x * 10)
                    .limit(y))
    
    def clear_not_allowed(l):
        out = []
        for x in l:
            y = get_page_to_view(x["_id"])
            if y is not None:
                out.append(x)
        return out
        
    skip = int(request.args.get("skip", 0))
    number = int(request.args.get("number", 10))
    pgs = clear_not_allowed(get(skip, number))
    count = len(pgs)
    
    while len(pgs) != number and count < total:
        skip += 1
        tmp = clear_not_allowed(get(skip, number - len(pgs)))
        pgs += tmp
        count += number

    for x in pgs:
        x["_id"] = str(x["_id"])
        
    return jsonify(pgs)
    
    
def blog_page_count():
    return range(get_db().usercontent.count())
