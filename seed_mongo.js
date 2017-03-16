db.users.insert({
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
    "real_pass":"iamsecret",
    "password": 'pbkdf2:sha1:1000$FmjdX5b2$c23a5cefc39cc669f3e193670c3c122041266f26',
    "first_name": "Bob",
    "last_name": "Smith",
    "roles": "admin editor",
    "confirmed": true,
    "organization": {
        "name": "Boston Latin",
        "type": "School",
        "region": "Dorchester"
    }
});

db.users.insert({
    "_id": 23456,
    "email_address": "iloveindoortennis@gmail.com",
    "real_pass":"youcantseeme",
    "password": "pbkdf2:sha1:1000$HDOj8diN$62524eb1619b6ee167aeb1d6116ad6075a5bf3cb",
    "first_name": "Alice",
    "last_name": "Da Example",
    "roles": "participant",
    "confirmed": false,
    "organization": {
        "name": "Squashbusters",
        "type": "Community Organization",
        "region": "Roxbury"
    }
});

db.users.insert({
    "_id": 34567,
    "email_address": "iamastudent@someschool.org",
    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "Eve",
    "roles":"",
    "last_name": "Fakename",
    "confirmed": true,
    "organization": null
});

db.users.insert({
    "_id": 56789,
    "email_address": "iamapeerleader@bphc.org",
    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "John",
    "roles":"peer_leader",
    "last_name": "Leader",
    "confirmed": true,
    "organization": null
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



