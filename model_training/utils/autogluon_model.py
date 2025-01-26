import shutil

folder_path = "AutogluonModels"


def clean_up():
    # Remove the AutogluonModels directory
    shutil.rmtree(folder_path, ignore_errors=True)
