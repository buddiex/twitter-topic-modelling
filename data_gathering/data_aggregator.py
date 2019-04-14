import pandas as pd

from data_gathering.data_collection_service import DataCollectionService

from data_gathering.handle import Handle


class DataAggregator:
	def __init(self):
		self.data_collection_service = DataCollectionService()

	def get_tweets_data_frame(
			self,
			handle: str,
			number_of_followers: int = 5,
			number_of_tweets_per_follower: int = 500
	)-> pd.DataFrame:
		target_user = Handle(handle)

		targets_followers = self.data_collection_service.get_users_followers(
			screen_name=target_user.username,
			count=number_of_followers
		)

		tweets_df = pd.DataFrame(columns=["followers_screen_name", "tweets"])

		for follower in targets_followers:
			tweets_data = self.data_collection_service.get_aggregate_timeline_text(
				follower,
				number_of_tweets_per_follower
			)
			for tweet in tweets_data.tweets:
				tweets_df = tweets_df.append({
					"followers_screen_name": tweets_data.screen_name,
					"tweets": tweet
				}, ignore_index=True)

		return tweets_df
