def clean(df):
    # TODO: normalize, v.v
    # rename label columns
    df = df.rename(columns={"is_fraud": "label"})
    df["trans_date_trans_time"] = df["trans_date_trans_time"].fillna("0000-00-00")
    df["merchant"] = df["merchant"].fillna('Unknown')
    df["category"] = df["category"].fillna("Unknown")
    df["amt"] = df["amt"].fillna(0)
    df["gender"] = df["gender"].fillna("Unknown")
    df["lat"] = df["lat"].fillna(0)
    df["long"] = df["long"].fillna(0)
    df["city_pop"] = df["city_pop"].fillna(0)
    df["job"] = df["job"].fillna("Unknown")
    df["unix_time"] = df["unix_time"].fillna(0)
    df["merch_lat"] = df["merch_lat"].fillna(0)
    df["merch_long"] = df["merch_long"].fillna(0)
    return df
