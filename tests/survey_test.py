from testlib import *
from datetime import date
from bson import ObjectId
from pli import retrieve_response_data, objectId_str, get_db

class RetrieveSurveyTest(PliEntireDbTestCase):


    @with_test_client
    def test_retreive_valid_survey(self, client):
        res = client.get("/surveys/survey000001")
        assert_survey_page(self, res)

    @with_test_client
    def test_retreive_invalid_survey(self, client):
        res = client.get("/surveys/surveyxxx003")
        assert_not_survey_page(self, res)
        assert_404_page(self, res)

class SubmitResponseTest(PliSurveysTestCase):
    def db_inits(self):
        #hack because this test case should not depend on qotd but it does
        #because of the with_login decorator
        return PliSurveysTestCase.db_inits(self) + [add_mocked_questions]

    @with_test_client
    def test_submit_valid_response1(self, client):

        form_data = {
            "survey_question1": 1,
            "survey_question2": 2,
        }

        res = client.post("/surveys/{sid}".format(sid=objectId_str("survey000001")),
                            data=form_data)
        assert_response_submitted_page(self, res)


    @with_test_client
    def test_submit_valid_response2(self, client):

        form_data = {
            "survey_question0": 0,
            "survey_question1": 2,
            "survey_question2": 3,
            "survey_question3": 2,
        }

        res = client.post("/surveys/{sid}".format(sid=objectId_str("survey000003")), data=form_data)
        assert_response_submitted_page(self, res)

    #invalid id
    @with_test_client
    def test_submit_invalid_response1(self, client):
        form_data = {
            "survey_question1": 1,
            "survey_question2": 2,
        }

        res = client.post("surveys/{sid}".format(sid=objectId_str("surveyxxx003")), data=form_data)
        assert_response_failed_page(self, res)

    #too many questions
    @with_test_client
    def test_submit_invalid_response2(self, client):
        form_data = {
            "survey_question1": 1,
            "survey_question2": 2,
            "survey_question3": 1
        }

        #2 questions on this survey
        sid = "survey000001"
        res = client.post("surveys/{sid}".format(sid=sid), data=form_data)
        assert_response_failed_page(self, res)

    #Not enough questions
    @with_test_client
    def test_submit_invalid_response3(self, client):
        form_data = {
            "survey_question1": 1,
            "survey_question2": 2,
            "survey_question3": 1
        }

        #4 questions on this survey
        res = client.post("surveys/{sid}".format(sid=objectId_str("survey000003")), data=form_data)
        assert_response_failed_page(self, res)

    #invalid ans_id for a questoin
    @with_test_client
    def test_submit_invalid_response4(self, client):
        form_data = {
            "survey_question1": 1,
            "survey_question2": 2,
            "survey_question3": 1,
            "survey_question4": 7,

        }

        res = client.post("surveys/{sid}".format(sid=objectId_str("survey000003")), data=form_data)
        assert_response_failed_page(self, res)


class CreateQuestionTest(PliUsersTestCase):
    def db_inits(self):
        #hack because this test case should not depend on qotd but it does
        #because of the with_login decorator
        return PliUsersTestCase.db_inits(self) + [add_mocked_questions]

    #admin role
    @with_login(user1["email_address"], user1["real_pass"])
    def test_get_create_question_page_1(self, client):
        res = client.get("/surveys/questions/create")
        assert_create_survey_question_page(self, res)

    #editor role
    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_get_create_question_page_2(self, client):
        res = client.get("/surveys/questions/create")
        assert_create_survey_question_page(self, res)

    #participant role - not allowed
    @with_login(user2["email_address"], user2["real_pass"])
    def test_get_create_question_page_3(self, client):
        res = client.get("/surveys/questions/create")
        assert_not_create_survey_question_page(self, res)
        self.assertEqual(403, res.status_code)

    #not logged in - redirect to login page
    @with_test_client
    def test_get_create_question_page_4(self, client):
        res = client.get("/surveys/questions/create")

        assert_not_create_survey_question_page(self, res)
        assert_redirect_page(self, res)



    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_question_success(self, client):

        form_data = {
            "question": "question?",
            "answers-0": "Yes",
            "answers-1": "No",
        }

        res = client.post("/surveys/questions/create", data=form_data)
        assert_create_success_page(self, res)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_question_fail_1(self, client):
        #Blank question
        form_data = {
            "question": "",
            "answers-0": "Yes",
            "answers-1": "No"
        }

        res = client.post("/surveys/questions/create", data=form_data)
        assert_create_failed_page(self, res)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_question_fail_2(self, client):
        #No answers
        form_data = {
            "question": "Some question"
        }

        res = client.post("/surveys/questions/create", data=form_data)
        assert_create_failed_page(self, res)

    @with_login(user2["email_address"], user2["real_pass"])
    def test_create_question_fail_3(self, client):
        #invalid permissions
        form_data = {
            "question": "question?",
            "answers-0": "Yes",
            "answers-1": "No",
        }

        res = client.post("/surveys/questions/create", data=form_data)
        assert_create_failed_page(self, res)
        self.assertEqual(403, res.status_code)


