"""The doc figures behind catalogue_1857_targets.py: eng_economy.md and raj_economy.md, as tables.

Each Item is one line of a doc: which building makes it, which good it is, its value in GBP M a year, how many thousand
people did it, and how it spreads across states. Weights only matter relative to each other: {A: 3, B: 1} means 75% and 25%.

Farm lines have workers=None, which means "a share of the farm workers". FARM_WORKERS gives each country's total, and a
line's share follows its value. This file holds numbers only: the steps are in catalogue_1857_targets.py.
"""
from collections import namedtuple

# These are a guide, not a rule (Strat, 2026-10-31). The UK starts from its workers. India starts from its value, with the rest on subsistence
Item = namedtuple("Item", "building good label gbp_m workers weights")


def share(total, weights):
    """Scales weights to sum to total, so a group can take a set part of a line."""
    s = sum(weights.values())
    return {k: v * total / s for k, v in weights.items()}


def merge(*parts):
    out = {}
    for p in parts:
        for k, v in p.items():
            out[k] = out.get(k, 0) + v
    return out


def by_population(pop, boost=None):
    return {s: p * (boost or {}).get(s, 1) for s, p in pop.items()}


# ---------------------------------------------------------------------------- British Isles
LON, SUS, EAN, COR, GLO, WMI, EMI, YOR, NOR, LAN = 952, 127, 125, 123, 338, 128, 129, 130, 131, 132
WAL = 122
LNK, LOT, ABD, HIG = 133, 121, 136, 120
LEI, ULS, CON, MUN = 113, 119, 134, 135
ENGLAND, SCOTLAND, IRELAND = [LON, SUS, EAN, COR, GLO, WMI, EMI, YOR, NOR, LAN], [LNK, LOT, ABD, HIG], [LEI, ULS, CON, MUN]
BRITISH_REGIONS = [("England", ENGLAND), ("Wales", [WAL]), ("Scotland", SCOTLAND), ("Ireland", IRELAND)]
BRITISH_DOC_POP = {"England": 18000, "Wales": 1250, "Scotland": 3000, "Ireland": 5950}
BRITISH_FARM_WORKERS = [(ENGLAND, 1480), ([WAL], 120), (SCOTLAND, 250), (IRELAND, 1150)]  # The doc's 3.0M
BRITISH_SUBSISTENCE = merge({s: 0.01 for s in ENGLAND}, {WAL: 0.05}, {s: 0.06 for s in SCOTLAND}, {s: 0.325 for s in IRELAND})
BRITISH_CITIES = {LON: 55, SUS: 31, EAN: 6, COR: 5, GLO: 10, WMI: 26, EMI: 7, YOR: 39, NOR: 13, LAN: 51, WAL: 7, LNK: 30, LOT: 10,
                  ABD: 2, HIG: 4, LEI: 10, ULS: 11, CON: 1, MUN: 4}  # Victory points
# GB 1851 census occupations the doc doesn't list, in K
BRITISH_NOT_LISTED = [("Labourers, branch not given", 377), ("Building trades and brick makers", 477), ("Army, navy, police, civil service", 228),
                      ("Charwomen", 55), ("Fishermen", 38), ("Millers", 37), ("Railway labourers", 34), ("Stone quarriers", 23)]

CROP_E = {EAN: 22, EMI: 16, SUS: 13, YOR: 12, LON: 10, GLO: 10, WMI: 8, COR: 4, NOR: 3, LAN: 2}
PAST_E = {LAN: 14, GLO: 14, EMI: 14, COR: 12, WMI: 12, YOR: 10, NOR: 8, SUS: 7, EAN: 5, LON: 4}
CROP_S, PAST_S = {LOT: 40, ABD: 30, LNK: 20, HIG: 10}, {ABD: 35, LNK: 25, LOT: 20, HIG: 20}
CROP_I, PAST_I = {LEI: 38, MUN: 32, ULS: 20, CON: 10}, {MUN: 40, LEI: 30, ULS: 15, CON: 15}


def nations(e, w, s, i, england, scotland, ireland):
    return merge(share(e, england), {WAL: w}, share(s, scotland), share(i, ireland))


