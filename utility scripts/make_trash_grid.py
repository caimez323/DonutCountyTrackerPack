#!/usr/bin/env python3
import copy
import json
import re
import sys
from pathlib import Path

MAP_NAME = "Trash"
COLS = 14
START_X, START_Y = 100, 100
STEP_X, STEP_Y = 170, 170
SIZE = 40
SORT_BY_NAME = True


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


if len(sys.argv) < 2:
    sys.exit("Usage : python make_trash_grid.py <Trash.json> [sortie.json]")

src = Path(sys.argv[1])
dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "_grid.json")

data = json.loads(src.read_text(encoding="utf-8"))
root = data[0]

template = {
    "chest_unopened_img": root.get("chest_unopened_img", "/images/items/close.png"),
    "chest_opened_img": root.get("chest_opened_img", "/images/items/open.png"),
    "overlay_background": root.get("overlay_background", "#000000"),
}

children = root.get("children", [])
known = set()
for c in children:
    known.add(norm(c["name"]))
    for s in c.get("sections", []):
        known.add(norm(s["name"]))

for section in root.get("sections", []):
    if norm(section["name"]) in known:
        print(f"Ignoré (existe déjà) : {section['name']}")
        continue
    sec = copy.deepcopy(section)
    sec.setdefault("access_rules", [])
    sec.setdefault("visibility_rules", [])
    sec.setdefault("item_count", 1)
    children.append({
        "name": section["name"],
        **template,
        "access_rules": [],
        "visibility_rules": [],
        "sections": [sec],
        "map_locations": [],
    })
    known.add(norm(section["name"]))

if SORT_BY_NAME:
    children.sort(key=lambda c: norm(c["name"]))

for i, child in enumerate(children):
    row, col = divmod(i, COLS)
    child["map_locations"] = [{
        "map": MAP_NAME,
        "x": START_X + col * STEP_X,
        "y": START_Y + row * STEP_Y,
        "size": SIZE,
        "shape": "rect",
    }]

root["children"] = children
root["sections"] = []

dst.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
rows = (len(children) + COLS - 1) // COLS
last = children[-1]["map_locations"][0]

