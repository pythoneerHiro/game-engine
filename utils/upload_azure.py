def uploadAzureBlobStorage(bucketName: str, file: str) -> str:
    pass


from azure.storage.blob import BlobServiceClient

storage_account_key = "RfkDC1yVo40Wiixh6QkrH4hqm7gWPsx8b9F+WWIu1yONJLDReaA+EkdbCdR/lnNER4Prvx80Hp9w+AStNp4eqQ=="
storage_account_name = "bzdevstorageaccount"
connection_string = "DefaultEndpointsProtocol=https;AccountName=bzdevstorageaccount;AccountKey=RfkDC1yVo40Wiixh6QkrH4hqm7gWPsx8b9F+WWIu1yONJLDReaA+EkdbCdR/lnNER4Prvx80Hp9w+AStNp4eqQ==;EndpointSuffix=core.windows.net"
container_name = "game-engine"


def uploadAzureBlobStorage(file_path, file_name) -> str:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
        print(f"Uploaded {file_name}.")
    return blob_client.url
