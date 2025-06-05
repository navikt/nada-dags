from google.cloud.storage import Client
import random
num = random.random()

c = Client()

destination_blob_name="file.txt"

bucket = c.get_bucket("local-flyte-test")
blob = bucket.blob(destination_blob_name)

with blob.open("w") as f:
    f.write(f"Tester data aware scheduling {num}")

print(f"File uploaded to {destination_blob_name}.")
