from data_gathering.data_aggregator import DataAggregator

data_aggregator = DataAggregator()

handle = "etsu"

tweets_data_frame = data_aggregator.get_tweets_data_frame(handle)
for tweets in tweets_data_frame:
	print(tweets)
	# todo: store data into sqlite database from data frame
