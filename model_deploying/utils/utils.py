import pandas as pd
from data_processing.data_processing import process_testing_data


def process_user_input(body):
    print([body])
    df = pd.DataFrame([body])
    print(df)
    X, Y = process_testing_data(df)
    return X
