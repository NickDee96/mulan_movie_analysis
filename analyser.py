import pandas as pd
import tensorflow as tf
#from transformers import pipeline

from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup



r_df = pd.read_csv("rotten_tomatoes.csv")
i_df = pd.read_csv("imdb.csv")
t_df = pd.read_csv("twitter.csv")




r_df["date"] = pd.to_datetime(r_df["date"],format = "%B %d, %Y")
i_df["date"] = pd.to_datetime(i_df["date"],format = "%d %B %Y")
t_df["date"]  = pd.to_datetime(t_df["date"],format = "%a %b %d %H:%M:%S +0000 %Y")


model = pipeline(task = "sentiment-analysis")

model(["I believe I can do it","Oh yes I do"])

vals = model(list(r_df["review"]))

r_df['label'] = [x{"label"} for x in vals]