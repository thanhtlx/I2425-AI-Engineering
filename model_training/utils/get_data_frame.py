import pandas as pd


def get_data_frame(file_url):
    # df = pd.read_csv(file_url)
    # test pipeline flow
    df = pd.read_csv(file_url, nrows=50000)
    return df
