import inspect

# This function returns a 2-tuple where the first element is a unit test for the positive result,
# and the second is a unit test for the negative result. The expected_content is what determines
# whether the result is "positive" or not.
# expected_content should be a list of strings which can be found
# in a HTTP response, if any of the strings aren't found in a given response,
# the test is considered negative
# The last argument is an optional name for the test.
def check_page(expected_content, *name):

    def _check_page(f, d, *msg):
        for s in expected_content:
            f(s in d, *msg)

    def assert_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertTrue, r.data, str(name[0]))
        else:
            _check_page(tr.assertTrue, r.data)

    def assert_not_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertFalse, r.data, "Not " + str(name[0]))
        else:
            _check_page(tr.assertFalse, r.data)

    return assert_page, assert_not_page

# These are some of the page tests we've already made.
assert_index_page, assert_not_index_page = check_page(["Index-Page"],"index")
assert_login_page, assert_not_login_page = check_page(["Email","Password"], "login")
assert_res_page, assert_not_res_page = check_page(["Resources-Page"], "resources")
assert_surv_page, assert_not_surv_page = check_page(["Survey-Page"], "surveys")
assert_mail_sent_page, assert_not_mail_sent_page = check_page(["Reg-Email-Sent"], "mail-sent")
assert_reg_page, assert_not_reg_page = check_page(["Reg-Page"], "register-page")
assert_alr_reg_page, assert_not_alr_reg_page = check_page(["Already-Reg"], "alr-reg")
assert_bad_vtok_page, assert_not_bad_vtok_page = check_page(["Failed-Token-Valid"], "bad-token-page")
assert_good_vtok_page, assert_not_good_vtok_page = check_page(["Good-Token-Valid"], "good-valid-tok")
assert_correct_page, assert_not_correct_page = check_page(["Correct!"], "correct")
assert_incorrect_page, assert_not_incorrect_page = check_page(["Wrong!"], "wrong")
assert_404_page, assert_not_404_page = check_page(["Sorry, there's nothing here."], "404")
assert_403_page, assert_not_403_page = check_page(["Forbidden"], "403")
assert_create_survey_question_page, assert_not_create_survey_question_page = check_page(["Create a Question"], "create_survey_question")
assert_create_success_page, assert_create_failed_page = check_page(["Submission Successful"], "create post")
assert_response_submitted_page, assert_response_failed_page = check_page(["Submission Successful"], "submit_response")
assert_survey_page, assert_not_survey_page = check_page(["Complete Survey"], "get_survey")
assert_survey_results_page, assert_not_survey_results_page = check_page(["Total responses for this survey"], "survey_results")
assert_redirect_page, assert_not_redirect_page = check_page(["Redirecting"], "redirect")
assert_logout_in_index, assert_not_logout_in_index = check_page(["Logout"], "index")
assert_login_in_index, assert_not_login_in_index = check_page(["Login"], "index")
assert_admin_dropdown_visible, assert_not_admin_dropdown_visible = check_page(["Admin"], "index")
assert_editor_dropdown_visible, assert_not_editor_dropdown_visible = check_page(["Manage", "Users"], "index")
assert_peerleader_resources_visible, assert_not_peerleader_resources_visible = check_page(["Peer Leader Resources"], "index")
assert_pass_reset_success, assert_not_pass_reset_success = check_page(["reset"], "pass reset")
