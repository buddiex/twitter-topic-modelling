import csv

import gensim


class TopicClassifier:
	def __init__(self, model_location: str):
		# Load pre-trained Word2Vec model.
		self.model = gensim.models.KeyedVectors.load_word2vec_format(model_location, binary=True)

	def get_topic(self, aggregate_of_words: list):
		most_common_word = None
		best_similarity = 0
		for word in aggregate_of_words:
			most_similar_to_other_words = 0
			for other_topic in aggregate_of_words:
				# compare against everything but yourself
				if word != other_topic:
					try:
						similarity = self.model.similarity(word, other_topic)
						# update most similar word
						if similarity > most_similar_to_other_words:
							most_similar_to_other_words = similarity
					except KeyError:
						# if the word does not exist in the model, then simply skip that word
						continue
			# update the best word that is most common if applicable
			if most_similar_to_other_words > best_similarity:
				best_similarity = most_similar_to_other_words
				most_common_word = word

		return most_common_word


# get the list of topics derived from Osas's data
topicClassifier = TopicClassifier('./model/GoogleNews-vectors-negative300.bin')

with open('./data/user_topics.csv', 'r') as user_topics_file:
	file_contents = csv.reader(user_topics_file, delimiter=',')
	for row in file_contents:
		print(topicClassifier.get_topic(row[4].split()))

