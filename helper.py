from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()


# -------------------- BASIC STATS --------------------
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # Force message column to string (CRITICAL FIX)
    df["message"] = df["message"].astype(str)

    num_messages = df.shape[0]

    words = []
    links = []

    for message in df["message"]:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))

    media_messages = df[
        df["message"].str.contains("<Media omitted>", na=False)
    ].shape[0]

    return num_messages, len(words), media_messages, len(links)


# -------------------- MOST ACTIVE USERS --------------------
def chart(df):
    user_counts = df["user"].value_counts().head()

    percentage_df = (
        (df["user"].value_counts(normalize=True) * 100)
        .round(2)
        .reset_index()
    )
    percentage_df.columns = ["Name", "Percentage"]

    return user_counts, percentage_df


# -------------------- WORD CLOUD --------------------
def workcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    df["message"] = df["message"].astype(str)

    temp = df[~df["message"].str.contains("<Media omitted>", na=False)]

    text = " ".join(temp["message"])

    if not text.strip():
        return WordCloud(background_color="white").generate("No Data")

    wc = WordCloud(
        width=600,
        height=600,
        background_color="white",
        min_font_size=10
    )

    return wc.generate(text)


# -------------------- EMOJI ANALYSIS --------------------
def emojies(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    df["message"] = df["message"].astype(str)

    emojis = []
    for message in df["message"]:
        emojis.extend([char for char in message if char in emoji.EMOJI_DATA])

    return pd.DataFrame(
        Counter(emojis).most_common(),
        columns=["Emoji", "Count"]
    )


# -------------------- MONTHLY TIMELINE --------------------
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


# -------------------- DAILY TIMELINE --------------------
def dates_timelines(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df.groupby("only_dates")["message"].count().reset_index()


# -------------------- WEEKLY ACTIVITY --------------------
def day_timelines(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    day_df = df.groupby("day_name")["message"].count().reset_index()
    day_df["day_name"] = pd.Categorical(
        day_df["day_name"], categories=order, ordered=True
    )

    return day_df.sort_values("day_name")


# -------------------- YEARLY ACTIVITY --------------------
def year_timelines(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df.groupby("year")["message"].count().reset_index()
