import pandas as pd
from model_training.utils.get_data_frame import get_data_frame
from model_training.utils.save_model import save_model
from model_training.utils.model import get_model
from model_training.validation.validation import validate
from data_processing.data_processing import process_training_data
from model_training.utils import autogluon_model

pd.options.mode.copy_on_write = True
import dagshub
import mlflow
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    filename="app.log",  # File to write logs to
    filemode="a",  # Append to the file (use 'w' to overwrite)
)
logger = logging.getLogger(__name__)


dagshub_token = os.getenv("DAGSHUB_TOKEN")
dagshub.auth.add_app_token(dagshub_token)  # Authenticate using the token
dagshub.init(
    repo_owner="vrykolakas166",
    repo_name="fraud-detection-model-versioning",
    mlflow=True,
)
mlflow_registry_uri = (
    "https://dagshub.com/vrykolakas166/fraud-detection-model-versioning.mlflow"
)


# INPUT train
def train(data_dir):
    # load data
    logger.info("Starting training: " + data_dir)
    df_train = get_data_frame(data_dir + "/train.csv")
    df_test = get_data_frame(data_dir + "/test.csv")

    # preproces data
    logger.info("Processing training data: " + str(df_train.shape))
    train_data = process_training_data(df_train)

    logger.info("Done processing training data: " + str(df_train.shape))
    # Set the MLflow registry URI
    mlflow.set_registry_uri(mlflow_registry_uri)
    # remove the AutogluonModels directory
    autogluon_model.clean_up()

    with mlflow.start_run():
        # TODO: tuning, analysis loss
        logger.info("Get auto model: ")
        model = get_model(
            "auto",
        )
        logger.info("Starting training model")
        model.fit(train_data=train_data)
        # TODO: actionale inside
        logger.info("Evaluate  model")
        metrics = validate(model, df_test)
        logger.info("Save  model")
        url = save_model(model)

        mlflow.log_param("best_model_by_validation_score", model.model_best)
        # Log metrics
        mlflow.log_metrics(metrics)

        # Log the model
        mlflow.log_artifact(autogluon_model.folder_path)
        mlflow.log_artifact(url)

    print(url, metrics)
    return url, metrics


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="data")
    args = parser.parse_args()
    train(args.data_dir)
