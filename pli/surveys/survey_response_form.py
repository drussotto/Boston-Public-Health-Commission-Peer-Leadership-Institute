from flask import current_app, abort
from bson import ObjectId
from datetime import datetime
from wtforms import Form, StringField, IntegerField, TextField, FieldList,\
RadioField, SelectMultipleField, validators

#50 shades of done with WTForms
class SubmitResponseForm():

    def __init__(self, sid, db):
        self.db = db
        self.sid = str(sid)
        self.survey = self.get_survey(sid)
        self.ans_ids = None
        self.ts = None

    def get_survey(self, sid):
        survey = self.db.surveys.find_one({"_id": ObjectId(self.sid)})

        if survey is None:
            abort(404)

        survey["questions"] = [self.db.survey_questions.find_one({"_id": qid}) for qid in survey["qids"]]

        return survey

    def set_ans_ids(self, request):
        self.ans_ids = [int(ans) for ans in request.form.itervalues()]

    def set_timestamp(self):
        self.ts = datetime.utcnow()

    def as_mongo_doc(self):
        return {
            "survey_id": self.sid,
            "date_taken": self.ts,
            "ans_ids": self.ans_ids
        }

    def validate(self):
        correct_length = len(self.survey["questions"]) == len(self.ans_ids)

        if correct_length:
            for i,question in enumerate(self.survey["questions"]):
                if len(question["answers"]) < self.ans_ids[i]: #out of bounds ans id
                    return False, "Out of bounds answer id: {id},len={l}"\
                        .format(id=self.ans_ids[i],l=len(question["answers"]))
        else:
            return False, "Incorrect number of answers to the survey"

        return True, "All good in the neigborhood"
