class Handle():
    def __init__(self, username):
        self.username = username


class TweetDataAggregator:

    def __init__(self):
        self.hashtags = []
        self.mentions = []
        self.handles_retweeted = []
        self.tweet_text = ''
        self.screen_name = ''
        self.tweets = []

    def parse(self, tweet):
        if "quoted_status" in tweet:
            quoted_tweet = tweet["quoted_status"]
            self.handles_retweeted.append(quoted_tweet["user"]["screen_name"])
            self.__retrieve_data(quoted_tweet)

        if "retweeted_status" in tweet:
            tweet = tweet["retweeted_status"]
            self.handles_retweeted.append(tweet["user"]["screen_name"])

        self.__retrieve_data(tweet)

    def __retrieve_data(self, tweet):
        self.hashtags.extend([i["text"] for i in tweet["entities"]["hashtags"]])
        self.mentions.extend([i["screen_name"] for i in tweet["entities"]["user_mentions"]])
        self.tweet_text += tweet["full_text"] + " "
        self.tweets.append(tweet["full_text"])
