import json
from pathlib import Path


# Get a dict of all sounds in the latest release {<path>: <hash>}

with open(Path("files", "version_manifest.json"), "r") as f:
    manifest = json.load(f)

latest_release = manifest["latest"]["release"]
version_data_path = Path("manifest", f"{latest_release}.json")
with open(version_data_path, "r") as f:
    version_data = json.load(f)

asset_index = version_data["assetIndex"]["id"]
asset_index_path = Path("asset_indexes", f"{asset_index}.json")
with open(asset_index_path, "r") as f:
    asset_index_data = json.load(f)

sounds = {}

for key, value in asset_index_data["objects"].items():
    if ".ogg" in key:
        sounds[key] = value["hash"]

with open(Path("files", "sound_list.json"), "w") as f:
    json.dump(sounds, f, indent=4)


# Build an index of all words in the sound paths
index = {}
for path, hash in sounds.items():
    path = path.replace("minecraft/sounds/", "")
    path = path.replace(".ogg", "")

    search_key = path

    search_key = search_key.strip("0123456789")
    search_key = search_key.strip("_")
    parts = search_key.split("/")

    # Further split parts by word
    words = []
    for part in parts:
        words.extend(part.split("_"))

    for word in words:
        if word not in index:
            index[word] = []

        if path not in index[word]:
            index[word].append(path)


word_list = list(index.keys())
word_list.sort()

with open(Path("files", "sound_index_words.json"), "w") as f:
    json.dump(index, f, indent=4, sort_keys=True)

with open(Path("files", "sound_index_keys.json"), "w") as f:
    json.dump(word_list, f, indent=4, sort_keys=True)


# Build a tree index of all sounds
