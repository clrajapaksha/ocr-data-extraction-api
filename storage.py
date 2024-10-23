from datetime import datetime, timedelta
from typing import List

from azure.storage.blob import generate_blob_sas, generate_container_sas, BlobSasPermissions, ContainerSasPermissions
from azure.storage.blob.aio import BlobServiceClient, BlobClient, ContainerClient

import os

from fastapi import HTTPException, UploadFile


async def upload_file_to_storage(files: List[UploadFile], file_type:str):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = os.getenv('CONTAINER_NAME')
    async with blob_service_client:
        container_client = blob_service_client.get_container_client(container_name)
        try:
            for file in files:
                blob_client = container_client.get_blob_client(file.filename)
                f = await file.read()
                await blob_client.upload_blob(f)
        except Exception as e:
            print(e)
            return HTTPException(401, "Something went terribly wrong..")


    return "{'did_it_work':'yeah it did!'}"


account_name = os.getenv('AZURE_STORAGE_ACCOUNT')
account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
container_name = os.getenv('CONTAINER_NAME')
blob_name = "CV_CLRajapaksha_UPADTED.pdf"

def get_container_sas(self, container_client: ContainerClient, account_key: str):
    # Create a SAS token that's valid for one day, as an example
    start_time = datetime.utcnow()
    expiry_time = start_time + timedelta(hours=1)

    sas_token = generate_container_sas(
        account_name=container_client.account_name,
        container_name=container_client.container_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=expiry_time,
        start=start_time
    )

    return sas_token

def get_blob_sas(blob_name):
    sas_blob = generate_blob_sas(account_name=account_name,
                                container_name=container_name,
                                blob_name=blob_name,
                                account_key=account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.utcnow() + timedelta(hours=1))
    return sas_blob

blob_sas = get_blob_sas(blob_name)
url = 'https://'+account_name+'.blob.core.windows.net/'+container_name+'/'+blob_name+'?'+blob_sas

def get_signed_blob_url(sas: str):
    sas_url = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + sas
    return sas_url

async def download_file_from_storage(file_id: str):
    # container = ContainerClient.from_container_url(url)
    # container.get_blob_client(blob_name)
    blob_client = BlobClient.from_blob_url(url)
    with open(file=os.path.join(r'./', 'my_cv.pdf'), mode="wb") as sample_blob:
        download_stream = await blob_client.download_blob()
        sample_blob.write(await download_stream.readall())