class CreateSurveyTest(PliSurveyQuestionsTestCase):
    def db_inits(self):
        #hack because this test case should not depend on qotd but it does
        #because of the with_login decorator
        return PliSurveyQuestionsTestCase.db_inits(self) + [add_mocked_questions]

    #admin privilege
    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_valid_survey_success1(self, client):
        #form_data = "name=NewSurvey1&questions=survey_question1&questions=survey_question3"

        form_data = {
            "name": "NewSurvey1",
            "question-0": "sq0000000001",
            "question-1": "sq0000000003"
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_success_page(self, res)

    #editor privilege
    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_create_valid_survey_success2(self, client):
        form_data = {
            "name": "NewSurvey1",
            "question-0": "sq0000000001",
            "question-1": "sq0000000003",
            "question-2": "sq0000000002"
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_success_page(self, res)

    #participant privilege (forbidden)
    @with_login(user2["email_address"], user2["real_pass"])
    def test_create_valid_survey_failure1(self, client):
        form_data = {
            "name": "NewSurvey1",
            "question-0": "sq0000000001",
            "question-1": "sq0000000003"
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_failed_page(self, res)
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_create_valid_survey_failure1(self, client):
        form_data = {
            "name": "NewSurvey1",
            "question-0": "sq0000000001",
            "question-1": "sq0000000003"
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_failed_page(self, res)
        assert_redirect_page(self, res)

    #No name for the survey
    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_invalid_survey1(self, client):
        form_data = {
            "name": "",
            "question-0": "sq0000000001",
            "question-1": "sq0000000003"
        }

        res = client.post("/surveys/create", data=form_data)
        self.assertEqual(res.status_code, 400)
        assert_create_failed_page(self, res)

    #No questions on the survey
    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_invalid_survey2(self, client):
        form_data = {
            "name": "NewSurvey1"
        }

        res = client.post("/surveys/create", data=form_data)
        self.assertEqual(res.status_code, 400)
        assert_create_failed_page(self, res)

    #invalid question id
    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_survey_bad_qid(self, client):
        form_data = {
            "name": "some name",
            "question-0": "sq0000000001",
            "question-1": "sq000z00x001"
        }

        res = client.post("/surveys/create", data=form_data)
        self.assertEqual(res.status_code, 400)
        assert_create_failed_page(self, res)

class RetrieveResponsesTest(PliEntireDbTestCase):
    @with_app_ctxt
    def test_retrieve_response_data(self):

        response_data = retrieve_response_data(objectId_str("survey000003"))
        self.assertEqual(len(response_data["questions"]), 4)
        self.assertEqual(len(response_data["questions"][0]["answers"].keys()), 4)

        q4_ans4 = ex.survey_question4["answers"][3]["answer"]


        self.assertEqual(response_data["questions"][3]["answers"][q4_ans4], 60)


    @with_login(user1["email_address"], user1["real_pass"])
    def test_get_survey_results_page1(self, client):
        res = client.get("/surveys/{sid}/responses".format(sid=objectId_str("survey000003")))
        # print res.data
        assert_survey_results_page(self, res)

    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_get_survey_results_page2(self, client):
        res = client.get("/surveys/{sid}/responses".format(sid=objectId_str("survey000001")))

        assert_survey_results_page(self, res)

    #participant privilege (forbidden)
    @with_login(user2["email_address"], user2["real_pass"])
    def test_get_survey_results_page_forbidden(self, client):
        res = client.get("/surveys/{sid}/responses".format(sid=objectId_str("survey000002")))

        self.assertEqual(res.status_code, 403)
        assert_not_survey_results_page(self, res)
        assert_403_page(self, res)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_get_survey_results_invalid(self, client):
        res = client.get("/surveys/{sid}/responses".format(sid=objectId_str("surveyxxxx03")))

        assert_not_survey_results_page(self, res)
        self.assertEqual(res.status_code, 404)
        assert_404_page(self, res)

class DeleteSurveys(PliEntireDbTestCase):
    #admin
    @with_login(user1["email_address"], user1["real_pass"])
    def test_delete_survey_succes1(self, client):
        survey_count = get_db().surveys.count()
        sid = objectId_str(ex.survey1["_id"])
        path = "/surveys/{sid}".format(sid=sid)

        res = client.delete(path)
        self.assertEqual(get_db().surveys.count(), survey_count - 1)
        self.assertEqual(0, get_db().responses.find({"survey_id": sid}).count())
        assert_404_page(self, client.get(path))

        #editor
    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_delete_survey_success2(self, client):
        survey_count = get_db().surveys.count()
        sid = objectId_str(ex.survey3["_id"])
        path = "/surveys/{sid}".format(sid=sid)

        res = client.delete(path)
        self.assertEqual(get_db().surveys.count(), survey_count - 1)
        self.assertEqual(0, get_db().responses.find({"survey_id": sid}).count())
        assert_404_page(self, client.get(path))

    #participant (forbidden)
    @with_login(user2["email_address"], user2["real_pass"])
    def test_delete_survey_fail1(self, client):
        survey_count = get_db().surveys.count()
        sid = objectId_str(ex.survey2["_id"])
        path = "/surveys/{sid}".format(sid=sid)

        res = client.delete(path)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(get_db().surveys.count(), survey_count)


    #not logged in
    @with_test_client
    def test_delete_survey_fail2(self, client):
        survey_count = get_db().surveys.count()
        sid = objectId_str(ex.survey2["_id"])
        path = "/surveys/{sid}".format(sid=sid)

        res = client.delete(path)
        self.assertEqual(survey_count, get_db().surveys.count())
        assert_redirect_page(self, res)

    #admin
    @with_login(user1["email_address"], user1["real_pass"])
    def test_delete_survey_question_success1(self, client):
        question_count = get_db().survey_questions.count()
        qid = objectId_str(ex.survey_question5["_id"])
        path = "/surveys/questions/{qid}".format(qid=qid)
        res = client.delete(path)
        self.assertEqual(get_db().survey_questions.count(), question_count - 1)

    #editor
    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_delete_survey_question_succes2(self, client):
        question_count = get_db().survey_questions.count()
        qid = objectId_str(ex.survey_question5["_id"])
        path = "/surveys/questions/{qid}".format(qid=qid)
        res = client.delete(path)
        self.assertEqual(get_db().survey_questions.count(), question_count - 1)

    #On a survey
    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_delete_survey_question_fail3(self, client):
        question_count = get_db().survey_questions.count()
        qid = objectId_str(ex.survey_question2["_id"])
        path = "/surveys/questions/{qid}".format(qid=qid)
        res = client.delete(path)

        self.assertEqual(get_db().survey_questions.count(), question_count)
        self.assertEqual(res.status_code, 400)

    #participant (forbidden)
    @with_login(user2["email_address"], user2["real_pass"])
    def test_delete_survey_question_fail1(self, client):
        question_count = get_db().survey_questions.count()
        qid = objectId_str(ex.survey_question5["_id"])
        path = "/surveys/questions/{qid}".format(qid=qid)

        res = client.delete(path)
        self.assertEqual(get_db().survey_questions.count(), question_count)
        self.assertEqual(res.status_code, 403)

    #not logged in
    @with_test_client
    def test_delete_survey_question_fail2(self, client):
        question_count = get_db().survey_questions.count()
        qid = objectId_str(ex.survey_question5["_id"])
        path = "/surveys/questions/{qid}".format(qid=qid)

        res = client.delete(path)
        self.assertEqual(get_db().survey_questions.count(), question_count)
        assert_redirect_page(self, res)
