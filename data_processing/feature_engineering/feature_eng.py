import pandas as pd
from sklearn.preprocessing import LabelEncoder


def feature_engineering(df):
    try:
        df.drop(
            columns=[
                "Unnamed: 0",
                "cc_num",
                "first",
                "last",
                "street",
                "city",
                "state",
                "zip",
                "dob",
                "trans_num",
                "trans_date_trans_time",
            ],
            inplace=True,
        )
    except:
        pass
    encoder = LabelEncoder()
    print("columns", df.columns)
    df["merchant"] = encoder.fit_transform(df["merchant"])
    df["category"] = encoder.fit_transform(df["category"])
    df["gender"] = encoder.fit_transform(df["gender"])
    df["job"] = encoder.fit_transform(df["job"])
    return df
