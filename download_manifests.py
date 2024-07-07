# Make a request to https://piston-meta.mojang.com/mc/game/version_manifest_v2.json
# and parse the JSON response.

# Print the latest release version of Minecraft: Java Edition.

import json
import shutil
import sys
from pathlib import Path

import requests

# Create a folder called 'files'
if not shutil.os.path.exists("files"):
    shutil.os.makedirs("files")

# Make a request to the version manifest
manifest = requests.get(
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)
manifest_data = manifest.json()
latest_release = manifest_data["latest"]["release"]
version_manifest = manifest_data["versions"]

# Save the version manifest to a file
with open(Path("files", "version_manifest.json"), "w") as f:
    json.dump(manifest_data, f, indent=4)

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
