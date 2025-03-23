from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
# Auth
first_account_name = os.getenv("AccountName1")
first_account_key = os.getenv("AccountKey1")
second_account_name = os.getenv("AccountName2")
second_account_key = os.getenv("AccountKey2")
connect_str1 = f"DefaultEndpointsProtocol=https;AccountName={first_account_name};AccountKey={first_account_key};EndpointSuffix=core.windows.net"
connect_str2 = f"DefaultEndpointsProtocol=https;AccountName={second_account_name};AccountKey={second_account_key};EndpointSuffix=core.windows.net"
container_name = "blobcontainer"


# Creating Azure clients
blob_service_client_Source = BlobServiceClient.from_connection_string(connect_str1)
blob_service_client_Destination = BlobServiceClient.from_connection_string(connect_str2)
container_clientSource = blob_service_client_Source.get_container_client(container_name)
container_clientDestination = blob_service_client_Destination.get_container_client(container_name)


# Creating container if it doesn't exist
def create_container(client):
    try:
        # container_client.create_container()
        client.create_container()
        print(f'account {client} has been created')
    except Exception:
        print(f"container creation has failed. Check if it already exists")

# Create and upload blobs to account1
def create_and_upload_blobs(blob_service_client):
    data = 0
    try:
        while data < 100:
            blob_name = f"blob{data}.txt"
            # blob_client = blob_service_client_Source.get_blob_client(container=container_name, blob=blob_name)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            blob_client.upload_blob(blob_name)
            data += 1
            print(f"blob number {data} have been uploded")
    except Exception:
        print("Uploading blob has failed")


create_container(container_clientSource)
create_container(container_clientDestination)
# Get source and destination container clients
source_container_client = blob_service_client_Source.get_container_client(container_name)
dest_container_client = blob_service_client_Destination.get_container_client(container_name)

# Copying the files from the first account to the second
def copy_blobs_to_second_account(sourceAccountName, sourceContainerName):
    try:
        
        for blob in source_container_client.list_blobs():
            
            source_blob_url = f"https://{sourceAccountName}.blob.core.windows.net/{sourceContainerName}/{blob.name}"
            print(source_blob_url)
            print(blob)
            # Get destination blob client
            dest_blob_client = dest_container_client.get_blob_client(blob.name)
            print(dest_blob_client)

            # Start copy operation
            copy_operation = dest_blob_client.start_copy_from_url(source_blob_url)
            print(f"Copying {blob.name} - Status: {copy_operation['copy_status']}")
        print("please be silent")
    except Exception:
        print("Something went wrong during copy")


create_and_upload_blobs(blob_service_client_Source)
copy_blobs_to_second_account(first_account_name, container_name)