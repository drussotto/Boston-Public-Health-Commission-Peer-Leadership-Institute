from .whats_new_card_examples import *
from .users_examples import *
from .questions_examples import *


def get_db_mock_initializers():
    return [add_mocked_users,
            add_mocked_questions,
            add_mocked_wn_cards]
