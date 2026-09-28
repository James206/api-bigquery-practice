
import requests #python package for deailing with apis

token = os.environ["GITHUB_TOKEN"]
headers = {"Authorization": f"Bearer {token}"}

url = "https://api.github.com/repos/James206/Touchlinker/commits?per_page=30"
all_commits = []

while url:
    response = requests.get(url, headers=headers)
    all_commits.extend(response.json())
    url = response.links.get('next', {}).get('url')

print(f"Total commits pulled: {len(all_commits)}")

# ── Flatten into rows BigQuery can load ──────────────────────
records = []
for c in all_commits:
    records.append({
        "sha": c["sha"],
        "author": c["commit"]["author"]["name"],
        "date": c["commit"]["author"]["date"],
        "message": c["commit"]["message"],
    })

# ── Load into BigQuery ────────────────────────────────────────
from google.cloud import bigquery

client = bigquery.Client(project="nene-practice-2026")
dataset_id = "github_practice"
table_id = f"{client.project}.{dataset_id}.commits"

client.create_dataset(dataset_id, exists_ok=True)
job = client.load_table_from_json(records, table_id)
job.result()

print(f"Loaded {len(records)} rows into {table_id}")

# ── Verify it actually landed ─────────────────────────────────
query = f"SELECT author, date, message FROM `{table_id}` ORDER BY date DESC LIMIT 5"
for row in client.query(query):
    print(row.author, row.date, row.message[:50])