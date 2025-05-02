from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor=URLExtract()

def fetch_stats(selected_user, df):
    if selected_user == "Overall":
        num_messages = df.shape[0]

        words = []
        for message in df["message"]:
            words.extend(message.split())
        
        links=[]
        for message in df["message"]:
            links.extend(extractor.find_urls(message))

        number_of_media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]

    else:
        df = df[df["user"] == selected_user]
        num_messages = df.shape[0]

        words = []
        for message in df["message"]:
            words.extend(message.split())

        number_of_media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]
        
        links=[]
        for message in df["message"]:
            links.extend(extractor.find_urls(message))

    return num_messages, len(words), number_of_media_messages,len(links)


def chart(df):
    x=df["user"].value_counts().head()
    per=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"Percentage","user":"Name"})
    return x,per


def workcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    text = df["message"].dropna().str.cat(sep=" ")
    
    if not text.strip(): 
        raise ValueError("No valid text found to generate a word cloud.")
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(text)
    return df_wc


def emojies(selected_user,df):
    if selected_user !="Overall":
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_counts = Counter(emojis)  
    most_common_emojis = emoji_counts.items() 
    emojies_data = pd.DataFrame(list(most_common_emojis), columns=['Emoji', 'Count'])
    return emojies_data

def monthly_timelines(selected_user,df):
    if selected_user !="Overall":
        df = df[df['user'] == selected_user]
    monthly_timeline=df.groupby(["year","months_dates","month"])["message"].count().reset_index()
    time=[]
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline["month"][i]+"-"+str(monthly_timeline["year"][i]))
    monthly_timeline["time"]=time
    return monthly_timeline

def dates_timelines(selected_user,df):
    if selected_user !="Overall":
        df = df[df['user'] == selected_user]
    
    dates_timeline=df.groupby("only_dates")["message"].count().reset_index()
    return dates_timeline
    
    
def day_timelines(selected_user,df):
    if selected_user !="Overall":
        df = df[df['user'] == selected_user]
        
    day_timeline= df.groupby("day_name")["message"].count().reset_index()
    return day_timeline

def year_timelines(selected_user,df):
    if selected_user !="Overall":
        df = df[df['user'] == selected_user]
    year_timeline= df.groupby("year")["message"].count().reset_index()
    return year_timeline
    
    
       