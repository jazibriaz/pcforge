"""Parts catalog for PCForge.

Prices are illustrative sample prices in EUR, not live retail prices.
`power` is the realistic peak draw (W) used for PSU sizing, not the marketing TDP.
"""

CATALOG = {
    "cpu": [
        {"id": "r5-7600", "name": "AMD Ryzen 5 7600", "socket": "AM5", "memory": ["DDR5"], "power": 88, "cores": 6, "price": 189},
        {"id": "r7-9700x", "name": "AMD Ryzen 7 9700X", "socket": "AM5", "memory": ["DDR5"], "power": 88, "cores": 8, "price": 309},
        {"id": "r7-7800x3d", "name": "AMD Ryzen 7 7800X3D", "socket": "AM5", "memory": ["DDR5"], "power": 120, "cores": 8, "price": 379},
        {"id": "r9-9950x", "name": "AMD Ryzen 9 9950X", "socket": "AM5", "memory": ["DDR5"], "power": 230, "cores": 16, "price": 589},
        {"id": "i5-14600k", "name": "Intel Core i5-14600K", "socket": "LGA1700", "memory": ["DDR4", "DDR5"], "power": 181, "cores": 14, "price": 239},
        {"id": "i7-14700k", "name": "Intel Core i7-14700K", "socket": "LGA1700", "memory": ["DDR4", "DDR5"], "power": 253, "cores": 20, "price": 349},
        {"id": "u7-265k", "name": "Intel Core Ultra 7 265K", "socket": "LGA1851", "memory": ["DDR5"], "power": 250, "cores": 20, "price": 299},
    ],
    "motherboard": [
        {"id": "b650-tomahawk", "name": "MSI MAG B650 Tomahawk WiFi", "socket": "AM5", "memory": "DDR5", "form": "ATX", "price": 199},
        {"id": "x870e-hero", "name": "ASUS ROG Crosshair X870E Hero", "socket": "AM5", "memory": "DDR5", "form": "ATX", "price": 649},
        {"id": "b650i-strix", "name": "ASUS ROG Strix B650E-I", "socket": "AM5", "memory": "DDR5", "form": "Mini-ITX", "price": 309},
        {"id": "b760m-ds3h", "name": "Gigabyte B760M DS3H DDR4", "socket": "LGA1700", "memory": "DDR4", "form": "Micro-ATX", "price": 109},
        {"id": "z790-tomahawk", "name": "MSI MAG Z790 Tomahawk WiFi", "socket": "LGA1700", "memory": "DDR5", "form": "ATX", "price": 229},
        {"id": "z890-tuf", "name": "ASUS TUF Gaming Z890-Plus WiFi", "socket": "LGA1851", "memory": "DDR5", "form": "ATX", "price": 259},
    ],
    "memory": [
        {"id": "ddr5-32-6000", "name": "Corsair Vengeance 32GB (2x16) DDR5-6000 CL30", "type": "DDR5", "power": 10, "price": 99},
        {"id": "ddr5-64-6400", "name": "G.Skill Trident Z5 RGB 64GB (2x32) DDR5-6400", "type": "DDR5", "power": 14, "price": 219},
        {"id": "ddr4-32-3200", "name": "Kingston Fury Beast 32GB (2x16) DDR4-3200", "type": "DDR4", "power": 8, "price": 64},
    ],
    "gpu": [
        {"id": "rtx5060ti", "name": "NVIDIA GeForce RTX 5060 Ti 16GB (dual-fan)", "length": 200, "power": 180, "price": 449},
        {"id": "rtx5070", "name": "NVIDIA GeForce RTX 5070 Founders Edition", "length": 242, "power": 250, "price": 619},
        {"id": "rx9070xt", "name": "AMD Radeon RX 9070 XT (Sapphire Pulse)", "length": 320, "power": 304, "price": 679},
        {"id": "rtx5080", "name": "NVIDIA GeForce RTX 5080 Founders Edition", "length": 304, "power": 360, "price": 1149},
        {"id": "rtx5090", "name": "NVIDIA GeForce RTX 5090 (triple-fan partner card)", "length": 357, "power": 575, "price": 2399},
    ],
    "cooler": [
        {"id": "pa120se", "name": "Thermalright Peerless Assassin 120 SE", "kind": "air", "height": 155, "rated": 245, "sockets": ["AM5", "LGA1700", "LGA1851"], "price": 39},
        {"id": "nhd15g2", "name": "Noctua NH-D15 G2", "kind": "air", "height": 168, "rated": 250, "sockets": ["AM5", "LGA1700", "LGA1851"], "price": 149},
        {"id": "nhl12s", "name": "Noctua NH-L12S (low profile)", "kind": "air", "height": 70, "rated": 95, "sockets": ["AM5", "LGA1700"], "price": 59},
        {"id": "lf3-360", "name": "Arctic Liquid Freezer III 360", "kind": "aio", "radiator": 360, "rated": 300, "sockets": ["AM5", "LGA1700", "LGA1851"], "price": 109},
        {"id": "lf3-240", "name": "Arctic Liquid Freezer III 240", "kind": "aio", "radiator": 240, "rated": 250, "sockets": ["AM5", "LGA1700", "LGA1851"], "price": 79},
    ],
    "case": [
        {"id": "fractal-north", "name": "Fractal Design North", "forms": ["ATX", "Micro-ATX", "Mini-ITX"], "max_gpu": 355, "max_cooler": 170, "max_radiator": 360, "psu": ["ATX"], "price": 139},
        {"id": "o11-evo", "name": "Lian Li O11 Dynamic EVO", "forms": ["ATX", "Micro-ATX", "Mini-ITX"], "max_gpu": 422, "max_cooler": 167, "max_radiator": 360, "psu": ["ATX"], "price": 159},
        {"id": "4000d", "name": "Corsair 4000D Airflow", "forms": ["ATX", "Micro-ATX", "Mini-ITX"], "max_gpu": 360, "max_cooler": 170, "max_radiator": 360, "psu": ["ATX"], "price": 94},
        {"id": "nr200p", "name": "Cooler Master NR200P V2", "forms": ["Mini-ITX"], "max_gpu": 336, "max_cooler": 155, "max_radiator": 280, "psu": ["SFX", "SFX-L"], "price": 109},
    ],
    "psu": [
        {"id": "rm750e", "name": "Corsair RM750e (ATX 3.1)", "watts": 750, "form": "ATX", "price": 99},
        {"id": "pp12m-850", "name": "be quiet! Pure Power 12 M 850W", "watts": 850, "form": "ATX", "price": 119},
        {"id": "vertex-1000", "name": "Seasonic Vertex GX-1000", "watts": 1000, "form": "ATX", "price": 189},
        {"id": "rm1200x", "name": "Corsair RM1200x Shift", "watts": 1200, "form": "ATX", "price": 239},
        {"id": "sf750", "name": "Corsair SF750 Platinum (SFX)", "watts": 750, "form": "SFX", "price": 169},
        {"id": "sf1000", "name": "Corsair SF1000 (SFX)", "watts": 1000, "form": "SFX", "price": 229},
    ],
    "storage": [
        {"id": "990pro-2tb", "name": "Samsung 990 Pro 2TB NVMe", "power": 8, "price": 169},
        {"id": "sn850x-1tb", "name": "WD Black SN850X 1TB NVMe", "power": 7, "price": 89},
        {"id": "t500-2tb", "name": "Crucial T500 2TB NVMe", "power": 7, "price": 139},
    ],
}

