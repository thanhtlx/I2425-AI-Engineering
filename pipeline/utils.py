from dagshub import get_repo_bucket_client
from dagshub.upload import Repo
from dagshub.streaming import DagsHubFilesystem
import shutil
import os


class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        os.system(command)


class DagsHubStorageBucket:
    def __init__(
        self, user="vrykolakas166", repo_name="fraud-detection-model-versioning"
    ):
        """
        Initializes the DagsHubStorageBucket instance.

        :param user: The username associated with the DagsHub account (default is "vrykolakas166").
        :param repo_name: The repository name in DagsHub (default is "fraud-detection-model-versioning").
        """
        self.user = user
        self.repo_name = repo_name
        self.repos = Repo(user, repo_name)
        self.fs = DagsHubFilesystem(
            ".", repo_url=f"https://dagshub.com/{user}/{repo_name}"
        )
        self.boto_client = get_repo_bucket_client(f"{user}/{repo_name}", flavor="boto")

    def upload_file(self, local_path, remote_path, enable_versioning=True):
        """
        Uploads a file to the DagsHub repository storage.

        :param local_path: The local path of the file to upload.
        :param remote_path: The remote path where the file will be stored in the repository.
        :param enable_versioning: If True, enables DVC versioning for the uploaded files.
        """

        # self.boto_client.upload_file(
        #     Bucket=self.repos,  # name of the repo
        #     Filename=local_path,  # local path of file to upload
        #     Key=remote_path,  # remote path where to upload the file
        # )
        if enable_versioning:
            self.repos.upload(
                local_path=local_path, remote_path=remote_path, versioning="dvc"
            )
        else:
            self.repos.upload(local_path=local_path, remote_path=remote_path)

        print(f"File '{local_path}' uploaded to '{remote_path}'.")

        return remote_path

    def zip_file(self, folder_path, output_name):
        """
        Zips the directory for storage or upload.

        Args:
            folder_path (str): The directory.
            output_name (str): The output zip file name.

        Returns:
            str: Path to the zipped file.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"{folder_path} does not exist!")

        zip_path = shutil.make_archive(output_name, "zip", folder_path)
        print(f"Zipped {folder_path} to {zip_path}")

        return zip_path

    def download_file(self, remote_path):
        """
        Downloads a file from the DagsHub repository storage.

        :param remote_path: The path of the file to download from the repository.
        :param local_path: The local path where the file will be stored.
        """
        # Ensure the local directory exists
        local_dir = os.path.dirname(remote_path)
        os.makedirs(
            local_dir, exist_ok=True
        )  # Creates the directory if it doesn't exist

        # Download the file
        # print("Downloading data from dagshub s3...")
        # self.boto_client.download_file(
        #     Bucket=self.repos,  # name of the repo
        #     Key=remote_path,  # remote path of file to download
        #     Filename=local_path,  # local path where to download the file
        # )

        # Open the file using the already initialized filesystem
        with self.fs.open(remote_path, "r"):
            # Read or process the file as needed
            pass

        print(f"File '{remote_path}' was downloaded.")
        return remote_path

    def remove_file(self, remote_path):
        """
        Removes a file from the DagsHub repository storage.

        :param remote_path: The path of the file to delete in the repository.
        """
        try:
            # Delete the file from the repository bucket
            self.boto_client.delete_object(Bucket=self.repos, Key=remote_path)
            print(f"File '{remote_path}' has been deleted successfully.")
        except Exception as e:
            print(f"Error occurred while deleting the file: {e}")
