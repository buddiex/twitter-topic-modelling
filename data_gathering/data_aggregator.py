import pandas as pd

from config import db_conn
from data_gathering.data_collection_service import DataCollectionService
from data_gathering.handle import Handle


class DataAggregator:
	def __init__(self):
		self.data_collection_service = DataCollectionService()

	def get_tweets_data_frame(
			self,
			handle: str,
			number_of_followers: int = 5,
			number_of_tweets_per_follower: int = 500
	) -> pd.DataFrame:
		# create handle
		target_user = Handle(handle)

		# get the followers for that handle
		targets_followers = self.data_collection_service.get_users_followers(
			screen_name=target_user.username,
			count=number_of_followers
		)

		# create a data frame for the tweets
		tweets_df = pd.DataFrame(columns=["text", "follower_id"])

		for follower in targets_followers:
			try:
				tweets_data = self.data_collection_service.get_aggregate_timeline_text(
					follower,
					number_of_tweets_per_follower
				)
			except:
				continue

			try:
				if len(tweets_data.tweets) > 0:
					follow_id = self.__add_follower(tweets_data.screen_name)

					for tweet in tweets_data.tweets:
						tweets_df = tweets_df.append({
							"text": tweet,
							"follower_id": follow_id
						}, ignore_index=True)

					tweets_df.to_sql("tweets", db_conn, if_exists="append", index=False)
			except:
				continue

		return tweets_df

	@staticmethod
	def __add_follower(screen_name: str):
		sql = '''INSERT INTO followers (screen_name) VALUES("{}")'''.format(screen_name)
		print(sql)
		cur = db_conn.cursor()
		cur.execute(sql)
		db_conn.commit()
		return cur.lastrowid
