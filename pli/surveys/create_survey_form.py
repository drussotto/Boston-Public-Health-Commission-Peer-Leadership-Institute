from flask import current_app
from wtforms import Form, StringField, IntegerField, TextField, FieldList, SelectMultipleField, validators


class CreateSurveyForm(Form):
    name = TextField("Name", [validators.required()])
    questions = SelectMultipleField("Questions", coerce=unicode)

    def populate_survey_questions(self, db):
        raw_data = db.survey_questions.find()
        
        self.questions.choices = [(str(q["_id"]), q["question"]) for q in raw_data]
        return self.questions.choices


    def as_mongo_doc(self):
        return {
            "name": self.name.data,
            "qids": self.questions.data
        }

    def validate(self):
        if not Form.validate(self):
            return False

        if len(self.questions.data) < 1:
            self.errors["questions"] = "Must provide at least one question for the survey"
            return False

        return True

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
