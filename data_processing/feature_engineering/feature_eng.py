import pandas as pd


def feature_engineering(df):
    columns = [
        "trans_date_trans_time",
        "merchant",
        "category",
        "amt",
        "gender",
        "lat",
        "long",
        "city_pop",
        "job",
        "unix_time",
        "merch_lat",
        "merch_long",
    ]
    if "label" in df.columns:
        columns.append("label")
    print(df.head(1))
    df = df[columns]
    print(df["trans_date_trans_time"])
    df["month"] = pd.to_datetime(df["trans_date_trans_time"]).dt.month
    df["day"] = pd.to_datetime(df["trans_date_trans_time"]).dt.day
    df["year"] = pd.to_datetime(df["trans_date_trans_time"]).dt.year
    df["normalized_amt"] = (df["amt"] - df["amt"].min()) / (
        df["amt"].max() - df["amt"].min()
    )
    return df
