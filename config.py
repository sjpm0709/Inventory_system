COLOR_MAP = {
    "0": "PLA Black",
    "1": "PLA Porcelain",
    "2": "PLA Orange",
    "3": "PLA Blue",
    "4": "PLA Green"
}

EXTRA_COMPONENTS = {
    "PBB": ["Wire", "Holder", "Bulb"],
    "ML": ["Wire", "Holder", "Bulb"],
    "WL": ["Wire", "Holder", "Bulb", "Metal Plate"]
}

# Default BOM rules (grams)
BOM_RULES = {
    ("PBB", "4"): (120, 40, 100),
    ("PBB", "7"): (120, 40, 100),
    ("PBB", "8"): (120, 40, 100),
    ("PBB", "9"): (40, 120, 100),

    ("ML", "1"): (80, 110, 50),
    ("ML", "2"): (80, 110, 50),
    ("ML", "3"): (80, 110, 50),

    ("WL", "1"): (80, 60, 20),
    ("WL", "2"): (80, 60, 20),
    ("WL", "3"): (80, 60, 20),
}