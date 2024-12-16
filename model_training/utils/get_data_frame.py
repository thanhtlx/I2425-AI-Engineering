import pandas as pd


def get_data_frame(file_url):
    df = pd.read_csv(file_url)
    return df