def crops(e, w, s, i):
    return nations(e, w, s, i, CROP_E, CROP_S, CROP_I)


def pasture(e, w, s, i):
    return nations(e, w, s, i, PAST_E, PAST_S, PAST_I)


def british_services(pop):
    """Doc: England 78% (London 20), Scotland 10, Ireland 9, Wales 3. Within a country, half population, half cities."""
    def within(states, total):
        people, cities = sum(pop[s] for s in states), sum(BRITISH_CITIES[s] for s in states)
        return {s: total * (0.5 * pop[s] / people + 0.5 * BRITISH_CITIES[s] / cities) for s in states}
    return merge({LON: 20}, within([s for s in ENGLAND if s != LON], 58), {WAL: 3}, within(SCOTLAND, 10), within(IRELAND, 9))


def british_items(pop):
    services = british_services(pop)
    light = by_population(pop, {LON: 1.5, LAN: 1.2, WMI: 1.3, WAL: 0.6, **{s: 0.9 for s in SCOTLAND}, **{s: 0.4 for s in IRELAND}})
    clothing = by_population(pop, {LON: 2, **{s: 0.5 for s in IRELAND}})
    lead_england = share(60, {NOR: 467, WMI: 176, YOR: 174, COR: 178, EMI: 100})  # Old state notes, plus Derbyshire
    wool = nations(75, 6, 12, 7, {EMI: 20, YOR: 15, NOR: 15, GLO: 12, SUS: 10, WMI: 10, EAN: 8, COR: 5, LAN: 3, LON: 2},
                   {HIG: 50, LOT: 30, ABD: 15, LNK: 5}, {CON: 40, MUN: 25, LEI: 25, ULS: 10})
    veg = nations(90, 2, 5, 3, {LON: 30, SUS: 20, WMI: 15, GLO: 15, COR: 5, EAN: 5, YOR: 4, LAN: 4, EMI: 1, NOR: 1}, CROP_S, CROP_I)
    ore = {LNK: 1357, LOT: 393, WMI: 1417, YOR: 1135, WAL: 784, NOR: 584, LAN: 415, EMI: 287, GLO: 100, COR: 33, SUS: 5, LON: 5}  # Old state notes
    coal = {NOR: 16.7, LAN: 9.3, YOR: 8.9, WMI: 8.3, WAL: 8.1, LNK: 4.9, EMI: 4.4, LOT: 2.5, GLO: 1.2, ABD: 0.8, LEI: 0.08, ULS: 0.02, CON: 0.02}  # Tons, old state notes
    furnaces = {WAL: 1010, WMI: 900, LNK: 800, NOR: 315, YOR: 270, EMI: 150, LOT: 120, GLO: 60, LAN: 10}  # Pig iron table
    timber = {HIG: 80, ABD: 60, WMI: 22, WAL: 21, SUS: 19, GLO: 17, YOR: 14, MUN: 14, NOR: 13, EAN: 12, LNK: 12, EMI: 11, LEI: 11, COR: 9, ULS: 9, LAN: 7,
              LOT: 5, CON: 5}  # Old map's sizes, as the doc has no split
    rail = {LAN: 15, WMI: 9, YOR: 7, LON: 6, EMI: 5, EAN: 4, NOR: 4, WAL: 4, LNK: 4, COR: 3, SUS: 3, GLO: 3, LOT: 3, LEI: 1, ULS: 1, CON: 1, MUN: 1}  # Old map's sizes
    # 70% follows the doc's exports by port, 30% the old port sizes, for coal and coastal trade
    ports = merge(share(70, {LAN: 55.2, LON: 27.8, YOR: 15.8, LNK: 5.1}),
                  share(30, {LON: 25, LAN: 15, SUS: 10, YOR: 8, LNK: 6, WAL: 5, COR: 5, NOR: 5, GLO: 5, EAN: 3, ULS: 3, LOT: 3, LEI: 2, ABD: 1}))
    return [
        Item("crop_farm", "food", "wheat", 42, None, crops(85, 2, 6, 9)),
        Item("crop_farm", "food", "barley", 20, None, crops(80, 5, 7, 8)),
        Item("crop_farm", "food", "oats", 17, None, crops(30, 5, 27, 38)),
        Item("crop_farm", "food", "potatoes", 11, None, crops(24, 3, 9, 64)),
        Item("crop_farm", "food", "vegetables", 6.5, None, veg),
        Item("livestock_ranch", "food", "meat", 45, None, pasture(70, 3, 12, 15)),
        Item("livestock_ranch", "food", "dairy", 37.5, None, pasture(65, 5, 10, 20)),
        Item("livestock_ranch", "food", "eggs", 5, None, pasture(55, 3, 7, 35)),
        Item("livestock_ranch", "food", "hides", 5, None, pasture(70, 3, 12, 15)),
        Item("livestock_ranch", "fiber", "wool", 11, None, wool),
        Item("fiber", "fiber", "flax", 1, None, {ULS: 95, CON: 3, LEI: 2}),
        Item("luxuries_plantation", "luxuries", "hops", 1.75, None, {SUS: 85, WMI: 15}),
        Item("wood", "wood", "timber", 1.75, 45.4, timber),
        Item("coal", "coal", "coal", 16.5, 237, coal),
        Item("iron", "iron", "pig iron smelting", 9.45, 25, furnaces),
        Item("iron", "iron", "iron ore", 3.3, 30, ore),
        Item("iron", "iron", "lead", 1.55, 20, merge(lead_england, {WAL: 30, LAN: 4, LNK: 3, LEI: 2, ULS: 1})),
        Item("copper", "copper", "copper ore", 1.3, 23, {COR: 88, MUN: 4, WAL: 3, LEI: 3, LAN: 1, NOR: 1}),
        Item("copper", "copper", "copper smelting", 0.7, 3.5, {WAL: 1}),
        Item("copper", "copper", "tin", 0.85, 15, {COR: 1}),
        Item("valuables", "valuables", "silver", 0.14, 2, {COR: 30, NOR: 30, WAL: 20, LAN: 10, YOR: 5, LNK: 5}),
        Item("valuables", "valuables", "gold", 0.002, 0.1, {WAL: 1}),
        Item("steel_foundry", "steel", "wrought iron", 19, 60, {WMI: 35, WAL: 28, LNK: 12, YOR: 12, NOR: 9, LAN: 2, EMI: 2}),
        Item("steel_foundry", "steel", "crucible steel", 3, 9, {YOR: 1}),
        Item("tooling_workshop", "tools", "hardware", 15.5, 187, {WMI: 55, YOR: 25, WAL: 7, LAN: 6, LON: 5, LNK: 2}),
        Item("tooling_workshop", "tools", "blacksmiths", 9.5, 113, by_population(pop)),
        Item("mechanical_works", "machinery", "machines", 17.5, 85, {LAN: 30, YOR: 14, NOR: 14, WMI: 14, LON: 14, LNK: 11, ULS: 1, LOT: 1, EMI: 1}),
        Item("mechanical_works", "machinery", "ships", 7, 35, {NOR: 30, LNK: 28, LON: 18, LAN: 8, ABD: 5, LOT: 3, SUS: 2, GLO: 2, ULS: 2, WAL: 2}),
        Item("chemical_plant", "chemicals", "chemicals", 10, 30, {NOR: 33, LAN: 33, LNK: 22, LON: 8, WAL: 2, ULS: 1, LOT: 1}),
        Item("consumer_goods_factory", "consumer_goods", "furniture, leather, glass, paper", 41.2, 260, light),
        Item("consumer_goods_factory", "consumer_goods", "pottery", 6.3, 40, {WMI: 85, NOR: 5, LAN: 5, LNK: 5}),
        # Textile workers are the doc's census lines, scaled up to its 2.3M total
        Item("textile_mill", "textiles", "clothing", 65, 923, clothing),
        Item("textile_mill", "textiles", "cotton", 57.5, 603, {LAN: 85, LNK: 10, EMI: 3, ULS: 2}),
        Item("textile_mill", "textiles", "woollen", 25, 166, {YOR: 60, GLO: 20, LOT: 10, WAL: 6, LAN: 4}),
        Item("textile_mill", "textiles", "worsted", 15, 125, {YOR: 1}),
        Item("textile_mill", "textiles", "linen", 15, 191, {ULS: 45, ABD: 25, YOR: 15, LOT: 10, LNK: 5}),
        Item("textile_mill", "textiles", "silk", 10, 138, {LAN: 45, WMI: 25, LON: 20, EMI: 10}),
        Item("textile_mill", "textiles", "lace, hosiery", 8, 155, {EMI: 1}),
        # Strat's call: domestic service (GBP 30M, 1,385K workers) and housing (GBP 45M) are hidden, as neither has a building
        Item("urban_center", "services", "retail and wholesale", 60, 801, services),
        Item("urban_center", "services", "professions", 20, 130, services),
        Item("urban_center", "services", "commerce, finance", 15, 86, {LON: 55, LAN: 15, LNK: 8, LOT: 5, YOR: 4, LEI: 4, WMI: 3, NOR: 2, GLO: 2, ULS: 1, MUN: 1}),
        Item("urban_center", "services", "road, canal transport", 14.4, 97, services),
        Item("entertainment_hub", "entertainment", "entertainment", 8, 27.5, {LON: 50, LAN: 14, LOT: 6, LNK: 5, LEI: 5, WMI: 5, YOR: 5, SUS: 3, NOR: 2, GLO: 2, ULS: 1, MUN: 1, WAL: 1}),
        Item("railway", "transport", "rail", 16.4, 110, rail),
        Item("port", "shipping", "shipping", 19.2, 129, ports),
    ]


