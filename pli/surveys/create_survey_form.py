from flask import current_app
from bson import ObjectId
from wtforms import Form, StringField, IntegerField, TextField, FieldList, SelectMultipleField, validators


class CreateSurveyForm():

    def __init__(self, db):
        self.db = db
        self.name = None
        self.questions = None

    @staticmethod
    def get_survey_questions(db):
        raw_data = db.survey_questions.find()

        choices = [(str(q["_id"]), q["question"]) for q in raw_data]
        return choices

    def set_name(self, request):
        self.name = request.form["name"]

    def set_questions(self, request):
        form_pairs = sorted(request.form.items(),
                            cmp=lambda q1, q2: cmp(q1[0], q2[0]))

        self.questions = [fp[1] for fp in form_pairs if fp[0] != "name"]


    def as_mongo_doc(self):
        return {
            "name": self.name,
            "qids": self.questions
        }

    def validate(self):
        if not self.name:
            return False, "Survey must have a name"

        if self.questions is None or len(self.questions) == 0:
            return False, "Must have at least one question in the survey"

        for qid in self.questions:
            question = self.db.survey_questions.find_one({"_id": ObjectId(str(qid))})
            if question is None:
                return False, "Invalid question id"

        return True, "We cool"

class CreateQuestionForm(Form):
    question = TextField("Question", [validators.required()])
    answers = FieldList(TextField('Answers', [validators.required()]), min_entries=0)

    def as_mongo_doc(self):
        return {
            "question": self.question.data,
            "answers": [dict(ans_id=i, answer=self.answers.data[i]) \
             for i in range(len(self.answers.data))]
        }

    def validate(self):
        if not Form.validate(self):
            return False

        if len(self.answers.data) < 1:
            self.errors["answers"] = "Must provide at least one answer for the question"
            return False

        return True
