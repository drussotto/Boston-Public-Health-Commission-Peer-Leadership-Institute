
question1 = {
    "_id": 0001,
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

question2 = {
    "_id": 0002,
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

question3 = {
    "_id": 0003,
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

question3 = {
    "_id": 0004,
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

questions = [question1, question2, question3, question4]

survey1 = dict(_id=1111, qids: [0001,0002])
survey2 = dict(_id=2222, qids: [0003,0004])
survey3 = dict(_id=3333, qids: [0001, 0002, 0003,0004])

surveys = [survey1, survey2]

response1 = {
    "_id": 9876,
    "survey_id": 12345
    "date_taken": ISODate("2017-09-24"),
    "ans_ids": [1, 3, 2]
}

response2 = {
    "_id": 98765,
    "survey_id": 23456
    "date_taken": ISODate("2017-10-31"),
    "ans_ids": [2, 1, 3]
}

responses = [response1, response2]


def add_mocked_surveys(db):
    db.surveys.insert_many(surveys)

def add_mocked_survey_qs(db):
    db.survey_questions.insert_many(questions)

def add_mocked_responses(db):
    db.responses.insert_many(responses)
