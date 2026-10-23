#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

NAMES = ["trash_egg","trash_donut","trash_tent","trash_chair","trash_radio","trash_testtuberack","trash_bird","trash_grass","trash_wall","trash_otherfood","trash_raccoon","trash_beehive","trash_bowl","trash_rock","trash_dumpster",
    "trash_hotthings","trash_hookgun","trash_trashcan","trash_joshualeaf","trash_donutbox","trash_tree","trash_character","trash_cage","trash_car","trash_fan","trash_bucket","trash_scooter","trash_flashlight","trash_beesmoker","trash_dirtpile",
    "trash_cowskull","trash_flour_icingbag","trash_chicken","trash_woodplank","trash_othertools","trash_brick","trash_bowlingball","trash_doghouse","trash_cat","trash_shovel","trash_donutcountylogoletters","trash_boulder","trash_frog","trash_paper","trash_megaphone",
    "trash_fence","trash_pot","trash_suitcase","trash_honeycomb","trash_keycard","trash_hardhat","trash_waterballoon","trash_campfire","trash_cockroach","trash_fish","trash_otherdrinks","trash_woodshelf","trash_trailer","trash_haybale","trash_money",
    "trash_tennisball","trash_bee","trash_laptop","trash_gecko","trash_microscope","trash_quadcopter","trash_crate","trash_firealarm","trash_cupramen","trash_bomb","trash_tincan","trash_book","trash_snake","trash_tire","trash_table",
    "trash_gardening","trash_cart","trash_cardboardbox","trash_sign","trash_nightstand","trash_carrot","trash_door","trash_lawnchair","trash_monitor","trash_mug","trash_bush","trash_clipboard","trash_camera","trash_rocket","trash_mask",
    "trash_hookpanel","trash_dryingrack","trash_pottedplant","trash_building","trash_trafficcone","trash_fly","trash_television","trash_fridge","trash_bone","trash_battery","trash_wheel","trash_candle","trash_takeout","trash_bunny","trash_corn",
    "trash_beaker","trash_instrument","trash_tile","trash_cactus","trash_pinecone","trash_beehouse","trash_hackingdevice"]

OVERWRITE = False  # POur écraser


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage : python {Path(sys.argv[0]).name} <image>")

    src = Path(sys.argv[1]).resolve()
    if not src.is_file():
        sys.exit(f"Fichier introuvable : {src}")

    copied = skipped = 0
    for name in NAMES:
        dst_name = name if Path(name).suffix else name + src.suffix
        dst = src.parent / dst_name

        if dst == src:
            print(f"Ignoré (même fichier que la source) : {dst.name}")
            skipped += 1
            continue
        if dst.exists() and not OVERWRITE:
            print(f"Ignoré (existe déjà) : {dst.name}")
            skipped += 1
            continue

        shutil.copy2(src, dst)
        print(f"Copié : {dst.name}")
        copied += 1

    print(f"\n{copied} copie(s), {skipped} ignorée(s).")


if __name__ == "__main__":
    main()