import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import json
from collections import Counter
from tqdm import tqdm, tqdm_notebook
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import plotly.graph_objects as go
import time

lang_model = spacy.load("en_core_web_sm")
tqdm.pandas()


def remove_stopwords(text):
    text = lang_model(text)
    processed_text = " ".join(
        [token.text for token in text if token.is_stop != True]
    )
    return processed_text


def remove_punc_special_chars(text):
    text = lang_model(text)
    processed_text = " ".join(
        [
            token.text
            for token in text
            if token.is_punct != True
            and token.is_digit != True
            and token.is_bracket != True
            and token.is_quote != True
            and token.is_currency != True
        ]
    )
    return processed_text


def lemmatize(text):
    text = lang_model(text)
    processed_text = " ".join([word.lemma_ for word in text])
    return processed_text


def remove_additional_special_chars(text):
    unwanted_chars = ["*", "~", "%", "*", '"', "\\n"]
    for i in unwanted_chars:
        text = text.replace(i, "")
        text = text.strip()
    return text


def split_sentences(doc):
    sentences = [s.text.strip() for s in doc.sents]
    return sentences


def vader_score(sentence_list):
    analyzer = SentimentIntensityAnalyzer()
    paragraph_sentiments = 0.0
    avg = -1
    size = len(sentence_list)
    for sentence in sentence_list:
        vs = analyzer.polarity_scores(sentence)
        paragraph_sentiments += vs["compound"]
    if size == 0:
        print("zero")
    else:
        avg = paragraph_sentiments / size
    return avg


def vader_sentiment(compound):
    res = ""
    if compound >= 0.05:
        res = "Positive"
    elif compound <= -0.05:
        res = "Negative"
    else:
        res = "Neutral"
    return res


def sentiment_vader(compound):
    res = ""
    if compound >= 0.05:
        res = "Positive"
    elif compound <= -0.05:
        res = "Negative"
    else:
        res = "Neutral"
    return res


def preprocess_text(df_col):
    print("Removing additional special characters")
    df_col = remove_additional_special_chars(df_col)
    print("Applying spaCy lang model")
    df_col = lang_model(df_col)
    print("Splitting sentences")
    df_col = split_sentences(df_col)
    print("Removing stopwords")
    df_col = [remove_stopwords(i) for i in df_col]
    print("Removing punctuation")
    df_col = [remove_punc_special_chars(i) for i in df_col]
    print("Lemmatizing")
    df_col = [lemmatize(i) for i in df_col]
    return df_col


def weighted_avg(score1, score2):
    weighted_avg = (score1 * 0.4) + (score2 * 0.6)
    return weighted_avg

start_time = time.time()
with open("news_scraped.json") as json_file:
    articles = json.load(json_file)
    articles_list = []
    headings_list = []
    all_news = articles["news_sites"].items()
    for news_site_name, val in all_news:
        for i in val["items"]:
            i["text"] = remove_additional_special_chars(i["text"])
            articles_list.append(i["text"])
            headings_list.append(i["title"])

articles_df = pd.DataFrame(articles_list)
headings_df = pd.DataFrame(headings_list)
articles_df.columns = ["text"]
articles_df.set_index("text")
headings_df.columns = ["headings"]
news_df = pd.concat([headings_df, articles_df], axis=1, join="inner")

print("Preprocessing headings")
news_df["headings"] = news_df["headings"].progress_apply(
    lambda x: preprocess_text(x)
)
print("Preprocessing text")
news_df["text"] = news_df["text"].progress_apply(lambda x: preprocess_text(x))

news_df["vader_compound_heading"] = news_df["headings"].apply(
    lambda x: vader_score(x)
)
news_df["vader_compound_text"] = news_df["text"].apply(
    lambda x: vader_score(x)
)
news_df["vader_sentiment_text"] = news_df["vader_compound_text"].apply(
    lambda x: vader_sentiment(x)
)
news_df["weighted_text_heading_vscore"] = news_df.apply(
    lambda x: weighted_avg(x.vader_compound_heading, x.vader_compound_text),
    axis=1,
)
news_df["vader_sentiment_weighted"] = news_df[
    "weighted_text_heading_vscore"
].apply(lambda x: vader_sentiment(x))

colors = ["gold", "red", "blue"]
fig = px.pie(
    news_df,
    values=news_df["vader_sentiment_text"].value_counts(),
    names=news_df["vader_sentiment_text"].unique(),
    color_discrete_sequence=px.colors.sequential.RdBu,
    title="Distribution of News based on Vader Sentiment (using only text)",
)
fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    textfont_size=20,
    marker=dict(colors=colors, line=dict(color="#000000", width=2)),
)
fig.show()

colors = ["green", "pink", "blue"]
fig = px.pie(
    news_df,
    values=news_df["vader_sentiment_weighted"].value_counts(),
    names=news_df["vader_sentiment_weighted"].unique(),
    color_discrete_sequence=px.colors.sequential.RdBu,
    title="Distribution of News based on Vader Sentiment (using heading and text)",
)
fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    textfont_size=20,
    marker=dict(colors=colors, line=dict(color="#000000", width=2)),
)
fig.show()
print("Time Taken")
print("--- %s seconds ---" % (time.time() - start_time))
