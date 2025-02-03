import pandas as pd


def filter(df):
    df.drop_duplicates(inplace=True)

    # Convert "amt" to float (handle non-numeric values safely)
    df["amt"] = pd.to_numeric(df["amt"], errors="coerce")

    df.dropna(ignore_index=True, inplace=True)

    df = df[df["amt"] > 0]  # amount > 0
    return df
