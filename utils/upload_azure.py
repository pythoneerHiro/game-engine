import json
from os import environ

from azure.storage.blob import BlobServiceClient
from icecream import ic

storage_account_key = environ["storage_account_key"]
storage_account_name = environ["storage_account_name"]

connection_string = json.loads(environ["connection_string"])
container_name = environ["container_name"]


def uploadAzureBlobStorage(file_path, file_name) -> str:
    ic(connection_string)
    ic(container_name)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
        ic(f"uploaded {file_name}.")
    return blob_client.url
