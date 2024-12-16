import pandas as pd


def filter(df):
    df.drop_duplicates(inplace=True)
    df.dropna(ignore_index=True)

    return df
