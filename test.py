import pytest

from user import Handle
from data_collection_service import DataCollectionService

user = Handle("omigie")
user_service = DataCollectionService()
count = 10


@pytest.fixture()
def target_handle_followers():
    return user_service.get_users_followers(user.username, count)


def test_get_aggregate_timeline_text():
    all_txt = user_service.get_aggregate_timeline_text(user.username)
    print(all_txt)


def test_get_user_timeline():
    content_returned_test(user_service.get_user_timeline(user.username, count))


def test_get_users_followers(target_handle_followers):
    content_returned_test(target_handle_followers)


def test_get_users_friends():
    content_returned_test(user_service.get_users_friends(user.username, count))


def test_get_one_user_description():
    des = user_service.get_users_descriptions([user.username])
    # assert "State" in des[0]


def test_get_bulk_user_description(target_handle_followers):
    users = target_handle_followers
    des = user_service.get_users_descriptions(users)
    content_returned_test(des)


def content_returned_test(rtn):
    print(rtn)
    lent = len(rtn)
    assert (lent == count)

# def test_get_users_following():
#     lent = len(user_service.get_users_friends())
#     assert (lent > 0)