CATEGORY_ORDER = ["cpu", "motherboard", "memory", "gpu", "cooler", "case", "psu", "storage"]

PRESETS = {
    "1440p-gaming": {
        "label": "1440p gaming",
        "parts": {"cpu": "r7-7800x3d", "motherboard": "b650-tomahawk", "memory": "ddr5-32-6000", "gpu": "rtx5070",
                  "cooler": "pa120se", "case": "fractal-north", "psu": "pp12m-850", "storage": "990pro-2tb"},
    },
    "small-form-factor": {
        "label": "Small form factor",
        "parts": {"cpu": "r7-9700x", "motherboard": "b650i-strix", "memory": "ddr5-32-6000", "gpu": "rtx5070",
                  "cooler": "lf3-240", "case": "nr200p", "psu": "sf750", "storage": "sn850x-1tb"},
    },
    "workstation": {
        "label": "Workstation",
        "parts": {"cpu": "r9-9950x", "motherboard": "x870e-hero", "memory": "ddr5-64-6400", "gpu": "rtx5080",
                  "cooler": "lf3-360", "case": "o11-evo", "psu": "vertex-1000", "storage": "990pro-2tb"},
    },
    "broken": {
        "label": "Spot the problems",
        "parts": {"cpu": "i7-14700k", "motherboard": "b650-tomahawk", "memory": "ddr4-32-3200", "gpu": "rtx5090",
                  "cooler": "nhl12s", "case": "nr200p", "psu": "rm750e", "storage": "sn850x-1tb"},
    },
}


def find(category, part_id):
    for part in CATALOG.get(category, []):
        if part["id"] == part_id:
            return part
    return None
