import mongomock

# These are example questions which get loaded into the test DB

question1 = {
    "_id": 1,
    "question": "What is the capital of Massachussetts?",
    "choices": {
        "a": "Boston",
        "b": "Washington"
    },
    "answer": "a"
}

question2 = {
    "_id": 2,
    "question": "What does PLI stand for?",
    "choices": {
        "a": "Please Leave It",
        "b": "Pop Lock I",
        "c": "Peer Leadership Institute"
    },
    "answer": "c"
}

question3 = {
    "_id": 3,
    "question": "What is BPHC?",
    "choices": {
        "a": "Boston Public Health Commission",
    },
    "answer": "a",
}

questions = [question1, question2, question3]

def mocked_questions():
    db = mongomock.MongoClient().pli
    db.questions.insert_many(questions)
    return db
