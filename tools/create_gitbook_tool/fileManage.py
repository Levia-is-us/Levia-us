from azure.storage.blob import BlobServiceClient, ContentSettings
import os
import sys
from dotenv import load_dotenv
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)


class file_manage:
    def __init__(self, azure_file_server_key):
        # azure blob service client
        self.blob_service_client = BlobServiceClient.from_connection_string(azure_file_server_key)
        # azure blob container client
        self.container_client = self.blob_service_client.get_container_client('pet-public')

    def upload_file(self,markdown_content,article_title):
        get_file_name= str(article_title) +'.md'
        blob_client = self.container_client.get_blob_client(get_file_name)
        blob_client.upload_blob(markdown_content, overwrite=True)
        if not blob_client.url:
            return 'Upload file failed! please check your file server connection!'

        return {
            "url":blob_client.url,
            "name":get_file_name
        }

    def delete_file(self,blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()






