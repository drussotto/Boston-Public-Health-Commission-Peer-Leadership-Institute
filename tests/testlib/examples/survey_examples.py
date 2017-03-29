from datetime import datetime

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

survey1 = dict(_id="survey1", qids=["survey_question1", "survey_question2"])
survey2 = dict(_id="survey2", qids=["survey_question3","survry_question4"])
survey3 = dict(_id="survey3", qids=["survey_question1", "survey_question2", "survey_question3","survey_question4"])

surveys = [survey1, survey2, survey3]

response1 = {
    "_id": "response1",
    "survey_id": "survey1",
    "date_taken": datetime.utcnow(),
    "ans_ids": [1, 3]
}

response2 = {
    "_id": "response2",
    "survey_id": "survey3",
    "date_taken": datetime.utcnow(),
    "ans_ids": [2, 1, 3, 4]
}

responses = [response1, response2]


def add_mocked_surveys(db):
    db.surveys.insert_many(surveys)

def add_mocked_survey_questions(db):
    db.survey_questions.insert_many(survey_questions)

def add_mocked_responses(db):
    db.responses.insert_many(responses)
