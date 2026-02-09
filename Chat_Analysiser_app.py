import streamlit as st
import matplotlib.pyplot as plt
import Chat_Analysis
import helper

st.set_page_config(page_title="Chat Analysis System", layout="wide")

st.sidebar.title("Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp chat (.txt)", type="txt")

if uploaded_file:
    data = uploaded_file.getvalue().decode("utf-8")
    df = Chat_Analysis.preprocess(data)

    if df.empty:
        st.error("Chat format not supported.")
        st.stop()

    users = df["user"].unique().tolist()
    if "group_notification" in users:
        users.remove("group_notification")

    users.sort()
    users.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", users)

    if st.sidebar.button("Show Analysis"):
        st.title("📊 Chat Analysis System")

        num, words, media, links = helper.fetch_stats(selected_user, df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Messages", num)
        c2.metric("Words", words)
        c3.metric("Media", media)
        c4.metric("Links", links)

        st.subheader("Monthly Activity")
        mt = helper.monthly_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(mt["time"], mt["message"])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.subheader("Weekly Activity")
        wd = helper.day_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(wd["day_name"], wd["message"])
        st.pyplot(fig)

        st.subheader("Word Cloud")
        wc = helper.workcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        st.subheader("Emoji Analysis")
        st.dataframe(helper.emojies(selected_user, df))
