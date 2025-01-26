import pandas as pd


def filter(df):
    df.drop_duplicates(inplace=True)
    df.dropna(ignore_index=True)
    df = df[df["amt"] > 0]  # amount > 0
    return df
