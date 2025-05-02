import re
import pandas as pd
def preprocess(data):
    pattern="\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    message=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    fi_data=pd.DataFrame({'user_message':message,'message_date':dates})
    fi_data["message_date"]=pd.to_datetime(fi_data["message_date"],format="%d/%m/%Y, %H:%M - ")
    fi_data.rename(columns={'message_date':'date'},inplace=True)
    user=[]
    messages=[] 
    for message in fi_data["user_message"]:
        entry=re.split("([\w\W]+?):\s",message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2]) 
        else:
            user.append("group_notification")
            messages.append(entry[0]) 
    fi_data["user"]=user
    fi_data["message"]=messages 
    fi_data=fi_data.drop(columns=["user_message"],axis=1)
    fi_data["months_dates"]=fi_data["date"].dt.month
    fi_data["year"]=fi_data["date"].dt.year
    fi_data["month"]=fi_data["date"].dt.month_name()
    fi_data["day"]=fi_data["date"].dt.day
    fi_data["hour"]=fi_data["date"].dt.hour
    fi_data["minute"]=fi_data["date"].dt.minute
    fi_data["only_dates"]=fi_data["date"].dt.date
    fi_data["day_name"]=fi_data["date"].dt.day_name()
    
    
    return fi_data