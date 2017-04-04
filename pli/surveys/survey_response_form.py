from flask import current_app, abort
from bson import ObjectId
from wtforms import Form, StringField, IntegerField, TextField, FieldList,\
RadioField, SelectMultipleField, validators

#50 shades of done with WTForms
class SubmitResponseForm():

    def get_survey(self, sid, db):
        survey = db.surveys.find_one({"_id": ObjectId(sid)})

        if survey is None:
            abort(404)

        survey["questions"] = [db.survey_questions.find_one({"_id": qid}) for qid in survey["qids"]]

        return survey
