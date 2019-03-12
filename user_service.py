from typing import List
import tweepy
from config import api
from user import User


class UserService:
    def __init__(self, user: User):
        self.user = user

    def get_user_timeline(self) -> List[List]:
        return [[status.full_text.encode("ascii", "ignore"),
                 [i["text"] for i in status.entities["hashtags"]],
                 [i["screen_name"] for i in status.entities["user_mentions"]]]
                for status in
                tweepy.Cursor(api.user_timeline, screen_name=self.user.username, tweet_mode="extended").items(10)
                ]

    def get_users_following(self, number_of_followers: int = 100) -> List:
        query = api.friends.ids(screen_name=self.user.username)
        return list(map(str, query["ids"][:number_of_followers]))

    def get_users_followers(self, number_of_followers: int) -> List:
        query = api.followers.ids(screen_name=self.user.username)
        return list(map(str, query["ids"][:number_of_followers]))

    def get_user_description(self) -> str:
        return self.__get_users_descriptions([self.user.username])[0]['description']

    def get_followers_descriptions(self, number_of_followers) -> List:
        usernames = self.get_users_followers(number_of_followers)
        return self.__get_users_descriptions(usernames)

    @staticmethod
    def __get_users_descriptions(usernames: List) -> List:
        result = api.users.lookup(user_id=','.join(usernames))
        return [res['description'] for res in result]