# ---------------------------------------------------------------------------- India
WBN, CBN, EBN, TRI, ASM, BIH, JHK, LOR, UOR, MNP = 431, 1315, 430, 1316, 432, 435, 1422, 426, 1423, 1075
LDB, UDB, DEL, HIM, OUDH = 438, 1128, 439, 1425, 756
PJB, SIR, MUL, ISL = 440, 1426, 1330, 1449
TML, AND, CIR, MLB = 423, 424, 1034, 757
NKK, SKK, SND, THA = 429, 977, 443, 1000
BER, BST = 436, 755
BUR, RAK, KRN, NTN = 288, 1390, 1392, 1391
DEC = 427
RJS, BIK, AGR, UDP = 433, 1427, 759, 1006
VIN, GWL, BUN = 437, 754, 1424
MYS = 425
GUJ, KUT = 1007, 428
KER = 758
KSH, JAM, AKS = 441, 1317, 947
INDIAN_REGIONS = [
    ("Bengal Presidency", [WBN, CBN, EBN, BIH, JHK, LOR, UOR, ASM, TRI, MNP]),
    ("North-Western Provinces", [LDB, UDB, DEL, HIM]),
    ("Oudh", [OUDH]),
    ("Punjab", [PJB, SIR, MUL, ISL]),
    ("Madras", [TML, AND, CIR, MLB]),
    ("Bombay and Sind", [NKK, SKK, SND, THA]),
    ("Central Provinces", [BER, BST]),
    ("British Burma", [KRN, BUR, RAK, NTN]),
    ("Hyderabad", [DEC]),
    ("Rajputana", [RJS, AGR, UDP, BIK]),
    ("Central India", [VIN, GWL, BUN]),
    ("Mysore", [MYS]),
    ("Baroda, Kathiawar, Cutch", [GUJ, KUT]),
    ("Travancore and Cochin", [KER]),
    ("Kashmir", [KSH, JAM, AKS]),
]
INDIAN_DOC_POP = {"Bengal Presidency": 40000, "North-Western Provinces": 30000, "Oudh": 9000, "Punjab": 14000, "Madras": 23000, "Bombay and Sind": 12000,
                  "Central Provinces": 6000, "British Burma": 2000, "Hyderabad": 11000, "Rajputana": 10000, "Central India": 9000, "Mysore": 4000,
                  "Baroda, Kathiawar, Cutch": 5000, "Travancore and Cochin": 2000, "Kashmir": 4000}
