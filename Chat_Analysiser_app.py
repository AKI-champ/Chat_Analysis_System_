import streamlit as st
import Chat_Analysis
import helper
import matplotlib.pyplot as plt

st.sidebar.title("User")
uploaded_file = st.sidebar.file_uploader("Choose the file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = Chat_Analysis.preprocess(data)

    user_list = df["user"].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Members name", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Chat Analysis System")

        num_messages, words, number_of_media_messages, links = helper.fetch_stats(
            selected_user, df
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(number_of_media_messages)

        with col4:
            st.header("Total Links Shared")
            st.title(links)

        # Monthly Activity
        st.title("Monthly Activity")
        monthly_timeline = helper.monthly_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline["time"], monthly_timeline["message"], color="green")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Daily Activity
        st.title("Activity Dates")
        date_timeline = helper.dates_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(date_timeline["only_dates"], date_timeline["message"], color="green")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Weekly Activity
        st.title("Activity Days")
        day_timeline = helper.day_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(day_timeline["day_name"], day_timeline["message"], color="green")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Yearly Activity
        st.title("Activity Year")
        year_timeline = helper.year_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(year_timeline["year"], year_timeline["message"], color="green")
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # Overall User Analysis
    if selected_user == "Overall":
        st.title("Most Active Users")
        x, per = helper.chart(df)

        col5, col6 = st.columns(2)

        with col5:
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color="green")
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col6:
            st.dataframe(per)

    # Word Cloud
    st.title("Word Cloud")
    wc = helper.workcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)

    # Emoji Analysis
    st.title("Emojis Used")
    emoji_df = helper.emojies(selected_user, df)

    col7, col8 = st.columns(2)

    with col7:
        st.dataframe(emoji_df)

    with col8:
        fig, ax = plt.subplots()
        ax.bar(emoji_df["Emoji"], emoji_df["Count"], color="green")
        ax.set_xlabel("Emoji")
        ax.set_ylabel("Count")
        ax.set_title("Emoji Frequency")
        st.pyplot(fig)
