import pandas as pd
import plotly.graph_objects as go

i_df = pd.read_csv("i_df.csv")
r_df = pd.read_csv("r_df.csv")
t_df = pd.read_csv("t_df.csv")

r_df["date"] = pd.to_datetime(r_df["date"],format = "%Y-%m-%d")
i_df["date"] = pd.to_datetime(i_df["date"],format = "%Y-%m-%d")
t_df["date"]  = pd.to_datetime(t_df["date"],format = "%a %b %d %H:%M:%S +0000 %Y")

i_df.columns = ['title', 'date', 'rating', 'text', 'found_helpful', 'label', 'score']
r_df.columns = ['date', 'text', 'label', 'score']


combined = pd.concat([i_df[["date","text","label","score"]],r_df[["date","text","label","score"]],t_df[["date","text","label","score"]]]).reset_index(drop=True)

combined = combined.assign(date=combined.date.dt.round('d'))
u_score = [x["score"]*-1  if x["label"]=="NEGATIVE" else x["score"] for x in  combined.to_dict(orient = "records")]
combined["score"] = u_score


time_list = []
for day in combined.date.unique():
    score = combined[combined.date == day].score.mean()
    time_list.append({
        "date":day,
        "score":score
    })

time_df = pd.DataFrame(time_list).sort_values(by = "date").reset_index(drop = True)


from scipy import signal

time_df.to_csv("time_df.csv",index = False)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = time_df.date,
        y = time_df.score ,
        fill='tozeroy'
    )
)


fig.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import string
import nltk
import re

wn = nltk.WordNetLemmatizer()
stopword = nltk.corpus.stopwords.words('english')
stopword.append("rt")

def clean_text(text):
    text  = "".join([char.lower() for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    text = re.split('\W+', text)
    text = [word for word in text if word not in stopword]
    text = [wn.lemmatize(word) for word in text]
    return " ".join(text)



t1 = [clean_text(x) for x in combined[~(combined.label == "NEGATIVE")].text]

wordcloud=WordCloud(max_font_size=50, max_words=100, background_color="white").generate(" ".join(t1))

plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

list_of_list_of_tokens = [x.split(" ") for x in t1]
from gensim import corpora, models
dictionary_LDA = corpora.Dictionary(list_of_list_of_tokens)
dictionary_LDA.filter_extremes(no_below=15, no_above=0.5, keep_n=10000)
corpus = [dictionary_LDA.doc2bow(token_list) for token_list in list_of_list_of_tokens]

import time

num_topics = 10
lda_model = models.LdaModel(corpus, num_topics=num_topics, \
                                  id2word=dictionary_LDA, \
                                  passes=4, alpha=[0.01]*num_topics, \
                                  eta=[0.01]*len(dictionary_LDA.keys()))

for i,topic in lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=10):
    print(str(i)+": "+ topic)
    print()

import graphlab as gl
import pyLDAvis
import pyLDAvis.graphlab
import pyLDAvis.gensim

vis = pyLDAvis.gensim.prepare(topic_model=lda_model, corpus=corpus, dictionary=dictionary_LDA)

pyLDAvis.save_html(vis, 'lda.html')