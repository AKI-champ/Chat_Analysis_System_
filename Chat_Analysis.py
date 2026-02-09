import re
import pandas as pd

def preprocess(data):
    # Android WhatsApp format with AM/PM
    pattern = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) == 0:
        return pd.DataFrame()

    df = pd.DataFrame({
        "user_message": messages,
        "date": dates
    })

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d/%m/%y, %I:%M %p - ",
        errors="coerce"
    )

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
