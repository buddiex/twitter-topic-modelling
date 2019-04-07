from user import Handle
from data_collection_service import DataCollectionService
import pandas as pd
import preprocessor as p


def aggregage_user_data(user: str) -> pd.DataFrame:
	target_user = Handle(user)
	dc = DataCollectionService()

	targets_followers = dc.get_users_followers(screen_name=target_user.username, count=5)
	df = pd.DataFrame(
		columns=["followers_screen_name", "tweet_text", "harsh_tags", "user_description", "followers_description",
				 "friends_description", "mentions_descriptions", "retweeted_descriptions"])

	tweets_df = pd.DataFrame(columns=["followers_screen_name", "tweets"])

	for follower in targets_followers:
		tweets_data = dc.get_aggregate_timeline_text(follower, 200)
		friends_ids = dc.get_users_friends(user_id=follower)
		followers_ids = dc.get_users_followers(user_id=follower)
		user_description = dc.get_users_descriptions(user_ids=[follower])
		friends_description = dc.get_users_descriptions(user_ids=friends_ids) if friends_ids else ""
		followers_description = dc.get_users_descriptions(user_ids=followers_ids) if followers_ids else ""
		mentions_descriptions = dc.get_users_descriptions(
			screen_names=tweets_data.mentions) if tweets_data.mentions else ""
		retweeted_descriptions = dc.get_users_descriptions(
			screen_names=tweets_data.handles_retweeted) if tweets_data.handles_retweeted else ""
		print("Getting data for : " + str(tweets_data.screen_name) + " Total tweets: " + str(len(tweets_data.tweets)))
		df = df.append({
			"followers_screen_name": tweets_data.screen_name,
			"tweet_text": tweets_data.tweet_text,
			"harsh_tags": " ".join(tweets_data.hashtags),
			"user_description": " ".join(user_description),
			"followers_description": " ".join(followers_description),
			"friends_description": " ".join(friends_description),
			"mentions_descriptions": " ".join(mentions_descriptions),
			"retweeted_descriptions": " ".join(retweeted_descriptions)}, ignore_index=True)
		for tweet in tweets_data.tweets:
			tweets_df = tweets_df.append({
				"followers_screen_name": tweets_data.screen_name,
				"tweets": tweet
			}, ignore_index=True)
		df.to_csv("tweets_info.csv")
		tweets_df.to_csv("tweets_standalone.csv")
	return df


def preprocess(df):
	df.apply(p.clean)
	df.to_csv("perprocessed_tweets_info.csv")


user = "etsu"
aggregage_user_data(user)
# df = pd.read_csv("tweets_info.csv")
# preprocess(df)
