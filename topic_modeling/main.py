import csv
from topic_modeling.biterm_classifier import traing_top_model

from topic_modeling.topic_classifier import TopicClassifier

# get the list of topics derived from Osas's data
# topicClassifier = TopicClassifier('./model/GoogleNews-vectors-negative300.bin')
#
# with open('./data/user_topics.csv', 'r') as user_topics_file:
# 	file_contents = csv.reader(user_topics_file, delimiter=',')
# 	for row in file_contents:
# 		print(topicClassifier.get_topic(row[4].split()))


traing_top_model()