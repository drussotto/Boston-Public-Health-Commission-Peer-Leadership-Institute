from pli import ADMIN_ROLE, EDITOR_ROLE, PARTICIPANT_ROLE, PEERLEADER_ROLE
import mongomock

# A convinience test case containing the "mocked users"
# From testlib in the db# Note that the "real_pass" field for these won't be present in the actual db
# just there for convinience during testing.
user1 = {
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
    "real_pass":"iamsecret",
    "password": 'pbkdf2:sha1:1000$FmjdX5b2$c23a5cefc39cc669f3e193670c3c122041266f26',
    "first_name": "Bob",
    "last_name": "Smith",
    "roles": [ADMIN_ROLE, EDITOR_ROLE],
    "confirmed": True,
    "organization": {
        "name": "Boston Latin",
        "type": "School",
        "region": "Dorchester"
    }
}

user2 = {
    "_id": 23456,
    "email_address": "iloveindoortennis@gmail.com",
    "real_pass":"youcantseeme",
    "password": "pbkdf2:sha1:1000$HDOj8diN$62524eb1619b6ee167aeb1d6116ad6075a5bf3cb",
    "first_name": "Alice",
    "last_name": "Da Example",
    "roles": [PARTICIPANT_ROLE],
    "confirmed": False,
    "organization": {
        "name": "Squashbusters",
        "type": "Community Organization",
        "region": "Roxbury"
    }
}

user3 = {
    "_id": 34567,
    "email_address": "iamastudent@someschool.org",
    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "Eve",
    "roles":[],
    "last_name": "Fakename",
    "confirmed": True,
    "organization": None
}

user_editor = {
    "_id": 123568,
    "email_address": "iamaneditor@bphc.org",
    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "Blue",
    "roles": [EDITOR_ROLE],
    "last_name": "Steel",
    "confirmed": True,
    "organization": None
}

user4 = {
    "_id": 56789,
    "email_address": "iamapeerleader@bphc.org",
    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "John",
    "roles": [PEERLEADER_ROLE],
    "last_name": "Leader",
    "confirmed": True,
    "organization": None
}

users = [user1, user2, user3, user4, user_editor]

ex.add(user1=user1,
       user2=user2,
       user3=user3,
       user4=user4,
       user_editor=user_editor,
       users=users)

def add_mocked_users(db):
    db.users.insert_many(users)