INDIAN_FARM_WORKERS = [([s for _, states in INDIAN_REGIONS for s in states], 70000)]
# Doc's subsistence table by region. Burma's lowlands aren't in it: 60% is a guess from its rice exports
INDIAN_SUBSISTENCE = merge({s: 0.45 for s in (WBN, CBN, EBN, BIH, LOR, NKK, SKK, SND, THA)}, {s: 0.5 for s in (LDB, UDB, DEL, OUDH)},
                           {s: 0.55 for s in (PJB, SIR, MUL, ISL, TML, AND, CIR, MLB)}, {s: 0.75 for s in (JHK, UOR, BER)}, {BST: 0.95},
                           {s: 0.85 for s in (ASM, TRI, MNP)}, {s: 0.6 for s in (KRN, BUR, RAK, NTN)},
                           {s: 0.6 for s in (DEC, RJS, AGR, UDP, BIK, VIN, GWL, BUN, MYS, GUJ, KUT, KER, KSH, JAM, AKS, HIM)})


def indian_items(pop):
    cities = by_population(pop, {WBN: 3, NKK: 3, TML: 2, DEL: 2, OUDH: 2, LDB: 2, DEC: 1.5, SKK: 1.5})
    rice = {CBN: 14, EBN: 13, WBN: 12, TML: 10, LOR: 8, BIH: 7, CIR: 7, AND: 3, MLB: 3, KRN: 3, ASM: 2, BUR: 2, RAK: 2, NKK: 1.5, SKK: 1.5, OUDH: 1.5, LDB: 1.5,
            TRI: 1, JHK: 1, KER: 1, MNP: 0.5}
    millets = {DEC: 20, SKK: 10, AND: 10, NKK: 8, TML: 8, RJS: 8, MYS: 8, GUJ: 7, BER: 6, AGR: 4, BIK: 3, UDP: 3, VIN: 3, KUT: 2}
    wheat = {UDB: 12, PJB: 8, SIR: 8, LDB: 7, DEL: 7, MUL: 6, OUDH: 6, BIH: 5, VIN: 5, GWL: 4, AGR: 4, BER: 4, ISL: 3, BUN: 3, UDP: 3, HIM: 2, RJS: 2, DEC: 2}
    dairy = by_population(pop, {GUJ: 2, PJB: 1.5, SIR: 1.5, MUL: 1.5, MYS: 1.3, LDB: 1.2, UDB: 1.2})
    cloth = by_population(pop, {KSH: 2, CIR: 1.5, LDB: 1.4, EBN: 1.3, WBN: 1.3, TML: 1.3, GUJ: 1.3, SKK: 1.3, CBN: 1.2, AND: 1.2, PJB: 1.2, NKK: 1.2})
    crafts = by_population(pop, {LDB: 1.5, AGR: 1.5, DEL: 1.5, PJB: 1.3, OUDH: 1.3, DEC: 1.2, TML: 1.2, WBN: 1.2})
    return [
        Item("rice_paddy", "food", "rice", 85, None, rice),
        Item("crop_farm", "food", "millets", 40, None, millets),
        Item("crop_farm", "food", "wheat", 25, None, wheat),
        Item("crop_farm", "food", "pulses, oilseeds, garden crops", 63, None, by_population(pop)),
        Item("livestock_ranch", "food", "milk, ghee, meat, fish", 50.5, 5000, dairy),  # The doc's herders
        Item("livestock_ranch", "fiber", "wool", 0.4, None, {MUL: 20, RJS: 20, PJB: 15, SIR: 10, BIK: 10, SND: 10, MYS: 10, THA: 5}),
        Item("cotton_plantation", "fiber", "cotton", 5.4, None, {GUJ: 28, BER: 20, DEC: 10, SKK: 10, NKK: 8, TML: 8, LDB: 6, UDB: 6, AND: 2, KUT: 2}),
        Item("cotton_plantation", "fiber", "jute", 0.9, None, {EBN: 85, CBN: 15}),
        Item("fiber", "fiber", "raw silk", 1.05, None, {CBN: 45, WBN: 15, MYS: 15, KSH: 15, EBN: 10}),
        Item("luxuries_plantation", "luxuries", "sugar", 12.5, None, {UDB: 8, LDB: 6, CBN: 5, DEL: 4, CIR: 4, OUDH: 3, WBN: 3, EBN: 3, BIH: 3, TML: 2, NKK: 2, SKK: 2, AND: 1}),
        Item("luxuries_plantation", "luxuries", "opium", 7.06, None, {BIH: 35, LDB: 25, GWL: 14, VIN: 12, UDP: 6, BUN: 5, AGR: 3}),
        Item("luxuries_plantation", "luxuries", "spices", 0.4, None, {MLB: 55, KER: 30, MYS: 10, TML: 5}),
        Item("luxuries_plantation", "luxuries", "coffee", 0.15, None, {MYS: 50, MLB: 35, TML: 15}),
        Item("luxuries_plantation", "luxuries", "tea", 0.04, None, {ASM: 90, HIM: 10}),
        Item("wood", "wood", "teak, sal", 1, 750, {NTN: 20, MLB: 15, KRN: 15, BUR: 15, HIM: 8, BER: 6, ASM: 6, KER: 5, JHK: 4, UOR: 3, MNP: 3}),
        Item("coal", "coal", "coal", 0.08, 10, {WBN: 1}),
        Item("iron", "iron", "bloom iron", 0.15, 45, {JHK: 28, BER: 22, DEC: 12, MYS: 10, TML: 10, HIM: 10, UOR: 5, BST: 3}),
        Item("copper", "copper", "copper", 0.03, 3, {JHK: 40, AGR: 35, HIM: 25}),
        Item("copper", "copper", "tin", 0.01, 1, {NTN: 1}),
        Item("valuables", "valuables", "gold, diamonds", 0.015, 5, {MLB: 35, BUN: 30, JHK: 20, ASM: 15}),
        Item("steel_foundry", "steel", "wootz, wrought iron", 0.2, 50, {DEC: 35, MYS: 20, TML: 15, JHK: 15, BER: 10, HIM: 5}),
        Item("tooling_workshop", "tools", "village tools, brass", 17.5, 1750, by_population(pop, {LDB: 2, UDB: 1.5, NKK: 1.3, SKK: 1.3})),
        Item("mechanical_works", "machinery", "dockyards, workshops", 0.5, 15, {NKK: 50, WBN: 40, TML: 10}),
        Item("chemical_plant", "chemicals", "saltpetre, salt, lac", 3.5, 170, {BIH: 40, LDB: 8, LOR: 8, UDB: 6, TML: 6, GUJ: 6, RJS: 6, ISL: 6, JHK: 6, DEL: 4, PJB: 4}),
        Item("chemical_plant", "chemicals", "indigo", 2.5, 30, {CBN: 35, BIH: 30, EBN: 8, LDB: 8, UDB: 7, WBN: 5, TML: 4, CIR: 3}),
        Item("consumer_goods_factory", "consumer_goods", "leather, jewellery, carpets", 35, 3500, crafts),
        Item("textile_mill", "textiles", "handloom cloth, silk, shawls", 40, 7000, cloth),
        Item("urban_center", "services", "trade, moneylending", 12, 3000, cities),
        Item("urban_center", "services", "village service castes", 10, 5000, by_population(pop)),
        Item("urban_center", "services", "road, river transport", 7.2, 1895, by_population(pop)),
        Item("urban_center", "services", "housing", 6.5, 0, cities),
        Item("urban_center", "services", "domestic service", 5, 2000, cities),
        Item("urban_center", "services", "professions", 5, 1000, cities),
        Item("entertainment_hub", "entertainment", "courts, festivals", 4, 750, {OUDH: 15, DEL: 12, LDB: 12, WBN: 12, DEC: 10, NKK: 8, TML: 8, MYS: 6, GWL: 6, GUJ: 5, RJS: 3, PJB: 3}),
        Item("railway", "transport", "rail", 0.5, 5, {NKK: 40, WBN: 40, TML: 20}),
        Item("port", "shipping", "shipping", 2.3, 100, {WBN: 40, NKK: 30, TML: 8, KRN: 6, THA: 5, MLB: 3, RAK: 2, NTN: 2, EBN: 2, CIR: 1, KUT: 1}),
    ]
