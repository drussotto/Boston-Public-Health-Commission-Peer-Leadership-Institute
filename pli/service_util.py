
from flask import current_app, g

def _get_cache_cfg_val(name):
    # I would like to cache these things in g,
    # but we can't assign at this point
    return current_app.config[name]


def get_db():
    return _get_cache_cfg_val("db")

def get_mail():
    return _get_cache_cfg_val("mail")

def get_signer():
    return _get_cache_cfg_val("signer")

def get_gridfs():
    return _get_cache_cfg_val("gridfs")
