

import mongomock

question1 = {
    "question_number" : 0,
    "question": "What is the capital of Massachussetts?",
    "choices": {
        "a": "Boston",
        "b": "Washington"
    },
    "answer": "a"
}

question2 = {
    "question_number" : 1,
    "question": "What does PLI stand for?",
    "choices": {
        "a": "Please Leave It",
        "b": "Pop Lock I",
        "c": "Peer Leadership Institute"
    },
    "answer": "c"
}

question3 = {
    "question_number" : 2,
    "question": "What is BPHC?",
    "choices": {
        "a": "Boston Public Health Commission",
    },
    "answer": "a",
}

questions = [question1, question2, question3]

def add_mocked_questions(db):
    db.questions.insert_many(questions)

ex.add(question1=question1,
       question2=question2,
       question3=question3,
       questions=questions)
