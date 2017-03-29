from .whats_new_card_examples import *
from .users_examples import *
from .questions_examples import *
from .survey_examples import *
from .blog_page_examples import *

def get_db_mock_initializers():
    return [add_mocked_users,
            add_mocked_questions,
            add_mocked_wn_cards,
            add_mocked_survey_questions,
            add_mocked_surveys,
            add_mocked_responses,
            add_mocked_blogs]
