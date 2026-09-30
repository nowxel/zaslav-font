"""Add designer/license metadata (name IDs 9,11,12,13,14) and bump version to 11.002.
Run once against each font file. Does not touch glyphs/outlines/kerning."""
import sys
from fontTools.ttLib import TTFont

HOMEPAGE = "https://nowxel.github.io/zaslav-display.html"
LICENSE_DESC = ("This Font Software is licensed under the SIL Open Font License, "
                 "Version 1.1. This license is available with a FAQ at: "
                 "https://scripts.sil.org/OFL")
LICENSE_URL = "https://scripts.sil.org/OFL"
VERSION = "11.002"
UNIQUE_ID = f"{VERSION};NOWXEL;ZaslavDisplay-Regular"

def set_name(name_table, name_id, value):
    name_table.setName(value, name_id, 1, 0, 0)      # Mac, English
    name_table.setName(value, name_id, 3, 1, 0x409)  # Windows, en-US

def process(path):
    font = TTFont(path)
    name = font["name"]
    set_name(name, 3, UNIQUE_ID)
    set_name(name, 5, f"Version {VERSION}")
    set_name(name, 9, "nowxel")
    set_name(name, 11, HOMEPAGE)
    set_name(name, 12, HOMEPAGE)
    set_name(name, 13, LICENSE_DESC)
    set_name(name, 14, LICENSE_URL)
    font["head"].fontRevision = float(VERSION)
    if "CFF " in font:
        cff = font["CFF "].cff
        topDict = cff[cff.fontNames[0]]
        topDict.version = VERSION
        topDict.Notice = LICENSE_DESC
    font.save(path)
    print(f"updated {path}")

for p in sys.argv[1:]:
    process(p)
