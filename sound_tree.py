import json

with open("soundList.json", "r") as f:
    sounds: dict[str, str] = json.load(f)


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

with open("soundIndex.json", "w") as f:
    json.dump(index, f, indent=4, sort_keys=True)

with open("soundIndexKeys.json", "w") as f:
    json.dump(word_list, f, indent=4, sort_keys=True)
