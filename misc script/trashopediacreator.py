#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

PER_ROW = 15
OUTPUT = "rows.txt"
HEADER = "rows : ["
NAME_RE = re.compile(r"^trash_(.+)$", re.IGNORECASE)
RENAMED_RE = re.compile(r"^Trash : .+$")


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage : python {Path(sys.argv[0]).name} <fichier.json>")

    path = Path(sys.argv[1])
    with path.open(encoding="utf-8") as f:
        items = json.load(f)

    codes = []
    renamed = 0

    for item in items:
        name = item.get("name", "")
        m = NAME_RE.match(name)
        r = RENAMED_RE.match(name)
        if m or r:
            suffix = m.group(1) if m else name[len("Trash : "):]
            new_name = f"Trash : {suffix[0].upper()}{suffix[1:]}"
            if new_name != name:
                item["name"] = new_name
                renamed += 1
        else:
            continue  # pas un item trash

        code = item.get("codes")
        if code:
            codes.append(code)

    with path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=4, ensure_ascii=False)
        f.write("\n")

    rows = [codes[i:i + PER_ROW] for i in range(0, len(codes), PER_ROW)]
    lines = [HEADER]
    for i, row in enumerate(rows):
        content = ",".join(f'"{c}"' for c in row)
        comma = "," if i < len(rows) - 1 else ""
        lines.append(f"    [{content}]{comma}")
    lines.append("]")

    Path(OUTPUT).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{renamed} item(s) renommé(s), {len(codes)} code(s) dans {len(rows)} ligne(s) -> {OUTPUT}")


if __name__ == "__main__":
    main()