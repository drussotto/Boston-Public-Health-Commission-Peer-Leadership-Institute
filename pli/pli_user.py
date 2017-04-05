from flask import current_app
from flask_login import UserMixin
from service_util import get_db

class PliUser(UserMixin):
    are_roles_valid = False

    def __init__(self, uid, is_auth):
        self.uid = uid

    def get_id(self):
        return self.uid

    @classmethod
    def get(clazz, uid):
        u = PliUser(uid, False)
        if u.get_me() is None:
            return None
        else:
            return u

    @classmethod
    def get_auth(clazz, uid):
        u = PliUser(uid, True)
        if u.get_me() is None:
            return None
        else:
            return u


    def same_uid(self, them):
        return self.uid == them.uid

    def get_me(self):
        return get_db().users.find_one({"_id" : self.uid})

    def get_roles(self, refresh=False):
        if not self.is_authenticated:
            return []
        elif self.are_roles_valid and not refresh:
            return self.role_list
        else:
            # Roles is a space seperated list of roles on the user.
            me = self.get_me()
            roles = me["roles"]
            self.are_roles_valid = True
            self.role_list = roles
            return self.role_list

    def invalidate_roles(self):
        self.are_roles_valid = False

    def update_roles_to(self, new_roles):
        get_db().users.update_one({"_id" : self.uid},
                                  {"$set" : {"roles" : new_roles}})
    def transform_roles(self, f, p, role_name):
        cur_roles = list(self.get_roles(refresh=True))
        if not p(role_name, cur_roles):
            return False
        f(role_name, cur_roles)
        self.update_roles_to(cur_roles)
        # We want to force-load the roles again so they get they updated version.
        self.invalidate_roles()
        return True


    def add_role(self, role_name):
        return self.transform_roles(
            # Add element
            lambda e,l: l.append(e),
            # only add new things
            lambda e,l: e not in l,
            role_name)

    def remove_role(self, role_name):
        return self.transform_roles(
            # remove element
            lambda e,l: l.remove(e),
            # only remove existing things
            lambda e,l: e in l,
            role_name)


    def __getattr__(self, name):
        if name == "roles":
            return self.get_roles()
        else:
            raise AttributeError("No name %s in PliUser" % name)

def list_all_users():
    return get_db().users.find({}, {"password": -1})
