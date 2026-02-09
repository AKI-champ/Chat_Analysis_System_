import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

# -------------------- SETUP --------------------
st.set_page_config(page_title="Chat Analysis System", layout="wide")
extractor = URLExtract()

# -------------------- PREPROCESS FUNCTION --------------------
def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) == 0:
        return pd.DataFrame()

    df = pd.DataFrame({
        "user_message": messages,
        "date": dates
    })

    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y, %H:%M - ", errors="coerce")

    users = []
    texts = []

    for msg in df["user_message"]:
        split = re.split(r"^([^:]+):\s", msg)
        if len(split) > 2:
            users.append(split[1])
            texts.append(split[2])
        else:
            users.append("group_notification")
            texts.append(msg)

    df["user"] = users
    df["message"] = pd.Series(texts).astype(str)
    df.drop(columns=["user_message"], inplace=True)

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["only_dates"] = df["date"].dt.date
    df["day_name"] = df["date"].dt.day_name()

    return df


# -------------------- HELPER FUNCTIONS --------------------
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


def monthly_timeline(selected_user, df):
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


def day_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_df = df.groupby("day_name")["message"].count().reset_index()
    day_df["day_name"] = pd.Categorical(day_df["day_name"], categories=order, ordered=True)
    return day_df.sort_values("day_name")


def wordcloud_func(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    text = " ".join(df["message"].astype(str))
    wc = WordCloud(width=600, height=600, background_color="white")
    return wc.generate(text if text.strip() else "No Data")


def emoji_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for msg in df["message"].astype(str):
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(), columns=["Emoji", "Count"])


# -------------------- STREAMLIT UI --------------------
st.sidebar.title("Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp chat (.txt)", type="txt")

if uploaded_file:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocess(data)

    if df.empty:
        st.error("❌ Chat format not supported or file is empty.")
        st.stop()

    users = df["user"].unique().tolist()
    if "group_notification" in users:
        users.remove("group_notification")
    users.sort()
    users.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", users)

    if st.sidebar.button("Show Analysis"):
        st.title("📊 Chat Analysis System")

        num_msgs, words, media, links = fetch_stats(selected_user, df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Messages", num_msgs)
        c2.metric("Words", words)
        c3.metric("Media", media)
        c4.metric("Links", links)

        st.subheader("Monthly Activity")
        mt = monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(mt["time"], mt["message"])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.subheader("Weekly Activity")
        wd = day_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(wd["day_name"], wd["message"])
        st.pyplot(fig)

        st.subheader("Word Cloud")
        wc = wordcloud_func(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        st.subheader("Emoji Analysis")
        emoji_df = emoji_analysis(selected_user, df)
        st.dataframe(emoji_df)
