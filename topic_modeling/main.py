from topic_modeling.biterm_classifier import train_topic_model

from config import db_conn
import pandas as pd
from topic_modeling.topic_classifier import TopicClassifier

# train_topic_model()

# topic classification process
topic_classifier = TopicClassifier('../model/GoogleNews-vectors-negative300.bin')

topics_query = "select * from topics"

add_category_query = """
                        update topics
                        set category = '{}'
                        where id = {}
                        """

topics = pd.read_sql(topics_query, db_conn)

for topic in topics.values:
    topic_id = topic[0]
    aggregate_of_topics = topic[2].split()
    category = topic_classifier.get_topic(aggregate_of_topics)
    cur = db_conn.cursor()
    cur.execute(add_category_query.format("test", topic_id))
    print(topic)

db_conn.commit()
