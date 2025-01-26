import pandas as pd
from utils.get_data_frame import get_data_frame
from utils.save_model import save_model
from utils.model import get_model
from validation.validation import validate
from data_processing.data_processing import process_training_data
pd.options.mode.copy_on_write = True
import dagshub
import mlflow
from utils import autogluon_model

dagshub.init(repo_owner='vrykolakas166', repo_name='fraud-detection-model-versioning', mlflow=True)
mlflow_registry_uri = "https://dagshub.com/vrykolakas166/fraud-detection-model-versioning.mlflow"

# INPUT train
def train(data_dir):
    # load data
    df_train = get_data_frame(data_dir + "/train.csv")
    df_test = get_data_frame(data_dir + "/test.csv")

    # preproces data
    train_data = process_training_data(df_train)

    # Set the MLflow registry URI
    mlflow.set_registry_uri(mlflow_registry_uri)
    autogluon_model.clean_up()

    with mlflow.start_run():
        # TODO: tuning, analysis loss
        model = get_model("auto",)
        model.fit(train_data=train_data)
        # TODO: actionale inside
        metrics = validate(model, df_test)
        url = save_model(model)

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log the model
        mlflow.log_artifact(autogluon_model.folder_path)

    print(url, metrics)
    return url, metrics


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="data")
    args = parser.parse_args()
    train(args.data_dir)
