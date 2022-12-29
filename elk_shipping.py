import os
from elasticsearch import Elasticsearch

# Connect to the Elasticsearch instance
es = Elasticsearch()

# Iterate through all the files in the /logs directory
for file in os.listdir("/logs"):
  with open("/logs/" + file, "r") as f:
    # Read the contents of the file
    contents = f.read()

    # Index the contents of the file in Elasticsearch
    es.index(index="logs", doc_type="log", body={"content": contents})

print("Finished shipping logs to Elasticsearch.")