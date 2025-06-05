from google.cloud.storage import Client

c = Client()

destination_blob_name="file.txt"

bucket = c.get_bucket("local-flyte-test")
blob = bucket.blob(destination_blob_name)

with blob.open("r") as f:
    content = f.read()

print(f"Read from bucket - file: {destination_blob_name}, content: {content}")
