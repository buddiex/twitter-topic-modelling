import pandas as pd
from wordcloud import WordCloud

import matplotlib.pyplot as plt

# Load in the dataframe
df = pd.read_csv("../data/user_topics.csv", index_col=0)
all_topics = ""
for row in df.values:
	all_topics += "" + row[5] + " "

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(all_topics)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
