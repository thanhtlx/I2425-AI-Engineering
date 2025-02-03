from google.cloud import storage
import os
import shutil

class GCSStorageBucket:
    def __init__(self, bucket_name):
        """
        Initializes the GCSStorageBucket instance.

        :param bucket_name: The name of the Google Cloud Storage bucket.
        """
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, local_path, remote_path):
        """
        Uploads a file to the Google Cloud Storage bucket.

        :param local_path: The local path of the file to upload.
        :param remote_path: The remote path in the bucket where the file will be stored.
        """
        blob = self.bucket.blob(remote_path)
        blob.upload_from_filename(local_path)
        print(f"File '{local_path}' uploaded to '{remote_path}'.")
        return remote_path

    def zip_file(self, folder_path, output_name):
        """
        Zips a directory for storage or upload.

        :param folder_path: The directory to zip.
        :param output_name: The output zip file name.
        :return: Path to the zipped file.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"{folder_path} does not exist!")
        
        zip_path = shutil.make_archive(output_name, "zip", folder_path)
        print(f"Zipped {folder_path} to {zip_path}")
        return zip_path

    def download_file(self, remote_path, local_path):
        """
        Downloads a file from the Google Cloud Storage bucket.

        :param remote_path: The remote path of the file in the bucket.
        :param local_path: The local path where the file will be stored.
        """
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        blob = self.bucket.blob(remote_path)
        blob.download_to_filename(local_path)
        print(f"File '{remote_path}' downloaded to '{local_path}'.")
        return local_path

    def remove_file(self, remote_path):
        """
        Removes a file from the Google Cloud Storage bucket.

        :param remote_path: The remote path of the file in the bucket.
        """
        blob = self.bucket.blob(remote_path)
        blob.delete()
        print(f"File '{remote_path}' has been deleted successfully.")
