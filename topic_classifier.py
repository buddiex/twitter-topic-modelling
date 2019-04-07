from gensim.models import Word2Vec


class TopicClassifier:
	def __init__(self, vectorized_model: Word2Vec, aggregate_of_words: list):
		self.model = vectorized_model
		self.aggregate_of_words = aggregate_of_words

	def get_topic(self):
		most_common_word = None
		best_similarity = 0
		for word in self.aggregate_of_words:
			most_similar_to_other_words = 0
			for other_topic in self.aggregate_of_words:
				# compare against everything but yourself
				if word != other_topic:
					similarity = self.model.similarity(word, other_topic)
					# update most similar word
					if similarity > most_similar_to_other_words:
						most_similar_to_other_words = similarity
			# update the best word that is most common if applicable
			if most_similar_to_other_words > best_similarity:
				best_similarity = most_similar_to_other_words
				most_common_word = word

		return most_common_word
