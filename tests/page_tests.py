
def check_page(expected_content, *name):
    
    def _check_page(f, r, *msg):
        if hasattr(r, 'data'):
            data = r.data
        else:
            data = r
        for s in expected_content:
            f(s in data, *msg)

    def assert_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertTrue, r, str(name[0]))
        else:
            _check_page(tr.assertTrue, r)
            
    def assert_not_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertFalse, r, "Not " + str(name[0]))
        else:
            _check_page(tr.assertFalse, r)

    return assert_page, assert_not_page

assert_index_page, assert_not_index_page = check_page(["Index-Page"],"index")
assert_login_page, assert_not_login_page = check_page(["Email Address","Login","Password"], "login")
assert_res_page, assert_not_res_page = check_page(["Resources-Page"], "resources")
assert_surv_page, assert_not_surv_page = check_page(["Survey-Page"], "surveys")
assert_mail_sent_page, assert_not_mail_sent_page = check_page(["Reg-Email-Sent"], "mail-sent")
assert_reg_page, assert_not_reg_page = check_page(["Reg-Page"], "register-page")
assert_alr_reg_page, assert_not_alr_reg_page = check_page(["Already-Reg"], "alr-reg")
assert_bad_vtok_page, assert_not_bad_vtok_page = check_page(["Failed-Token-Valid"], "bad-token-page")
assert_good_vtok_page, assert_not_good_vtok_page = check_page(["Good-Token-Valid"], "good-valid-tok")
assert_correct_page, assert_not_correct_page = check_page(["Correct!"], "correct")
assert_wrong_page, assert_not_wrong_page = check_page(["Wrong!"], "wrong")

