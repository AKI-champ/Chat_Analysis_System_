import streamlit as st
import matplotlib.pyplot as plt
import Chat_Analysis
import helper

st.set_page_config(page_title="Chat Analysis System", layout="wide")

st.sidebar.title("User")
uploaded_file = st.sidebar.file_uploader("Choose a chat file", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = Chat_Analysis.preprocess(data)

    user_list = df["user"].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("📊 Chat Analysis System")

        # ------------------- Stats -------------------
        num_messages, words, media_msgs, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", media_msgs)
        col4.metric("Links Shared", links)

        # ------------------- Monthly Activity -------------------
        st.subheader("Monthly Activity")
        monthly = helper.monthly_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly["time"], monthly["message"])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # ------------------- Daily Activity -------------------
        st.subheader("Daily Activity")
        daily = helper.dates_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily["only_dates"], daily["message"])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # ------------------- Weekly Activity -------------------
        st.subheader("Weekly Activity")
        weekly = helper.day_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(weekly["day_name"], weekly["message"])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # ------------------- Yearly Activity -------------------
        st.subheader("Yearly Activity")
        yearly = helper.year_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(yearly["year"], yearly["message"])
        st.pyplot(fig)

        # ------------------- Overall Analysis -------------------
        if selected_user == "Overall":
            st.subheader("Most Active Users")
            x, per = helper.chart(df)

            col5, col6 = st.columns(2)

            with col5:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col6:
                st.dataframe(per)

        # ------------------- Word Cloud -------------------
        st.subheader("Word Cloud")
        wc = helper.workcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # ------------------- Emoji Analysis -------------------
        st.subheader("Emoji Analysis")
        emoji_df = helper.emojies(selected_user, df)

        col7, col8 = st.columns(2)

        with col7:
            st.dataframe(emoji_df)

        with col8:
            fig, ax = plt.subplots()
            ax.bar(emoji_df["Emoji"], emoji_df["Count"])
            plt.xticks(rotation=45)
            st.pyplot(fig)
