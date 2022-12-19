import json
from os import environ

from azure.storage.blob import BlobServiceClient, ContentSettings
from icecream import ic

storage_account_key = environ["storage_account_key"]
storage_account_name = environ["storage_account_name"]

connection_string = json.loads(environ["connection_string"])
container_name = environ["container_name"]


def uploadAzureBlobStorage(file_path, file_name, content_type="application/octet-stream") -> str:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    with open(file_path, "rb") as data:
        content_settings = ContentSettings(content_type=content_type)
        # ic(f'setting the content type : {content_type}')
        blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
        ic(f"uploaded {file_name}.")
    return blob_client.url
