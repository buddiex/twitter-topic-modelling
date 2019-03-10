from typing import List
from config import twitter


def get_user_timeline(username: str):
    results = twitter.statuses.user_timeline(screen_name=username)
    for status in results:
        print([status["created_at"],
               status["text"].encode("ascii", "ignore"),
               [i["text"] for i in status["entities"]["hashtags"]],
               [i["screen_name"] for i in status["entities"]["user_mentions"]]
               ]
              )


def get_users_following(username: str, numbers: int = 100) -> List:
    query = twitter.friends.ids(screen_name=username)
    return list(map (str, query["ids"][:numbers]))


def get_users_followers(username: str, numbers: int) -> List:
    query = twitter.followers.ids(screen_name=username)
    return list(map(str, query["ids"][:numbers]))


def get_user_description(username: str) -> str:
    return get_users_descriptions([username])[0]['description']


def get_users_descriptions(usernames: List) -> List:
    result = twitter.users.lookup(user_id=','.join(usernames))
    return [res['description'] for res in result]


user = 'omigie'
# get_user_timeline(user)
users = get_users_followers(user, 100)
for i in get_users_descriptions(users):
    print (i)
