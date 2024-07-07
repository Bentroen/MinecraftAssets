import json
import shutil
from pathlib import Path

import dateutil.parser
import requests

# Set to True to ignore snapshot versions
IGNORE_SNAPSHOTS = False

# Download asset indices from versions
earliest_dates = {}
urls = {}

if not Path("asset_indexes").exists():
    Path("asset_indexes").mkdir()

if not Path("asset_indexes_by_date").exists():
    Path("asset_indexes_by_date").mkdir()

# Get the first appearance date of each asset index
for file in shutil.os.listdir("manifest"):
    with open(Path(f"manifest/{file}"), "r") as f:
        data = json.load(f)

    if IGNORE_SNAPSHOTS and data["type"] != "release":
        continue

    asset_index_id = data["assetIndex"]["id"]
    asset_index_url = data["assetIndex"]["url"]

    if asset_index_id not in urls:
        urls[asset_index_id] = asset_index_url

    release_time = dateutil.parser.parse(data["releaseTime"])

    if asset_index_id not in earliest_dates:
        earliest_dates[asset_index_id] = release_time
    else:
        if release_time < earliest_dates[asset_index_id]:
            earliest_dates[asset_index_id] = dateutil.parser.parse(data["releaseTime"])

# Download asset indices
for asset_index_id, asset_index_url in urls.items():

    earliest_index_date = earliest_dates[asset_index_id]

    print(f"Asset index: {asset_index_id}")
    print(f"Earliest appearance was at {earliest_dates[asset_index_id]}")

    # Skip file if it already exists
    if Path(f"asset_indexes/{asset_index_id}.json").exists():
        continue

    # Download version manifest to manifest/ folder
    manifest = requests.get(asset_index_url).text

    # Format date as YYYY-MM-DD
    date = earliest_index_date.strftime("%Y-%m-%d")

    with open(Path(f"asset_indexes/{asset_index_id}.json"), "w") as f:
        f.write(manifest)

    with open(Path(f"asset_indexes_by_date/{date}_{asset_index_id}.json"), "w") as f:
        f.write(manifest)
