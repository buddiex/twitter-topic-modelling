from typing import List
import tweepy
from tweepy.models import Status

from config import api
from user import TweetDataAggregator


class DataCollectionService:

	def get_aggregate_timeline_text(self, user_id, count: int = 1000) -> TweetDataAggregator:
		tweet_data = TweetDataAggregator()
		tweet_data.screen_name = api.get_user(user_id).screen_name
		for tweet_obj in tweepy.Cursor(api.user_timeline, user_id=user_id, tweet_mode="extended", count=count).items(
				count):
			tweet_data.parse(tweet_obj._json)
		return tweet_data

	def get_users_friends(self, count=50, **kwargs) -> List[str]:
		query = self.get_data(api.friends_ids, count, **kwargs)
		return list(map(str, query))

	def get_users_followers(self, count=50, **kwargs) -> List[str]:
		query = self.get_data(api.followers_ids, count, **kwargs)
		return list(map(str, query))

	@staticmethod
	def get_users_descriptions(**kwargs) -> List[str]:
		return [user.description for user in api.lookup_users(**kwargs)]

	@staticmethod
	def get_data(endpoint: str, count=100, **kwargs) -> List[Status]:
		try:
			return tweepy.Cursor(endpoint, count=5000, **kwargs).items(count)
		except Exception as e:
			raise
