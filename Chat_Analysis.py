import re
import pandas as pd

def preprocess(data):
    # Regex pattern for WhatsApp date-time
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        "user_message": messages,
        "message_date": dates
    })

    # Convert date column
    df["message_date"] = pd.to_datetime(
        df["message_date"],
        format="%d/%m/%Y, %H:%M - ",
        errors="coerce"
    )

    df.rename(columns={"message_date": "date"}, inplace=True)

    users = []
    texts = []

    for msg in df["user_message"]:
        split_msg = re.split(r"^([^:]+):\s", msg)
        if len(split_msg) > 2:
            users.append(split_msg[1])
            texts.append(split_msg[2])
        else:
            users.append("group_notification")
            texts.append(msg)

    df["user"] = users
    df["message"] = texts
    df.drop(columns=["user_message"], inplace=True)

    # Time-based features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    df["only_dates"] = df["date"].dt.date
    df["day_name"] = df["date"].dt.day_name()

    return df
