
from flask import current_app, g

def _get_cache_cfg_val(name):
    # I would like to cache these things in g,
    # but we can't assign at this point
    return current_app.config[name]

# Gets the current database client for the app
def get_db():
    return _get_cache_cfg_val("db")

# Gets the flask-mail manager for the app
def get_mail():
    return _get_cache_cfg_val("mail")

# Gets the secure "itsdangerous" http encoded signer
# uses the app's secret key
def get_signer():
    return _get_cache_cfg_val("signer")

# Gets the gridfs manager for the app.
def get_gridfs():
    return _get_cache_cfg_val("gridfs")

# Returns the current "ObjectId" constructor that the app should use.
# During a real instance of the site this will correspond to bson.ObjectId
# During testing this will correspond to mongomock.ObjectId
def get_obj_id(arg=None):
    if arg is not None:
        try:
            return _get_cache_cfg_val("object_id")(arg)
        except:
            return None
    else:
        return _get_cache_cfg_val("object_id")
