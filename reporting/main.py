import pandas as pd

from wordcloud import WordCloud

from config import db_conn

import matplotlib.pyplot as plt

# Load in the dataframe
all_topics = ""

topics_query = "select * from topics"

# get topics from database
topics = pd.read_sql(topics_query, db_conn)

for topic in topics.values:
    all_topics += "" + topic[3] + " "

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(all_topics)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


