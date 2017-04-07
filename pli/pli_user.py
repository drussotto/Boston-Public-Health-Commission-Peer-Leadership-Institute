from flask import current_app, abort
from flask_login import UserMixin
from service_util import get_db
import pli

class PliUser(UserMixin):
    are_role_valid = False

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

    def get_role(self, refresh=False):
        if not self.is_authenticated:
            return None
        elif self.are_role_valid and not refresh:
            return self.role
        else:
            # Roles is a space seperated list of roles on the user.
            me = self.get_me()
            role = me["role"]
            self.are_role_valid = True
            self.role = role
            return self.role

    def invalidate_role(self):
        self.are_roles_valid = False

    def update_role_to(self, name):
        get_db().users.update_one({"_id": self.uid}, {"$set": {"role": name}})
    
    def edit_role(self, role_name):
        if (role_name in pli.get_all_roles()):
            self.update_role_to(role_name)
            self.invalidate_role()
            return "", 200
        else:
            return "", 400

    def __getattr__(self, name):
        if name == "role":
            return self.get_role()
        else:
            raise AttributeError("No name %s in PliUser" % name)

def user_by_email(email):
    return get_db().users.find_one({"email_address": email})

def list_all_users():
    return get_db().users.find({}, {"password": 0})
