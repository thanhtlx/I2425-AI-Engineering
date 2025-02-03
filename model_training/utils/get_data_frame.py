import pandas as pd


def get_data_frame(file_url):
    # df = pd.read_csv(file_url)

    # TESTING: Read the first 10,000 rows
    df = pd.read_csv(file_url, nrows=15000)

    return df
