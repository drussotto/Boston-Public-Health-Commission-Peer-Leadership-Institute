from ex_global import ExampleCollection

import __builtin__
__builtin__.ex = ExampleCollection()

import random
import string
from pli import PliUser
from .pli_test_case import PliTestCase, PliUsersTestCase, PliQotdTestCase, PliEntireDbTestCase, PliSurveyQuestionsTestCase, PliSurveysTestCase
from .context_decorators import with_login, with_test_client, with_app_ctxt
from .examples import *
from .page_tests import *
from .post_utils import *

# Provides the PliUsers instance for the given uid, the returned user is
# not "authenticated", meaning they can't be used were auth is required, they
# are only for comparison.
def get_u(uid):
    return PliUser(uid, False)


def rand_string(l):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(l))
