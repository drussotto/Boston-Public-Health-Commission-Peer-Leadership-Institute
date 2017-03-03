from pli import validate_login, PliUser
from pli_test_case import PliTestCase, PliUsersTestCase, PliQotdTestCase, PliEntireDbTestCase
from context_decorators import with_login, with_test_client, with_app_ctxt
from users_examples import *
from questions_examples import *
from page_tests import *
from post_utils import *


# Provides the PliUsers instance for the given uid, the returned user is
# not "authenticated", meaning they can't be used were auth is required, they
# are only for comparison.
def get_u(uid):
    return PliUser(uid, False)

def get_db_mock_initializers():
    return [add_mocked_users, add_mocked_questions]
