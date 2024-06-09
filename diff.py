import json
from pathlib import Path
import shutil
from typing import Literal


ONLY_SOUNDS = True


def signed_size(size):
    if size == 0:
        return "0 B"
    if size < 0:
        return f"{size} B"
    return f"+{size} B"


ops = {"add": "+", "remove": "-", "rename": "|", "change": ">"}


def print_and_write(
    f, obj: str, op: Literal["add", "remove", "rename", "change"] | None = None
):
    # obj = obj.replace("minecraft/", "")
    if op is None:
        line = obj
    else:
        line = f"({ops[op]}) {obj}"
    # print(line)
    f.write(line + "\n")


# Run get_asset_indexes.py first!

prev_file = None
prev_objects = None

diff_file = open("diff.txt", "w")
diff_summary = open("diff_summary.txt", "w")

summary = {}

prev_hash_table = None
hash_table = {}

for file in shutil.os.listdir("asset_indexes_by_date"):
    with open(f"asset_indexes_by_date/{file}", "r") as f:
        data = json.load(f)

    date, index = file.split("_")
    index = index.replace(".json", "")

    curr_size = Path(f"asset_indexes_by_date/{file}").stat().st_size
    # print(f"Asset Index: {index}, Date: {date}, Size: {curr_size}")

    if ONLY_SOUNDS:
        objects = {
            obj: data["objects"][obj]
            for obj in data["objects"]
            if ".ogg" in obj or ".mus" in obj
        }
    else:
        objects = data["objects"]

    print()
    print(index)

    # Construct current hash table to compare with previous hash table
    for obj, obj_data in objects.items():

        if "hal4" in obj:
            print(objects[obj]["hash"])

        hash = objects[obj]["hash"]
        name = obj

        if hash not in hash_table:
            hash_table[hash] = []  # List of names that we have seen with this hash

        if name not in hash_table[hash]:
            hash_table[hash].append(name)

    # Calculate diff between prev and current asset index
    if prev_file is None:

        # First file -- all files are new

        print_and_write(diff_file, f"{index} ({signed_size(curr_size)})")
        print_and_write(diff_file, "-------------------------------")

        summary[f"{index}"] = {
            "size": curr_size,
            "objects": {
                "add": 0,
                "remove": 0,
                "rename": 0,
                "change": 0,
            },
        }

        for obj in objects:
            print_and_write(diff_file, obj, "add")
            summary[f"{index}"]["objects"]["add"] += 1

    else:
        prev_date, prev_index = prev_file.split("_")
        prev_index = prev_index.replace(".json", "")
        prev_size = Path(f"asset_indexes_by_date/{prev_file}").stat().st_size

        diff = curr_size - prev_size

        print_and_write(diff_file, f"{prev_index} -> {index} ({signed_size(diff)})")
        print_and_write(diff_file, "-------------------------------")

        summary[f"{prev_index} -> {index}"] = {
            "size": signed_size(diff),
            "objects": {
                "add": 0,
                "remove": 0,
                "rename": 0,
                "change": 0,
            },
        }

        renamed_list = []

        for hash, names in hash_table.items():

            if hash == "5e7d63e75c6e042f452bc5e151276911ef92fed8":
                print("Names:", names)
                print(
                    "Prev names:",
                    prev_hash_table[hash] if hash in prev_hash_table else None,
                )

            # If the hash is not in the previous hash table, skip it
            if hash not in prev_hash_table:
                continue

            prev_names = prev_hash_table[hash]
            curr_names = hash_table[hash]

            if hash == "5e7d63e75c6e042f452bc5e151276911ef92fed8":
                print(prev_names != curr_names)

            if prev_names != curr_names:
                print_and_write(
                    diff_file,
                    f"[{','.join(prev_names)}] -> [{','.join(curr_names)}]",
                    "rename",
                )
                summary[f"{prev_index} -> {index}"]["objects"]["rename"] += 1

                renamed_list.extend(curr_names)
                renamed_list.extend(prev_names)

        for obj in objects:

            # If the object was renamed in this index, skip it
            if obj in renamed_list:
                continue

            if obj not in prev_objects:
                # ADD
                # size = objects[obj]["size"]
                print_and_write(diff_file, obj, "add")
                summary[f"{prev_index} -> {index}"]["objects"]["add"] += 1
            else:
                # CHANGE
                if objects[obj]["hash"] != prev_objects[obj]["hash"]:
                    # size_diff = objects[obj]["size"] - prev_objects[obj]["size"]
                    print_and_write(
                        diff_file,
                        obj,
                        "change",
                    )
                    summary[f"{prev_index} -> {index}"]["objects"]["change"] += 1

        # REMOVE
        for obj in prev_objects:

            # If the object was renamed in this index, skip it
            if obj in renamed_list:
                continue

            if obj not in objects:
                print_and_write(diff_file, obj, "remove")
                summary[f"{prev_index} -> {index}"]["objects"]["remove"] += 1

    prev_hash_table = hash_table.copy()
    hash_table = {}

    print_and_write(diff_file, "")
    prev_file = file
    prev_objects = objects


for key, value in summary.items():
    print_and_write(diff_summary, f"{key} ({value['size']})")
    print_and_write(diff_summary, "-------------------------------")
    objects = value["objects"]
    print_and_write(diff_summary, str(objects["add"]), "add")
    print_and_write(diff_summary, str(objects["change"]), "change")
    print_and_write(diff_summary, str(objects["rename"]), "rename")
    print_and_write(diff_summary, str(objects["remove"]), "remove")
    print_and_write(diff_summary, "")


diff_file.close()
diff_summary.close()
