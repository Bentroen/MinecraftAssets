import json
import shutil
import sys
import requests
from pathlib import Path


asset_indexes = {}
asset_indexes_grouped = {}


# Load version manifest
with open(Path("files", "version_manifest.json"), "r") as f:
    version_manifest = json.load(f)


# Create a dict with the version ID as keys and version data as values
version_manifest_dict = {
    version["id"]: version for version in version_manifest["versions"]
}


# List all files in manifest folder
for version in shutil.os.listdir("manifest"):
    with open(f"manifest/{version}", "r") as f:
        data = json.load(f)

    version = version.replace(".json", "")
    asset_index = data["assets"]

    if asset_index not in asset_indexes_grouped:
        asset_indexes_grouped[asset_index] = []
        print(f"Asset Index: {asset_index}")
    asset_indexes_grouped[asset_index].append(version)

    asset_indexes[version] = asset_index


if not Path("files").exists():
    Path("files").mkdir()

with open(Path("files", "asset_indexes_grouped.json"), "w") as f:
    json.dump(asset_indexes_grouped, f, indent=4)

with open(Path("files", "asset_indexes.json"), "w") as f:
    json.dump(asset_indexes, f, indent=4)


# Filter snapshot versions

asset_indexes_grouped_nosnapshots = {}

for group, group_versions in asset_indexes_grouped.items():

    for version in group_versions:
        version_data = version_manifest_dict[version]

        if group not in asset_indexes_grouped_nosnapshots:
            asset_indexes_grouped_nosnapshots[group] = []

        if version_data["type"] != "release":
            continue

        asset_indexes_grouped_nosnapshots[group].append(version)

with open(Path("files", "asset_indexes_grouped_nosnapshots.json"), "w") as f:
    json.dump(asset_indexes_grouped_nosnapshots, f, indent=4)
