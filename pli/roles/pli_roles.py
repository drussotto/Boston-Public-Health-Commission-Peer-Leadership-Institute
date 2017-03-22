from collections import namedtuple
from flask import current_app, g, request
from flask_login import current_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed, RoleNeed, UserNeed, Permission
from pli import PliUser
from role_info_form import RoleInfoForm
from all_roles import *

# Tells flask principal that we have a new identity (the user with the given uid)
def set_identity(uid):
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(uid))

# Tells flask to remove the identity of the current user
def remove_identity():
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())


# This function gets called when someone's Identity gets initialized
def on_identity_loaded(sender, identity):
    if current_user.is_authenticated:
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'uid'):
            identity.provides.add(UserNeed(current_user.uid))

        # Add roles to the identity
        if current_user.roles is not None:
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role))


def add_role():
    info = RoleInfoForm(request.form)
    if not info.validate():
        return "", 400
    else:
        target = PliUser.get(info.user.data)

        if target is None:
            # User doesn't exist...
            return "", 400

        ok = target.add_role(info.role.data)
        if ok:
            return "", 200
        else:
            return "", 409

def rm_role():
    info = RoleInfoForm(request.form)
    if not info.validate():
        return "", 400
    else:
        target = PliUser.get(info.user.data)

        if target is None:
            # User doesn't exist...
            return "", 400

        ok = target.remove_role(info.role.data)
        if ok:
            return "", 200
        else:
            return "", 409
