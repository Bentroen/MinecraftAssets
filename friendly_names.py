import json

substitutions = {
    # Folders
    "/mob/": "",
    "/entity/": "",
    "/ambient/nether/": "",
    "/ambient/": "",
    "/block/": "",
    "/item/": "",
    "/additions/": "/",
    "/tile/": "",
    "/ui/": "",
    "/fire/": "fire/",
    "/fireworks/": "firework_rocket/",
    "/random/glass_": "glass/break_",
    "/random/anvil_": "anvil/",
    "/random/": "",
    "/records/": "music disc/",
    "/liquid/": "",
    "/note/": "note block/",
    "/damage/": "damage/",
    "/dig/": "dig/",
    "/step/": "step/",
    "/portal/": "portal/",
    "/enchant/": "enchant/",
    "/minecart/": "minecart/",
    "/music/game/water/": "music/",
    "/music/game/swamp/": "music/",
    "/music/game/creative/": "music/",
    "/music/game/nether/nether_wastes/": "music/",
    "/music/game/nether/soulsand_valley/": "music/",
    "/music/game/nether/crimson_forest/": "music/",
    "/music/game/nether/": "music/",
    "/music/game/end/": "music/",
    "/music/game/": "music/",
    "/music/menu/": "music/",
    "/event/": "",
    # Note blocks
    "/harp": "/harp",
    "/bass": "/bass",
    "/bassattack": "/bass attack",
    "/bd": "/bass drum",
    "/snare": "/snare drum",
    "/hat": "/click",
    "/xylobone": "/xylophone",
    "/icechime": "/chime",
    # Repeated words
    "guardian/elder": "elder_guardian",
    "guardian_": "",
    "elytra/elytra_": "elytra/",
    "dye/dye": "dye/use",
    "brush/brushing_": "brush/",
    "brush/brush_": "brush/",
    "bonemeal/bonemeal": "bonemeal",
    "player/hurt": "player",
    "endereye/endereye": "endereye",
    "grindstone/grindstone": "grindstone",
    "cave/cave": "cave",
    "portal/portal": "portal/ambient",
    "zpigangry": "angry",
    "zpigdeath": "death",
    "zpighurt": "hurt",
    "zpig": "idle",
    "longdig": "long dig",
    "say": "idle",
    "egg/drop_egg": "egg/drop",
    "egg/jump_egg": "egg/jump",
    "egg/egg": "egg/",
    "ink_sac/ink_sac": "ink_sac",
    "fire/fire": "fire/crackle",
    "soulspeed/soulspeed": "soulspeed",
    "totem/use_totem": "totem/use",
    "fletching_table/fletching_table": "fletching_table",
    "bamboo_wood_button/bamboo_wood_button": "bamboo_wood_button",
    "underwater/underwater_ambience": "underwater > ambience",
    "cherrywood_button/cherrywood_": "cherrywood_button/",
    "bell/bell": "bell",
    "bunnymurder": "murder",
    "swim/swim": "swim",
    "smithing_table/smithing_table": "smithing_table",
    "sculk_sensor/sculk_clicking": "sculk_sensor/clicking",
    "end_portal/endportal": "end_portal/spawn",
    "honeycomb/wax_on": "honeycomb/wax",
    "brush_armadillo": "brush",
    "camel/dash_ready_1": "camel/dash_ready",
    "trial_spawner/eject_item_1": "trial_spawner/eject_item",
    "ghast/fireball_4": "ghast/fireball",
    "endermen/portal": "endermen/teleport",
    "pick_from_bush": "pick",
    "cat/ocelot/": "cat/",
    "cat/stray/": "stray_cat/",
    "wololo": "charming",
    "hitt": "hit",
    "pre_sneeze": "pre-sneeze",
    "kill": "death",
    # Quick Charge
    "quick_charge/quick1": "quick_charge_i",
    "quick_charge/quick2": "quick_charge_ii",
    "quick_charge/quick3": "quick_charge_iii",
    # Word separation
    "magmacube": "magma cube",
    "irongolem": "iron golem",
    "vindication_illager": "vindicator",
    "illusion_illager": "illusioner",
    "evocation_illager": "evoker",
    "illager_beast": "ravager",
    "endermen": "enderman",
    "enderdragon": "ender dragon",
    "dragonbreath": "dragon breath",
    "largeblast": "large blast",
    "raidhorn": "horn",
    "berrybush": "berry bush",
    "crit": "critical",
    "endereye": "eye of ender",
    "itemframe": "item frame",
    "soulspeed": "soul speed",
    "soulsand": "soul sand",
    "basaltground": "basalt ground",
    "waterlily": "lily pad",
    "fallbig": "fall big",
    "fallsmall": "fall small",
    "blastfurnace": "blast furnace",
    "netherwart": "nether wart",
    "armorstand": "armor stand",
    "drawmap": "draw map",
    "bonemeal": "bone meal",
    "snowman": "snow golem",
    "leashknot": "lead",
    "honeyblock": "honey block",
    "enderchest": "ender chest",
    "bowhit": "bow/hit",
    "polarbear": "polar bear",
    "chestclosed": "chest close",
    "chestopen": "chest open",
    "levelup": "level up",
    "lavapop": "lava pop",
    "oxygene": "oxygène",
    "stereo": "(stereo)",
    "unfect": "cure",
    "woodbreak": "door break",
    "appeared": "appear",
    "listening": "listen",
    "panting": "pant",
    "sniffing": "sniff",
    "searching": "search",
    "scenting": "scent",
    "digging": "dig",
    "eyeplace": "place eye",
    # Horse variants
    "horse/skeleton": "skeleton horse",
    "horse/zombie": "zombie horse",
    "horse/donkey": "donkey",
    # Panda
    "cant": "can't",
    "worried/": "",
    "aggressive/": "",
    "nosebreath": "nose breath",
    # Goat
    "screaming": "scream",
    "pre_ram": "pre-ram",
}

caps = {
    "Ui": "UI",
    " Of ": " of ",
    " To ": " to ",
    " From ": " from ",
    " The ": " the ",
    " In ": " in ",
    " On ": " on ",
    " Iii": " III",
    " Ii": " II",
    "Otherside": "otherside",
    "Can'T": "Can't",
}


with open("files/sound_list.json", "r") as f:
    sound_list = json.load(f)

pretty_names = {}

for sound_name in sound_list:

    # Clean up
    pretty = sound_name
    pretty = pretty.replace("minecraft/sounds", "")
    pretty = pretty.replace(".ogg", "")

    # Replace numbers in fireworks
    if "firework" in pretty:
        pretty = pretty.replace("1", "")

    # Replace leading zeros
    pretty = pretty.replace("01", "1")
    pretty = pretty.replace("02", "2")
    pretty = pretty.replace("03", "3")
    pretty = pretty.replace("04", "4")

    # Split numbers
    if "record" not in pretty:
        if pretty[-2].isdigit() and pretty[-3] != "_":
            pretty = pretty[:-2] + " " + pretty[-2:]
        elif pretty[-1].isdigit() and pretty[-2] != "_":
            pretty = pretty[:-1] + "_" + pretty[-1]

    # Apply substitutions
    for old, new in substitutions.items():
        pretty = pretty.replace(old, new)

    # Break words
    pretty = pretty.replace("_", " ")
    pretty = pretty.title()

    # Apply unusual caps
    for old, new in caps.items():
        pretty = pretty.replace(old, new)

    # Split by /
    pretty = pretty.replace("/", " > ")

    print(pretty)

    pretty_names[sound_name] = pretty


with open("files/sound_list_pretty.json", "w") as f:
    json.dump(pretty_names, f, indent=4)
