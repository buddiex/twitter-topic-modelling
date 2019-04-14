from data_gathering.handle import Handle
from data_gathering.data_collection_service import DataCollectionService
import pandas as pd
from config import db_conn


def add_follower(screen_name):
    sql = '''INSERT INTO followers (screen_name) VALUES("{}")'''.format(screen_name)
    cur = db_conn.cursor()
    cur.execute(sql)
    db_conn.commit()
    return cur.lastrowid


def aggregage_user_data(user: str) -> pd.DataFrame:
    target_user = Handle(user)
    dc = DataCollectionService()

    targets_followers = dc.get_users_followers(screen_name=target_user.username, count=5)
    tweets_df = pd.DataFrame(columns=["text", "followers_id"])

    for follower in targets_followers:
        tweets_data = dc.get_aggregate_timeline_text(follower, 500)
        print("Getting data for : " + str(tweets_data.screen_name) + " Total tweets: " + str(len(tweets_data.tweets)))
        follow_id = add_follower(tweets_data.screen_name)
        for tweet in tweets_data.tweets:
            tweets_df = tweets_df.append({
                "text": tweet,
                "followers_id": follow_id
            }, ignore_index=True)

        tweets_df.to_sql("tweets", db_conn, if_exists="append", index=False)

    return tweets_df


user = "etsu"
aggregage_user_data(user)
