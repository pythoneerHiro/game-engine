def uploadAzureBlobStorage(bucketName: str, file: str) -> str:
    pass

# from azure.storage.blob import BlobServiceClient
#
# storage_account_key = "GRAB_IT_FROM_AZURE_PORTAL"
# storage_account_name = "GRAB_IT_FROM_AZURE_PORTAL"
# connection_string = "GRAB_IT_FROM_AZURE_PORTAL"
# container_name = "GRAB_IT_FROM_AZURE_PORTAL"
#
# def uploadAzureBlobStorage(file_path,file_name):
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
#     with open(file_path,”rb”) as data:
#         blob_client.upload_blob(data)
#         print(f”Uploaded {file_name}.”)
