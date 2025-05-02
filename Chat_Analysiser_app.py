import streamlit as st
import Chat_Analysis,helper
import matplotlib.pyplot as plt
st.sidebar.title("User")
uploaded_file=st.sidebar.file_uploader("Choose the file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=Chat_Analysis.preprocess(data)
    
    
    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Members name ",user_list)
    if st.sidebar.button("Show Analysis"):
        
        num_messages,words,number_of_media_messages,links=helper.fetch_stats(selected_user,df)
        st.title("Chat_Analysis_System")
        col1,col2,col3,col4=st.columns(4)
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
            
        st.title("Monthly Activity")
        monthly_timeline=helper.monthly_timelines(selected_user,df)
        fi,ax=plt.subplots()
        ax.plot(monthly_timeline["time"],monthly_timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fi)
        
        st.title("Activity Dates")
        dates_timeline=helper.dates_timelines(selected_user,df)
        fi,ax=plt.subplots()
        ax.plot(dates_timeline["only_dates"],dates_timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fi)
        
        st.title("Activity Days")
        day_timeline=helper.day_timelines(selected_user,df)
        fi,ax=plt.subplots()
        ax.bar(day_timeline["day_name"],day_timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fi)
        
        st.title("Activity Year")
        year_timeline=helper.year_timelines(selected_user,df)
        fi,ax=plt.subplots()
        ax.bar(year_timeline["year"],year_timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fi)
        
            
    if selected_user=="Overall":
        st.title("The most activated user")
        x,per=helper.chart(df)
        fi,ax=plt.subplots()
        
        col5,col6=st.columns(2) 
        with col5:
            x.plot.bar(x.index,x.values,color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fi)
        with col6:
            st.dataframe(per)
           
    st.title("Work_cloud")    
    df_wc=helper.workcloud(selected_user,df)
    fi,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fi)

      
    emojies_data=helper.emojies(selected_user,df)
    plt.rcParams['font.family'] = 'Segoe UI Emoji'
    st.title("Emojies Used")
    col7,col8=st.columns(2)
    with col7:
        st.dataframe(emojies_data)
    with col8:
        st.title("Emoji Usage Histogram")
        fig, ax = plt.subplots()
        ax.bar(
            emojies_data["Emoji"],
            emojies_data["Count"],
            color='green'
    )
    ax.set_xlabel("Emoji")
    ax.set_ylabel("Count")
    ax.set_title("Emoji Frequency")
    plt.xticks(rotation="horizontal")  
    st.pyplot(fig)