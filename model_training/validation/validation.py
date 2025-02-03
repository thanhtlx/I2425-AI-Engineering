from model_training.validation.metrics.calc_metrics import calc_metrics

from data_processing.data_processing import process_testing_data


def validate(model, df_test):
    X_test, Y_test = process_testing_data(df_test)
    Y_pred = model.predict(X_test)
    metrics = calc_metrics(Y_test, Y_pred)
    return metrics
