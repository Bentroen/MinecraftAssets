# MinecraftAssets

A bunch of scripts to parse Minecraft: Java Edition asset files. It allows you to see useful stuff about how the assets in Minecraft have evolved over time, like when an asset index was introduced, and the changes in assets between versions.

This is extremely sloppy code that isn't meant to be used in production, but it may become a fully-fledged library for parsing and querying version data in the future.

See also:

-   https://wiki.vg/Game_files
-   https://github.com/InventivetalentDev/minecraft-assets
-   https://mcasset.cloud/

## Goals

The motivation behind this repository was to create a uniform way to specify a pointer to Minecraft sounds, for use in [Minecraft Note Block Studio](https://opennbs.org/). Considering a particular sound may change between different versions of the game, a sound's path can't be solely used as its unique identifier. As such, we need to reference the version of the game in which the sound is located.

However, a sound is more likely NOT to change between two different versions, than it is to change. That would create a lot of repeated pointers to the same files (e.g. `1.8.9/minecraft/sounds/ambient/cave/cave1.ogg` and `1.9/.../cave/cave1.ogg` would likely be the same file, so it would be pointless to store them differently in a song).

Additionally, many sounds which are the same in two different versions of the game have been _renamed_ in the game's file structure. This means that we can't simply compare the paths of the sounds in two different versions to see if they are the same sound.

The purpose of this repository is to investigate the changes in Minecraft assets over time by analyzing the asset indexes of different versions of the game. Based on this, we aim to create a format that allows for easy querying of asset data across different versions.

Ultimately, the end goal is to have a stable, fixed, predictable reference to every version of a sound asset ever introduced to the game, such that a song never sounds different according to when it's being viewed at, due to a version of Minecraft replacing a particular sound (see e.g. the piston sound change in 24w20a).

Although the goal of our approach applies primarily to the game's sounds, it can be later expanded to include other assets, such as textures, models, and language files.

## Structure

As the Minecraft version data is structured currently, the [`version_manifest.json`](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json) stores every version ever released, along with a URL of a manifest JSON that stores the data for a particular version.

In each version's manifest, along with libraries and other data used by the launcher, there's an `assetIndex` field that stores the name and the URL of the asset index for that version. The asset index stores all the asset objects in that version: the path to the asset in the game's files, the object's MD5 hash, and its size. The objects themselves can be downloaded from the server using the hash (`https://resources.download.minecraft.net/<first two characters of hash>/<full hash>`) and are stored in the `objects` folder in the game's files.

New asset indexes are introduced every time there's a major change in the assets, and although they are now more predictable, they seem to have been introduced more arbitrarily in past versions. The motivation behind this repository was to investigate in which versions asset indexes were introduced, and what assets were changed between versions.

## Usage

### [`download_manifests.py`](download_manifests.py)

This script downloads the `version_manifest.json` file from Mojang's servers, then downloads the manifests for all versions and saves it to the `manifest` folder.

### [`list_asset_indexes.py`](list_asset_indexes.py)

> [!IMPORTANT]
> This script depends on `download_manifests.py` being run first.

This script reads the `version_manifest.json` file and prints a list of unique asset indexes across all versions. It also outputs three files:

-   `asset_indexes.json`: a list of all the versions and their respective asset indexes.
-   `asset_indexes_grouped.json`: a map of all the asset indexes to the versions that use them.
-   `asset_indexes_grouped_nosnapshots.json`: the same as above, but containing only official releases.

### [`get_asset_indexes.py`](get_asset_indexes.py)

> [!IMPORTANT]
> This script depends on `download_manifests.py` being run first.

This version reads each version's data from the `manifest` folder and downloads the asset indexes to the `asset_indexes` folder. By sorting the asset index by the earliest version it appears in, we can build a chronological list of asset indexes. The asset indexes are then saved again to the `asset_indexes_by_date` folder, in the format `YYYY-MM-DD_index.json`.

### [`diff.py`](diff.py)

> [!IMPORTANT]
> This script depends on `get_asset_indexes.py` being run first.

This script reads a pair of subsequent asset indexes and compares them, outputting the differences between the two. The differences are saved to the `diffs` folder, as such:

-   `diff.txt`: a list of all the differences between the two asset indexes.
-   `diff_summary.txt`: a summary of the differences, including the number of added, removed, renamed and changed assets.

> [!INFO]
> As multiple paths can point to the same object, renames are notated as `[<old_path1>, <old_path2>, ...] -> [<new_path1>, <new_path2>, ...]`.

### `get_sounds.py`

> [!IMPORTANT]
> This script depends on `get_asset_indexes.py` being run first.

This script reads all the asset indexes and downloads all sound objects to the `objects` folder. It also counts the total number of sound assets, total number of references, and number of unique references in each asset index, and in total (across all versions).

### [`sound_tree.py`](sound_tree.py)

> [!IMPORTANT]
> This script depends on `get_sounds.py` being run first.

This script reads the asset index of the latest Minecraft release and creates a tree structure of all the sounds in the game, based on their paths. The tree is saved to `sound_tree.json`.

### [`asset_index_friendly_names.json`](asset_index_friendly_names.json)

This is a list of friendly names for all currently released asset indexes (`17` being the latest as of this repository's creation).

It is used to give a more human-readable name to the asset indexes, as the names in the version manifest are not very descriptive. It names each asset index with its defining version, which was chosen using the following criteria:

-   Use the earliest release version in which the asset index appears
-   If the asset index doesn't appear in any release version, use the first pre-release in which it appears
-   If the asset index doesn't appear in any pre-release, use the first snapshot in which it appears

Then, we process the name:

-   If the version tag differs from the version name, use the version name (e.g. `1.14-af` -> `3D Shareware v1.34`)
-   Exceptions: `pre-1.6` > `Pre-1.6`, `legacy` -> `1.6-1.7`
-   Anything else gets treated as _Future version_

As it was created manually, there's not a way to generate it automatically yet.

---

License - [MIT](LICENSE)
