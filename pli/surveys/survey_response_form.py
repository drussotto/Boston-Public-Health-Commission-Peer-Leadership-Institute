from flask import current_app
from wtforms import Form, StringField, IntegerField, TextField, FieldList,\
RadioField, SelectMultipleField, validators

#50 shades of done with WTForms
class SubmitResponseForm():

    def get_survey(self, sid, db):
        survey = db.surveys.find({"_id": sid})[0]

        survey["questions"] = [db.survey_questions.find({"_id": qid})[0] for qid in survey["qids"]]

        return survey
