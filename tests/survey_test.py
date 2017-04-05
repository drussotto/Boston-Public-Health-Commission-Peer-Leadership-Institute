from testlib import *
from datetime import date
from bson import ObjectId

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
            "survey_question1": 1,
            "survey_question2": 2,
            "survey_question3": 4,
            "survey_question4": 3,
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
            "questions": ["survey_question1", "survey_question3"]
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_success_page(self, res)

    #editor privilege
    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_create_valid_survey_success2(self, client):
        form_data = {
            "name": "NewSurvey1",
            "questions": ["survey_question1", "survey_question3"]
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_success_page(self, res)

    #participant privilege (forbidden)
    @with_login(user2["email_address"], user2["real_pass"])
    def test_create_valid_survey_failure1(self, client):
        form_data = {
            "name": "NewSurvey1",
            "questions": ["survey_question1", "survey_question3"]
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_failed_page(self, res)
        self.assertEqual(403, res.status_code)

    @with_test_client
    def test_create_valid_survey_failure1(self, client):
        form_data = {
            "name": "NewSurvey1",
            "questions": ["survey_question1", "survey_question3"]
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_failed_page(self, res)
        assert_redirect_page(self, res)

    #No name for the survey
    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_invalid_survey1(self, client):
        form_data = {
            "name": "",
            "questions": ["survey_question1", "survey_question3"]
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_failed_page(self, res)

    #No questions on the survey
    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_invalid_survey2(self, client):
        form_data = {
            "name": "NewSurvey1"
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_failed_page(self, res)

    #invalid question id
    @with_login(user1["email_address"], user1["real_pass"])
    def test_create_survey_bad_qid(self, client):
        form_data = {
            "name": "some name",
            "questions": ["survey_question1", "survey_questionIAMNOTREAL"]
        }

        res = client.post("/surveys/create", data=form_data)
        assert_create_failed_page(self, res)

class RetrieveResponsesTest(PliEntireDbTestCase):
    @with_app_ctx
    def test_retrieve_response_data(self):
        """
        {
            "sid": "survey000003",
            "questions": [
                {
                    "question": "When did you last...",
                    "answers": [
                        {
                            "answer": "Within the past week",
                            "answered": 25
                        }
                        ...
                    ]
                }
                ...
            ]
        }
        """
        response_data = retrieve_response_data(objectId_str("survey000003"))
        self.assertEqual(len(response_data["questions"]), 4)
        self.assertEqual(len(response_data["questions"][0]["answers"]), 4)
        self.assertEqual(response_data["questions"][0]["answers"])[0]["answered"], 100) ##?
        self.assertEqual(response_data["questions"][0]["answers"])[0]["answer"], "Within the past week")


    @with_login(user1["email_address"], user1["real_pass"])
    def test_get_survey_results_page1(self, client):
        res = client.get("/surveys/{sid}/results".format(sid=objectId_str("survey000003")))

        assert_surveys_results_page(self, res)

    @with_login(user_editor["email_address"], user_editor["real_pass"])
    def test_get_survey_results_page2(self, client):
        res = client.get("/surveys/{sid}/results".format(sid=objectId_str("survey000001")))

        assert_surveys_results_page(self, res)

    #participant privilege (forbidden)
    @with_login(user2["email_address"], user2["real_pass"])
    def test_get_survey_results_page_forbidden(self, client):
        res = client.get("/surveys/{sid}/results".format(sid=objectId_str("survey000002")))

        self.assertEqual(res.status_code, 404)
        assert_not_surveys_results_page(self, res)
        assert_404_page(self, res)

    @with_login(user1["email_address"], user1["real_pass"])
    def test_get_survey_results_invalid(self, client):
        res = client.get("/surveys/{sid}/results".format(sid=objectId_str("surveyxxxx03")))

        assert_not_surveys_results_page(self, res)
        self.assertEqual(res.status_code, 404)
        assert_404_page(self, res)


#Allows for prettier object ids, represented as a string
def objectId_str(name):
    return str(ObjectId(name))
