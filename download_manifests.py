# Make a request to https://piston-meta.mojang.com/mc/game/version_manifest_v2.json
# and parse the JSON response.

# Print the latest release version of Minecraft: Java Edition.

import json
import shutil
import sys
import requests

# Make a request to the version manifest
manifest = requests.get(
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)
manifest_data = manifest.json()
latest_release = manifest_data["latest"]["release"]
version_manifest = manifest_data["versions"]

# Save the version manifest to a file
with open("version_manifest.json", "w") as f:
    json.dump(manifest_data, f, indent=4)

# Create a dict with the version ID as keys and version data as values
version_manifest_dict = {version["id"]: version for version in version_manifest}

print(f"The latest release version of Minecraft: Java Edition is {latest_release}.")

# Create a folder called manifest
if not shutil.os.path.exists("manifest"):
    shutil.os.makedirs("manifest")


for version in version_manifest:
    # type = release, snapshot, old_beta, old_alpha
    type = version["type"]
    v_id = version["id"]
    url = version["url"]

    print(f"Version: {v_id}, Type: {type}")

    # Skip file if it already exists
    if shutil.os.path.exists(f"manifest/{v_id}.json"):
        continue

    # Download version manifest to manifest/ folder
    manifest = requests.get(url).text

    with open(f"manifest/{v_id}.json", "w") as f:
        f.write(manifest)

print()

asset_indexes = {}
asset_indexes_grouped = {}

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


with open("asset_indexes_grouped.json", "w") as f:
    json.dump(asset_indexes_grouped, f, indent=4)

with open("asset_indexes.json", "w") as f:
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

with open("asset_indexes_grouped_nosnapshots.json", "w") as f:
    json.dump(asset_indexes_grouped_nosnapshots, f, indent=4)
