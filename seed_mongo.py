#!/usr/bin/env python

from pymongo import MongoClient
from bson import ObjectId
import gridfs
import os
client = MongoClient()
db = client.pli
gridfs = gridfs.GridFS(db)

def get_image_bytes(file_name):
    path = os.path.join(os.path.dirname(__file__), "tests", "testlib", "examples", "res", file_name)
    return open(path, "r")

def put_gridfs(name, mime_type, gridfs):
    gridfs.put(get_image_bytes(name), content_type=mime_type)

db.users.remove()
db.questions.remove()
db.cards.remove()
db.whatsnew.remove()
db.fs.files.remove()
db.fs.chunks.remove()
db.usercontent.remove()

db.users.insert({
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
#    "real_pass":"iamsecret",
    "password": 'pbkdf2:sha1:1000$FmjdX5b2$c23a5cefc39cc669f3e193670c3c122041266f26',
    "first_name": "Bob",
    "last_name": "Smith",
    "roles": "admin editor",
    "confirmed": True,
    "organization": {
        "name": "Boston Latin",
        "type": "School",
        "region": "Dorchester"
    }
});

db.users.insert({
    "_id": 23456,
    "email_address": "iloveindoortennis@gmail.com",
#    "real_pass":"youcantseeme",
    "password": "pbkdf2:sha1:1000$HDOj8diN$62524eb1619b6ee167aeb1d6116ad6075a5bf3cb",
    "first_name": "Alice",
    "last_name": "Da Example",
    "roles": "participant",
    "confirmed": False,
    "organization": {
        "name": "Squashbusters",
        "type": "Community Organization",
        "region": "Roxbury"
    }
});

db.users.insert({
    "_id": 34567,
    "email_address": "iamastudent@someschool.org",
#    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "Eve",
    "roles":"",
    "last_name": "Fakename",
    "confirmed": True,
    "organization": None
});

db.users.insert({
    "_id": 56789,
    "email_address": "iamapeerleader@bphc.org",
#    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "John",
    "roles":"peer_leader",
    "last_name": "Leader",
    "confirmed": True,
    "organization": None
});

db.questions.insert({
    "question_number" : 0,
    "question": "What is the capital of Massachussetts?",
    "choices": {
        "a": "Boston",
        "b": "Washington"
    },
    "answer": "a"
});

db.questions.insert({
    "question_number" : 1,
    "question": "What does PLI stand for?",
    "choices": {
        "a": "Please Leave It",
        "b": "Pop Lock I",
        "c": "Peer Leadership Institute"
    },
    "answer": "c"
});

db.questions.insert({
    "question_number" : 2,
    "question": "What is BPHC?",
    "choices": {
        "a": "Boston Public Health Commission",
    },
    "answer": "a",
});

wn_card0 = {
    "_id": ObjectId(),
    "background": gridfs.put(get_image_bytes("mongodb.png"), content_type="image/png"),
    "caption": "This is in mongo",
    "sub_caption": "This is the sub-caption",
    "hyperlink": "example.com"
}
wn_card1 = {
    "_id": ObjectId(),
    "background": gridfs.put(get_image_bytes("FlaskLogo.png"), content_type="image/png"),
    "caption": "This is a flask app",
    "sub_caption": "Flask is cool.",
    "hyperlink": "example.com"
}
wn_card2 = {
    "_id": ObjectId(),
    "background": gridfs.put(get_image_bytes("stack-overflow.png"), content_type="image/png"),
    "caption": "Powered by stack-overflow",
    "sub_caption": "Teaching me how to do css",
    "hyperlink": "example.com"
}

db.cards.insert_many([wn_card1, wn_card0, wn_card2])
# All our whatsnew info
db.whatsnew.insert({"show": [wn_card2["_id"], wn_card1["_id"]],
                    "cards": [wn_card0["_id"], wn_card1["_id"], wn_card2["_id"]]})

blog_page_one = {
    "_id": ObjectId(),
    "title":"<h1>Page one</h1>",
    "body":"<h2>Body one</h2>",
    "required_roles": [],
    "owner": user3["_id"],
    "attachments": [],
}

blog_page_two = {
    "_id": ObjectId(),
    "title": "<h1>Page two</h1>",
    "body": "<h2>Body two</h2>",
    "required_roles": ["peer_leader"],
    "owner": user2["_id"],
    "attachments": [
        {"picture": put_gridfs("mongodb.png", "image/png", gridfs)}
    ]
}

blog_page_three = {
    "_id": ObjectId(),
    "title": "<h1>Page three</h1>",
    "body": "<h2>Body three</h2>",
    "required_roles": [],
    "owner": user1["_id"],
    "attachments": [
        {"picture": put_gridfs("FlaskLogo.png", "image/png", gridfs)}
    ]
}


blog_page_four = {
    "_id": ObjectId(),
    "title": "<h1>For the public</h1>",
    "body": "<h2>A post</h2>",
    "required_roles": [],
    "owner": user2["_id"],
    "attachments": []
}

db.usercontent.insert_many(
    [blog_page_one,
     blog_page_two,
     blog_page_three,
     blog_page_four])

client.close()
