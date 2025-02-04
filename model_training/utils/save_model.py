from joblib import dump
import os


def save_model(model, out_dir="output/model.pkl"):
    dir_path = os.path.dirname(out_dir)
    # Check if the directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    model.save()
    # dump(model, out_dir)
    return out_dir
