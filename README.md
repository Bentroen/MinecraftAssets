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

Ultimately, the end goal is to have a stable, fixed, predictable reference to every version of a sound asset ever introduced to the game, such that a song never sounds different according to when it's being viewed at, due to a version of Minecraft replacing a particular sound (see e.g. the controversial [piston sound change in 24w20a](https://minecraft.wiki/w/Java_Edition_24w20a#Sounds)).

Although the goal of our approach applies primarily to the game's sounds, it can be later expanded to include other assets, such as textures, models, and language files.

## Structure

As the Minecraft version data is structured currently, the [`version_manifest.json`](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json) stores every version ever released, along with a URL of a manifest JSON that stores the data for a particular version.

In each version's manifest (e.g. [1.20.5.json](https://piston-meta.mojang.com/v1/packages/f5e18046457e8aa93dd301ffc3719d2088085e7a/1.20.6.json)), along with libraries and other data used by the launcher, there's an `assetIndex` field that stores the name and the URL of the asset index for that version (e.g. [16.json](https://piston-meta.mojang.com/v1/packages/346e146d8a8ec2e53aa9e916a8e1af962492fcc0/16.json)). The asset index stores all the asset objects in that version: the path to the asset in the game's files, the object's SHA-1 hash, and its size. The objects themselves can be downloaded from the server using the hash through the following URL:

```
https://resources.download.minecraft.net/<first two characters of hash>/<full hash>
```

New asset indexes are introduced every time there's a major change in the assets, and although they are now more predictable (a number which increments at the start of a release cycle), they seem to have been introduced more arbitrarily in past versions. The motivation behind this repository was to investigate in which versions asset indexes were introduced, and what assets were changed between versions.

## Limitations

This doesn't include sounds from classic Minecraft that are not present in the current game. These files are not available from the current resource system, so they can't be downloaded from the game's servers, and have been replaced even in older game versions downloaded from the launcher (although they can be found online in community-made resource packs, such as [this one](https://www.planetminecraft.com/texture-pack/old-sounds-4911323/)). The Minecraft Wiki lists a lot of these files in the game's elements _History_ section (e.g. [Door#Historical sounds](https://minecraft.wiki/w/Wooden_Door#Historical_sounds), but calculating their hashes and trying to download them from the resource server yields no results (e.g. `https://resources.download.minecraft.net/02/022e48005197b37f0caa53e8051c8a266eeae15e`).

It also doesn't include sounds that are still downloadable from the game's servers, but for which there are no pointers in any asset index. One such example is the piston sound, which was [changed in the 24w20a snapshot](https://minecraft.wiki/w/Java_Edition_24w20a#Sounds), then [changed again in 24w21a](https://minecraft.wiki/w/Java_Edition_24w21a#Blocks). As both versions share the same asset index, the reference to the asset in 24w20a was replaced entirely (i.e. downloading 20w24a now yields the _new_ version of the sound), so it's no longer possible to get their download URL from the procedure above, even though they are still available from the game's servers (e.g. `tile/piston/in`: `https://resources.download.minecraft.net/2f/2faade0f2de6cf7414e021c6231cf662095062fa`).

To make these sounds available in the proposed system, it would be necessary to manually add them under a special category, and then host the files ourselves. For sounds that are still available from the game's servers, the [mcasset.cloud](https://mcasset.cloud/) project provides a historical view of versions, since they are scraped as soon as they are released - for instance, the aforementioned piston sound can be found [here](https://mcasset.cloud/24w20a/assets/minecraft/sounds/tile/piston). So, in theory, it should be possible to compare all versions stored in the repository to "catch" unlisted changes to the assets, calculate the replaced asset's hash and look it up in the resource server, replacing them in that version's asset index.

There are still limits to this source though, as 1) we can't guarantee that all versions have been scraped before an asset was replaced (especially versions from before the project's inception), and 2) we can't guarantee that the project will be maintained indefinitely. The [Minecraft Wiki](https://minecraft.wiki/) is also a valuable source in tracking changes to the sounds, but then again, it's not a complete source, and it's not structured in a way that would allow for easy querying of the data. This then becomes more an archival project than a data structuring project, which is not our primary goal.

## Usage

### [`download_manifests.py`](download_manifests.py)

This script downloads the `version_manifest.json` file from Mojang's servers, then downloads the manifests for all versions and saves them to the `manifest` folder.

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

This version reads each version's data from the `manifest` folder and downloads the asset indexes to the `asset_indexes` folder. By sorting the asset index by the earliest version it appears in, we can build a chronological list of asset indexes. The asset indexes are then saved again to the `asset_indexes_by_date` folder, in the format `<YYYY-MM-DD>_<index>.json`.

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

This script reads the asset index of the latest Minecraft release and creates three files:

-   `sound_list.json`: a map of all the sounds in th mapping the path where they are located to their hash. Useful for downloading a sound from the game's server by its path.
-   `sound_index_words.json`: a map of all unique words that appear in the sound paths (minus the `minecraft/sounds/` prefix) to the sounds that contain them. Useful for searching for a sound by a keyword, e.g. `piston` or `cave`.
-   `sound_index_keys.json`: a list of the keys in `sound_index_words.json`.
-   `sound_tree.json`: a tree structure of all the sounds in the game, based on their paths.

### [`asset_index_friendly_names.json`](asset_index_friendly_names.json)

This is a list of friendly names for all currently released asset indexes (`17` being the latest as of this repository's creation; `19` as of its last update).

It is used to give a more human-readable name to the asset indexes, as the names in the version manifest are not very descriptive. It names each asset index with its defining version, which was chosen using the following criteria:

-   Use the earliest release version in which the asset index appears
-   If the asset index doesn't appear in any release version, use the first pre-release in which it appears
-   If the asset index doesn't appear in any pre-release, use the first snapshot in which it appears

Then, we process the name:

-   If the version tag differs from the version name, use the version name (e.g. `1.14-af` -> `3D Shareware v1.34`)
-   Exceptions: `pre-1.6` > `Pre-1.6`, `legacy` -> `1.6-1.7`
-   Anything else gets treated as _Future version_

As it was created manually, there's not a way to generate it automatically yet.

## To-do

- At around 1.21.4, some change was applied to the game's resources that caused the hashes of all existing sounds to change, despite them sounding the same. While the hash is an easy way to identify a particular sound, it can no longer be used to match a particular sound if one's looking at only the most recent asset index (for instance, the reference to the sound may have been created before the hash change, and as such looking for this sound in the most recent game files would yield no result). If a custom system is developed to allow stable references to sounds, it possibly has to take im
-into account that multiple hashes can refer to what's, conceptually, the same sound (even if their contents are slightly different).

- Create a script to auto-generate the asset index friendly names

- Add GitHub action to run the scripts automatically and create artifacts/branches containing the output

- Create scripts to find the sound name based on the hash (looking at multiple asset index versions if necessary), and vice-versa

---
License - [MIT](LICENSE)
