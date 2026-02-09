from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    df["message"] = df["message"].astype(str)

    num_messages = df.shape[0]

    words, links = [], []
    for msg in df["message"]:
        words.extend(msg.split())
        links.extend(extractor.find_urls(msg))

    media_msgs = df[df["message"].str.contains("<Media omitted>", na=False)].shape[0]

    return num_messages, len(words), media_msgs, len(links)


def chart(df):
    counts = df["user"].value_counts().head()
    percent = (df["user"].value_counts(normalize=True) * 100).round(2).reset_index()
    percent.columns = ["Name", "Percentage"]
    return counts, percent


def workcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    text = " ".join(df["message"].astype(str))
    wc = WordCloud(width=600, height=600, background_color="white")
    return wc.generate(text if text.strip() else "No Data")


def emojies(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for msg in df["message"].astype(str):
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(), columns=["Emoji", "Count"])


def monthly_timelines(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = (
        df.groupby(["year", "month_num", "month"])["message"]
        .count()
        .reset_index()
        .sort_values(["year", "month_num"])
    )

    timeline["time"] = timeline["month"] + "-" + timeline["year"].astype(str)
    return timeline


def dates_timelines(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df.groupby("only_dates")["message"].count().reset_index()


def day_timelines(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_day = df.groupby("day_name")["message"].count().reset_index()
    df_day["day_name"] = pd.Categorical(df_day["day_name"], categories=order, ordered=True)
    return df_day.sort_values("day_name")


def year_timelines(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df.groupby("year")["message"].count().reset_index()
