from data_processing.data_filtering.filter import filter
from data_processing.data_cleaning.clean import clean
from data_processing.data_augmentation.augmentate import augmentate
from data_processing.feature_engineering.feature_eng import feature_engineering

import logging

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    filename="app.log",  # File to write logs to
    filemode="a",  # Append to the file (use 'w' to overwrite)
)
logger = logging.getLogger(__name__)


def process_training_data(data):
    # TODO: DATA: raw dataframe
    # 1: filtering
    # 2: clean
    # 3: augmentation
    # 4: feature engineering
    logger.info("Filtering data")
    data = filter(data)
    logger.info("Cleaning data")
    data = clean(data)
    data = augmentate(data)
    # feature
    logger.info("Feature engineering data")

    data = feature_engineering(data)
    # X = data.drop(columns=["label"], inplace=False)
    # Y = data["label"]
    return data


def process_testing_data(data):
    # TODO: DATA: raw dataframe
    # 2: clean
    # 4: feature engineering
    data = clean(data)
    data = feature_engineering(data)
    if "label" in data.columns:
        X = data.drop(columns=["label"], inplace=False)
        Y = data["label"]
        return X, Y
    else:
        return data, []
