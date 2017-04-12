from datetime import datetime
from bson import ObjectId
#from pli import objectId_str
from pli import objectId_str

survey_question1 = {
    "_id": ObjectId("sq0000000001"),
    "question": "When did you last...",
    "answers": [
        {
            "ans_id": 0,
            "answer": "within the past week"
        },
        {
            "ans_id": 1,
            "answer": "within the past month"
        },
        {
            "ans_id": 2,
            "answer": "within the past year"
        },
        {
            "ans_id": 3,
            "answer": "Never"
        }
    ]
}

survey_question2 = {
    "_id": ObjectId("sq0000000002"),
    "question": "Which best describes...",
    "answers": [
        {
            "ans_id": 0,
            "answer": "Asian/Pacific Islander"
        },
        {
            "ans_id": 1,
            "answer": "African American"
        },
        {
            "ans_id": 2,
            "answer": "White"
        },
        {
            "ans_id": 3,
            "answer": "Latin American"
        }
    ]
}

survey_question3 = {
    "_id": ObjectId("sq0000000003"),
    "question": "How much do you agree with...",
    "answers": [
        {
            "ans_id": 0,
            "answer": "Strongly Agree"
        },
        {
            "ans_id": 1,
            "answer": "Agree"
        },
        {
            "ans_id": 2,
            "answer": "Disagree"
        },
        {
            "ans_id": 3,
            "answer": "Strongly Disagree"
        }
    ]
}

survey_question4 = {
    "_id": ObjectId("sq0000000004"),
    "question": "Which do you prefer?",
    "answers": [
        {
            "ans_id": 0,
            "answer": "Strongly Prefer X"
        },
        {
            "ans_id": 1,
            "answer": "Slightly Prefer X"
        },
        {
            "ans_id": 2,
            "answer": "Slightly Prefer Y"
        },
        {
            "ans_id": 3,
            "answer": "Strongly Prefer Y"
        }
    ]
}

survey_question5 = {
    "_id": ObjectId("sq0000000005"),
    "question": "Which do you prefer?",
    "answers": [
        {
            "ans_id": 0,
            "answer": "Strongly Prefer X"
        },
        {
            "ans_id": 1,
            "answer": "Slightly Prefer X"
        },
        {
            "ans_id": 2,
            "answer": "Slightly Prefer Y"
        },
        {
            "ans_id": 3,
            "answer": "Strongly Prefer Y"
        }
    ]
}


survey_questions = [survey_question1, survey_question2, survey_question3, survey_question4, survey_question5]

ex.add(survey_question1=survey_question1,
        survey_question2=survey_question2,
        survey_question3=survey_question3,
        survey_question4=survey_question4,
        survey_question5=survey_question5)

survey1 = dict(_id=ObjectId("survey000001"), name="Survey One",
                    qids=[objectId_str(qid) for qid in ["sq0000000001", "sq0000000002"]])
survey2 = dict(_id=ObjectId("survey000002"), name="Survey Two",
                    qids=[objectId_str(qid) for qid in ["sq0000000003","sq0000000004"]])
survey3 = dict(_id=ObjectId("survey000003"), name="Survey Three",
                qids=[objectId_str(qid) for qid in ["sq0000000001", "sq0000000002", "sq0000000003","sq0000000004"]])

surveys = [survey1, survey2, survey3]

ex.add(survey1=survey1,
        survey2=survey2,
        survey3=survey3)

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
    "ans_ids": [1, 0, 2, 3]
}

response_list = []

for i in range(20):
    response_list.append({
        "_id": ObjectId(),
        "survey_id": objectId_str("survey000003"),
        "date_taken": datetime.utcnow(),
        "ans_ids": [1, 0, 2, 3]
    })

    response_list.append({
        "_id": ObjectId(),
        "survey_id": objectId_str("survey000003"),
        "date_taken": datetime.utcnow(),
        "ans_ids": [0, 2, 1, 3]
    })

    response_list.append({
        "_id": ObjectId(),
        "survey_id": objectId_str("survey000003"),
        "date_taken": datetime.utcnow(),
        "ans_ids": [0, 2, 1, 3]
    })

for i in range(10):
    response_list.append({
        "_id": ObjectId(),
        "survey_id": objectId_str("survey000003"),
        "date_taken": datetime.utcnow(),
        "ans_ids": [3, 1, 0, 0]
    })

    response_list.append({
        "_id": ObjectId(),
        "survey_id": objectId_str("survey000003"),
        "date_taken": datetime.utcnow(),
        "ans_ids": [2, 3, 3, 1]
    })

responses = [response1, response2]

ex.add(response1=response1,
        response2=response2)

def add_mocked_surveys(db):
    db.surveys.insert_many(surveys)

def add_mocked_survey_questions(db):
    db.survey_questions.insert_many(survey_questions)

def add_mocked_responses(db):
    db.responses.insert_many(responses)
    db.responses.insert_many(response_list)
