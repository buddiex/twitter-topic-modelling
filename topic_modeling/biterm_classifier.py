import re
import nltk
import string
import sqlite3
import stop_words
import wordsegment
import numpy as np
import pandas as pd
import preprocessor as p
from config import db_conn
from textblob import Word
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from biterm.btm import oBTM
from biterm.utility import vec_to_biterms, topic_summuary  # helper functions

wordsegment.load()
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

stop_words = stop_words.get_stop_words('en') + nltk.corpus.stopwords.words('english')
stop_words = list(set(list(ENGLISH_STOP_WORDS) + stop_words + list(string.ascii_lowercase)))
lemmatizer = WordNetLemmatizer()

wordNet_lemmatizer = lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()])
texblob_lemmatizer = lambda x: " ".join([Word(word).lemmatize() for word in x.split()])

db_conn =  sqlite3.connect('../database.db')


def segment_harsh_tags(tags):
    return " ".join([" ".join(wordsegment.segment(t)) for t in str(tags).split(" ")])


def remove_links(tweet):
    tweet = re.sub(r'http\S+', ' ', tweet)  # remove http links
    tweet = re.sub(r'bit.ly/\S+', ' ', tweet)  # rempve bitly links
    tweet = tweet.strip('[link]')  # remove [links]
    return tweet


def remove_users(tweet):
    tweet = re.sub(r'(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', ' ', tweet)  # remove retweet
    tweet = re.sub(r'(@[A-Za-z]+[A-Za-z0-9-_]+)', ' ', tweet)  # remove tweeted at
    return tweet


def clean_tweets(tweet):
    tweet = remove_users(tweet)
    tweet = remove_links(tweet)
    tweet = tweet.encode('ascii', 'ignore').decode('ascii')  # remove emojis
    tweet = tweet.lower()  # lower case
    tweet = re.sub(r'[' + string.punctuation + ']+', ' ', tweet)  # strip punctuation
    tweet = re.sub(r'\s+', ' ', tweet)  # remove double spacing
    tweet = re.sub(r'([0-9]+)', '', tweet)  # remove numbers
    #     tweet = wordNet_lemmatizer(tweet)
    tweet_token_list = [word for word in tweet.split(' ') if
                        word not in stop_words and len(word) > 2]  # remove stopwords
    tweet = ' '.join(tweet_token_list)
    tweet = p.clean(tweet)
    return tweet


def get_users_topics(texts, num_topics=10):
    vec = CountVectorizer(stop_words='english')  # vectorize texts
    X = vec.fit_transform(texts).toarray()
    vocab = np.array(vec.get_feature_names())  # get vocabulary
    biterms = vec_to_biterms(X)  # get biterms
    btm = oBTM(num_topics=num_topics, V=vocab)  # create btm

    print("Train Online BTM ..")
    for i in range(0, len(biterms), 100):  # prozess chunk of 200 texts
        biterms_chunk = biterms[i:i + 100]
        btm.fit(biterms_chunk, iterations=50)
    topics = btm.transform(biterms)
    summary = topic_summuary(btm.phi_wz.T, X, vocab, num_topics, verbose=False)
    return [t.argmax() for t in topics], summary


def update_table_tweets_table(df):
    df.to_sql('temp_table', db_conn, if_exists='replace')

    sql = """update tweets
             set topics = (select temp_table.topics from temp_table 
                              where temp_table.id = tweets.id )
            """
    cur = db_conn.cursor()
    cur.execute(sql)
    db_conn.commit()


followers_df = pd.read_sql("select * from followers", db_conn)
for index, row in followers_df.iterrows():
    follower_screen_name = row['screen_name']
    sql = "select * from tweets where follower_id='{}'".format(row['id'])
    texts_df = pd.read_sql(sql, db_conn)

    texts_df['clean_tweets'] = texts_df['text'].map(clean_tweets)
    texts_df['topics'] = ''
    user_topics_df = pd.DataFrame(columns=["follower_topic_index", "words", "category"])
    print("processing for user:{} with {} tweets".format(follower_screen_name, len(texts_df)))
    text = list(texts_df['clean_tweets'])
    # actual topic modelling
    if text:
        topics, summary = get_users_topics(text, num_topics=10)
        for i in range(len(summary['coherence'])):
            user_topics_df = user_topics_df.append({
                "follower_id": row['id'],
                "follower_topic_index": i,
                "words": " ".join(summary['top_words'][i])
            },
                ignore_index=True)
        user_topics_df.to_sql("topics", db_conn, if_exists="append", index=False)
        texts_df['topics'] = topics
        update_table_tweets_table(texts_df)
