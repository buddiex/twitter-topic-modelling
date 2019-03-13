from typing import List
import tweepy
from tweepy.models import Status

from config import api
from user import TweetDataAggregator


class DataCollectionService:

    def get_aggregate_timeline_text(self, user_id, count: int = 100) -> TweetDataAggregator:
        tweet_data = TweetDataAggregator()

        for tweet_obj in self.get_data(api.user_timeline, user_id, count):
            tweet_data.parse(tweet_obj._json)

        return tweet_data

    def get_user_timeline(self, user_id: str, count: int = 100) -> List[List]:
        return [[tweet.full_text.encode("ascii", "ignore"),
                 [i["text"] for i in tweet._json['entities']["hashtags"]],
                 [i["screen_name"] for i in tweet.entities["user_mentions"]]]
                for tweet in
                self.get_data(api.user_timeline, user_id, count)
                ]

    def get_data(self, endpoint: str, user_id, count=100) -> List[Status]:
        try:
            return tweepy.Cursor(endpoint, screen_name=user_id, tweet_mode="extended").items(count)
        except Exception as e:
            raise

    def get_users_friends(self, user_id: str, count: int = 100) -> List[str]:
        query = self.get_data(api.friends_ids, user_id, count)
        return list(map(str, query))

    def get_users_followers(self, user_id: str, count: int = 100) -> List[str]:
        query = self.get_data(api.followers_ids, user_id, count)
        return list(map(str, query))

    def get_users_descriptions(self, users_ids: List) -> List[str]:
        if len(users_ids) == 1:
            return [api.get_user(users_ids[0]).description]
        else:
            return [user.description for user in api.lookup_users(users_ids)]
