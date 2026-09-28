from google.cloud import bigquery
client = bigquery.Client(project="nene-practice-2026")
print(list(client.list_datasets()))