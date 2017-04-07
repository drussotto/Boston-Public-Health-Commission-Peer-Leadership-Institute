# This module contains all of our predefined roles.
from .all_roles import \
    has_admin, \
    has_editor, \
    has_peerleader, \
    has_user, \
    admin_perm, \
    editor_perm, \
    peerleader_perm, \
    user_perm, \
    get_all_roles, \
    has_permission

# All of the functions for manipulating roles.
from .pli_roles import edit_role, set_identity, remove_identity, on_identity_loaded
