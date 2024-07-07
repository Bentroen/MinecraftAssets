import json
import os

import requests

files = 0
sounds = 0
refs = 0

all_hashes = set()

if not os.path.exists("objects"):
    os.mkdir("objects")

for asset in os.listdir("asset_indexes_by_date"):
    with open(f"asset_indexes_by_date/{asset}", "r") as f:
        data = json.load(f)

    objects = data["objects"]

    files += 1
    file_sounds = 0
    file_refs = 0

    new_hashes = 0

    hashes = set()

    for key, obj in objects.items():
        if ".ogg" not in key:
            continue

        hash = obj["hash"]
        size = obj["size"]

        if hash not in hashes:
            hashes.add(hash)
            file_sounds += 1

        if hash in all_hashes:
            continue

        all_hashes.add(hash)
        sounds += 1
        new_hashes += 1

        # Download sound

        if os.path.exists(f"objects/{hash}"):
            continue

        url = f"https://resources.download.minecraft.net/{hash[:2]}/{hash}"
        # use requests to download the file
        # save to objects/hash

        print(f"Downloading {hash} ({size} bytes)")
        content = requests.get(url).content

        with open(f"objects/{hash}", "wb") as f:
            f.write(content)

        refs += 1
        file_refs += 1

    print(
        f"{asset}: {file_sounds} unique sounds ({new_hashes} new), {file_refs} references"
    )

print(f"Total: {sounds} unique sounds, {refs} references over {files} files")
