from flask_login import UserMixin
class PliUser(UserMixin):

    def __init__(self, uid, is_auth):
        self.uid = uid


    def get_id(self):
        return self.uid
    

    @classmethod
    def get(clazz, uid):
        return PliUser(uid, False)

    @classmethod
    def get_auth(clazz, uid):
        return PliUser(uid, True)

    def same_uid(self, them):
        return self.uid == them.uid
