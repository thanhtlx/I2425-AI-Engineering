import pandas as pd
from utils.get_data_frame import get_data_frame
from utils.save_model import save_model
from utils.model import get_model
from validation.validation import validate
from data_processing.data_processing import process_training_data


# INPUT train
def train(data_dir):

    # load data
    df_train = get_data_frame(data_dir + "/train.csv")
    df_test = get_data_frame(data_dir + "/test.csv")

    # preproces data
    X_train, Y_train = process_training_data(df_train)

    # TODO: tuning, analysis loss
    model = get_model("svc")
    model.fit(X_train, Y_train)

    # TODO: actionale inside
    metrics = validate(model, df_test)
    url = save_model(model)

    print(url, metrics)
    return url, metrics


import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="data")
    args = parser.parse_args()
    train(args.data_dir)
