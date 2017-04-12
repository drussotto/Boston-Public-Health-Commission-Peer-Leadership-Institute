from flask_principal import Identity, AnonymousIdentity, identity_changed, RoleNeed, UserNeed, Permission

# String must not have spaces, as users can have multiple roles
# And this is accomplished by a space delimited string.
# For more information, see example data for MongoDB

_ADMIN_ROLE = "admin"
_EDITOR_ROLE = "editor"
_PEERLEADER_ROLE = "peer_leader"
_USER_ROLE = "user"

_ADMIN_NEED = RoleNeed(_ADMIN_ROLE)
_EDITOR_NEED = RoleNeed(_EDITOR_ROLE)
_PEERLEADER_NEED = RoleNeed(_PEERLEADER_ROLE)
_USER_NEED = RoleNeed(_USER_ROLE)

_ADMIN_PERM = Permission(_ADMIN_NEED)
_EDITOR_PERM = Permission(_ADMIN_NEED, _EDITOR_NEED)
_PEERLEADER_PERM = Permission(_ADMIN_NEED, _EDITOR_NEED, _PEERLEADER_NEED)
_USER_PERM = Permission(_ADMIN_NEED, _EDITOR_NEED, _PEERLEADER_NEED, _USER_NEED)


def get_all_roles():
    return [_ADMIN_ROLE, _EDITOR_ROLE, _PEERLEADER_ROLE, _USER_ROLE]

def has_admin():
    return _ADMIN_PERM.can()

def has_editor():
    return _EDITOR_PERM.can()

def has_peerleader():
    return _PEERLEADER_PERM.can()

def has_user():
    return _USER_PERM.can()
        
def admin_perm(f):
    return _ADMIN_PERM.require(http_exception=403)(f)

def editor_perm(f):
    return _EDITOR_PERM.require(http_exception=403)(f)

def peerleader_perm(f):
    return _PEERLEADER_PERM.require(http_exception=403)(f)

def user_perm(f):
    return _USER_PERM.require(http_exception=403)(f)

def _to_perm(name):
    if name == _ADMIN_ROLE:
        return _ADMIN_PERM
    elif name == _EDITOR_ROLE:
        return _EDITOR_PERM
    elif name == _PEERLEADER_ROLE:
        return _PEERLEADER_PERM
    elif name == _USER_ROLE:
        return _USER_PERM
    else:
        return None

def has_permission(name):
    return Permission(_to_perm(name)).can()
