from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobServiceClient
import os
import math
import Domain.FileInfo as fileInfo
from pathlib import Path

MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=devmakstorage;AccountKey=PgdSHyWamCSNWJWc51tQ/VUONoqGLL0x++ruDHCYT/bLFqwFS8tDZRmZ747DSQ8/4+vnWOh879bkvcXnHjY/Uw==;EndpointSuffix=core.windows.net"
MY_BLOB_CONTAINER = "assets"



class AzureHandler(object):
    def __init__(self):
        print("Initializing BlobExample")
        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
        self.my_container = self.blob_service_client.get_container_client(MY_BLOB_CONTAINER)
        self.LOCAL_BLOB_PATH = "r" + os.path.dirname(os.path.abspath(__file__))


    def save_blob(self, file_name, file_content):
        # Get full path to the file
        download_file_path = os.path.join(self.LOCAL_BLOB_PATH, file_name)

        # for nested blobs, create local path as well!
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

        with open(download_file_path, "wb") as file:
            file.write(file_content)

    def download_file(self, file):
        try:
            print("Downloading file " + file)
            download_file_path = os.path.join(self.LOCAL_BLOB_PATH, file)
            os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
            bytes = self.my_container.get_blob_client(file).download_blob().readall()

            with open(download_file_path, "wb") as file:
                file.write(bytes)

            blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client("assets", os.path.basename(file))
            with open(file, "wb") as download_file:
                download_file.write(blob_client.download_blob())
        except Exception as e:
            print(e)

    def download_all_blobs_in_container(self):
        my_blobs = self.my_container.list_blobs()
        for blob in my_blobs:
            print(blob.name)
            bytes = self.my_container.get_blob_client(blob).download_blob().readall()
            self.save_blob(blob.name, bytes)

    def uploadfile(self, file):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
            # Here we split and use only the name of the file so it doesn't create folders and subfolders in azure
            blob_client = blob_service_client.get_blob_client(MY_BLOB_CONTAINER, os.path.basename(file))
            print("Uploading to azure as blob: " + file)

            with open(file, "rb") as data:
                blob_client.upload_blob(data)
        except Exception as e:
            print(e)


    def getFileNames(self):

        # Instantiate a new ContainerClient
        blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(MY_BLOB_CONTAINER)
        try:
            filenames = []
            files = container_client.list_blobs()
            for file in files:
                fileI = fileInfo.FileInfo(file.name,file.creation_time.strftime("%Y/%m/%d %H:%M:%S"),self.convert_size(file.size),file.content_settings['content_type'])
                filenames.append(fileI)
            return filenames
        except Exception as e:
            print(e)
            return None



    def showFiles(self):

        # Instantiate a new ContainerClient
        blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(MY_BLOB_CONTAINER)

        try:
            # List containers in the storage account
            list_response = blob_service_client.list_containers()
            print("\nListing blobs...")
            blob_list = container_client.list_blobs()
            for blob in blob_list:
                print("\t" + blob.name)
        except Exception as e:
            print(e)

    def getRootPath(self):
        return os.path.dirname(os.path.abspath(__file__))

    def convert_size(self,size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])



if __name__ == '__main__':

    blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(MY_BLOB_CONTAINER)
    container_client.list_blobs()