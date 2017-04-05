#!/usr/bin/env python

from pymongo import MongoClient
from bson import ObjectId
import gridfs
import os
from datetime import datetime
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
db.survey_questions.remove()
db.surveys.remove()
db.responses.remove()
db.usercontent.remove()
db.staff.remove()

u1={
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
#    "real_pass":"iamsecret",
    "password": 'pbkdf2:sha1:1000$FmjdX5b2$c23a5cefc39cc669f3e193670c3c122041266f26',
    "first_name": "Bob",
    "last_name": "Smith",
    "roles": ["admin", "editor"],
    "confirmed": True,
    "organization": {
        "name": "Boston Latin",
        "type": "School",
        "region": "Dorchester"
    }
}
db.users.insert(u1);

u2={
    "_id": 23456,
    "email_address": "iloveindoortennis@gmail.com",
#    "real_pass":"youcantseeme",
    "password": "pbkdf2:sha1:1000$HDOj8diN$62524eb1619b6ee167aeb1d6116ad6075a5bf3cb",
    "first_name": "Alice",
    "last_name": "Da Example",
    "roles": ["participant"],
    "confirmed": False,
    "organization": {
        "name": "Squashbusters",
        "type": "Community Organization",
        "region": "Roxbury"
    }
}
db.users.insert(u2);

u3={
    "_id": 34567,
    "email_address": "iamastudent@someschool.org",
#    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "Eve",
    "roles":[],
    "last_name": "Fakename",
    "confirmed": True,
    "organization": None
}
db.users.insert(u3);

u4={
    "_id": 56789,
    "email_address": "iamapeerleader@bphc.org",
#    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "John",
    "roles":["peer_leader"],
    "last_name": "Leader",
    "confirmed": True,
    "organization": None
}
db.users.insert(u4);

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

survey_question1 = {
    "_id": "survey_question1",
    "question": "When did you last...",
    "answers": [
        {
        "ans_id": 1,
        "answer": "within the past week"
        },
        {
        "ans_id": 2,
        "answer": "within the past month"
        },
        {
            "ans_id": 3,
            "answer": "within the past year"
        },
        {
            "ans_id": 4,
            "answer": "Never"
        }
    ]
}

survey_question2 = {
    "_id": "survey_question2",
    "question": "Which best describes...",
    "answers": [
        {
            "ans_id": 1,
            "answer": "Asian/Pacific Islander"
        },
        {
            "ans_id": 2,
            "answer": "African American"
        },
        {
            "ans_id": 3,
            "answer": "White"
        },
        {
            "ans_id": 4,
            "answer": "Latin American"
        }
    ]
}

survey_question3 = {
    "_id": "survey_question3",
    "question": "How much do you agree with...",
    "answers": [
        {
            "ans_id": 1,
            "answer": "Strongly Agree"
        },
        {
            "ans_id": 2,
            "answer": "Agree"
        },
        {
            "ans_id": 3,
            "answer": "Disagree"
        },
        {
            "ans_id": 4,
            "answer": "Strongly Disagree"
        }
    ]
}

survey_question4 = {
    "_id": "survey_question4",
    "question": "Which do you prefer?",
    "answers": [
        {
            "ans_id": 1,
            "answer": "Strongly Prefer X"
        },
        {
            "ans_id": 2,
            "answer": "Slightly Prefer X"
        },
        {
            "ans_id": 3,
            "answer": "Slightly Prefer Y"
        },
        {
            "ans_id": 4,
            "answer": "Strongly Prefer Y"
        }
    ]
}

survey_questions = [survey_question1, survey_question2, survey_question3, survey_question4]

db.survey_questions.insert_many(survey_questions)

survey1 = dict(_id=ObjectId("survey000001"), name="Survey One", qids=["survey_question1", "survey_question2"])
survey2 = dict(_id=ObjectId("survey000002"), name="Survey Two", qids=["survey_question3","survey_question4"])
survey3 = dict(_id=ObjectId("survey000003"), name="survey Three", qids=["survey_question1", "survey_question2", "survey_question3","survey_question4"])

surveys = [survey1, survey2, survey3]

db.surveys.insert_many(surveys)

response1 = {
    "_id": "response1",
    "survey_id": "survey00001",
    "date_taken": datetime.utcnow(),
    "ans_ids": [1, 3]
}

response2 = {
    "_id": "response2",
    "survey_id": "survey000003",
    "date_taken": datetime.utcnow(),
    "ans_ids": [2, 1, 3, 4]
}

responses = [response1, response2]

db.responses.insert_many(responses)

blog_page_one = {
    "_id": ObjectId(),
    "title":"<h1>Page one</h1>",
    "body":"<h2>Body one</h2>",
    "required_roles": [],
    "owner": u3["_id"],
    "attachments": [],
}

blog_page_two = {
    "_id": ObjectId(),
    "title": "<h1>Page two</h1>",
    "body": "<h2>Body two</h2>",
    "required_roles": ["peer_leader"],
    "owner": u2["_id"],
    "attachments": [
        {"picture": put_gridfs("mongodb.png", "image/png", gridfs)}
    ]
}

blog_page_three = {
    "_id": ObjectId(),
    "title": "<h1>Page three</h1>",
    "body": "<h2>Body three</h2>",
    "required_roles": [],
    "owner": u1["_id"],
    "attachments": [
        {"picture": put_gridfs("FlaskLogo.png", "image/png", gridfs)}
    ]
}


blog_page_four = {
    "_id": ObjectId(),
    "title": "<h1>For the public</h1>",
    "body": "<h2>A post</h2>",
    "required_roles": [],
    "owner": u2["_id"],
    "attachments": []
}

db.usercontent.insert_many(
    [blog_page_one,
     blog_page_two,
     blog_page_three,
     blog_page_four])

staff1 = {
    "_id": ObjectId(),
    "name": "Peggy Gibson",
    "title": "The Boss",
    "bio": "Peggy Gibson is a weird name but I got it from a random name generator, don't judge me. Peggy is the boss for this example and I need to write a bunch of words here because bios are supposed to be sorta long. Like a few sentences or so. Though it doesn't really matter I guess.",
    "picture": gridfs.put(get_image_bytes("howard.png"), content_type="image/png"),
    "email": "theboss@notarealemail.com",
    "phone": "555-555-5555",
    "active": True
}

staff2 = {
    "_id": ObjectId(),
    "name": "Josh Arnold",
    "title": "Vice Boss",
    "bio": "Josh Arnold is a weird name but I got it from a random name generator, don't judge me. Josh is the vice boss for this example, and has no picture.",
    "picture": None,
    "email": "viceboss@notarealemail.com",
    "phone": "555-555-5555",
    "active": True
}

staff3 = {
    "_id": ObjectId(),
    "name": "Erik Maxwell",
    "title": "Regular Employee",
    "bio": "Another random name. Erik's a regular employee so I decided not to give him a phone number, since he's not important enough to get a phone. He's also Peggy's twin.",
    "picture": gridfs.put(get_image_bytes("howard.png"), content_type="image/png"),
    "email": None,
    "phone": None,
    "active": True
}

staff_inactive = {
    "_id": ObjectId(),
    "name": "Victoria Lamb",
    "title": "Regular Employee",
    "bio": "This randomly named person isn't active, and you shouldn't be able to read this. Unless you've made it active, in which case you should. Or if you're in the back-end doing tests or something.",
    "picture": gridfs.put(get_image_bytes("howard.png"), content_type="image/png"),
    "email": None,
    "phone": None,
    "active": False
}

db.staff.insert_many(
    [staff1,
     staff2,
     staff3,
     staff_inactive])

client.close()
