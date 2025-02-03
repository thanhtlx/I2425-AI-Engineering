from model_training.train import train
from model_training.utils import autogluon_model
from utils import DagsHubStorageBucket
from datetime import datetime


class TrainingPipeline:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.sb = DagsHubStorageBucket()

    def run(self, data_dir):
        try:
            model_file, _ = train(data_dir)

            ## output model is going to dagshub storage bucket
            zip_path = self.sb.zip_file(
                folder_path=autogluon_model.folder_path,
                output_name=autogluon_model.folder_path,
            )

            self.sb.upload_file(
                zip_path,
                f"final_model/{self.timestamp}/{autogluon_model.folder_path}.zip",
                False,
            )

            self.sb.upload_file(
                model_file, f"final_model/{self.timestamp}/model.pkl", False
            )

        except Exception as e:
            raise e


if __name__ == "__main__":
    tp = TrainingPipeline()
    data_dir = "data"
    tp.sb.download_file(f"{data_dir}/test.csv")
    tp.sb.download_file(f"{data_dir}/train.csv")
    tp.run(data_dir)
