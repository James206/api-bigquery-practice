import requests #python package for deailing with apis

url = "https://pokeapi.co/api/v2/pokemon?limit20"
all_pokemon = []

"""
while url:
    response = requests.get(url, headers=headers)
    all_commits.extend(response.json())
    url = response.links.get('next', {}).get('url')

print(f"Total commits pulled: {len(all_commits)}")

"""

while url:
    response = requests.get(url)
    data = response.json()
    all_pokemon.extend(data["results"])
    url = data["next"]

print(f"Total pokemon pulled: {len(all_pokemon)}")

# ── Flatten into rows BigQuery can load ──────────────────────

#print(all_pokemon[0])

records = []
for p in all_pokemon:
    records.append({
        "name": p["name"],
        "url": p["url"],
    })


# ── Load into BigQuery ────────────────────────────────────────
from google.cloud import bigquery

client = bigquery.Client(project="nene-practice-2026")
dataset_id = "github_practice"
table_id = f"{client.project}.{dataset_id}.pokemon"

job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE",  # wipe the table clean before loading
)

client.create_dataset(dataset_id, exists_ok=True)
job = client.load_table_from_json(records, table_id, job_config=job_config)
job.result()

print(f"Loaded {len(records)} rows into {table_id}")

# ── Verify it actually landed ─────────────────────────────────
query = f"SELECT name, url FROM `{table_id}` ORDER BY name DESC LIMIT 5"
for row in client.query(query):
    print(row.name, row.url[:50])
   