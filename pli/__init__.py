# User stuff
from .pli_user import \
    PliUser, \
    list_all_users, \
    user_by_email

# Our compatability helper (need for testing with mongomock)
from .helpers import \
    encode_uid, \
    decode_uid, \
    uid_exists, \
    objectId_str, \
    datetime_today


# Service utilities
from .service_util import \
    get_db, \
    get_mail, \
    get_signer, \
    get_gridfs, \
    get_obj_id

# Password stuff
from .passwords import \
    init_reset_password, \
    reset_password, \
    gen_hash, \
    check_hash

# Role related things
from .roles import *

# Registration
from .register import \
    register, \
    is_confirmed_uid, \
    validate_user

# Question of the day
from .qotd import \
    get_todays_question, \
    get_todays_choices, \
    get_question


# Blog stuff
from blog import *

# Staff management
from .staff import *

from .carousel_card import *
from .login import validate_login, logout, login
from .surveys import *
from .images import *

from login_form import get_login_form
from .questions import *

import flask
import bson

def pli_init():
    flask.current_app.config["object_id"] = bson.ObjectId
    flask.current_app.teardown_request(save_question_list)
