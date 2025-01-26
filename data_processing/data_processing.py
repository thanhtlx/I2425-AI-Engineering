from data_processing.data_filtering.filter import filter
from data_processing.data_cleaning.clean import clean
from data_processing.data_augmentation.augmentate import augmentate
from data_processing.feature_engineering.feature_eng import feature_engineering


def process_training_data(data):
    # TODO: DATA: raw dataframe
    # 1: filtering
    # 2: clean
    # 3: augmentation
    # 4: feature engineering
    data = filter(data)
    data = clean(data)
    data = augmentate(data)
    # feature
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
