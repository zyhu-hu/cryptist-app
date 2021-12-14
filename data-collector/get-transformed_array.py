from google.cloud import storage
from google.oauth2 import service_account
import json
gcp_project = "zippy-avatar-332205"
bucket_name = "models-ac215"
token = "../secrets/credientials.json"


storage_credential = service_account.Credentials.from_service_account_file(
    token)
storage_client = storage.Client(
    project=gcp_project, credentials=storage_credential)

bucket = storage_client.bucket(bucket_name)
# Find all content in a bucket
#blobs = bucket.list_blobs()
blobs = bucket.blob("q_model_eth.h5")
#print(blobs)
#for blob in blobs:
#    print(blob.name)
#    if not blob.name.endswith("/"):
#        blob.download_to_filename(blob.name)
blobs.download_to_filename("q_model_eth.h5")
