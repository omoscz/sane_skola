# cestina.py — lokální databáze cvičení z češtiny pro 4. třídu (bez AI)
import random

# ============================================================
# 1) DIKTÁT — věty s vyjmenovanými slovy, doplň i/í/y/ý
#    Vyjmenovaná slova se píšou po B, L, M, P, S, V, Z.
#    Každá položka: (věta s mezerami "_", seznam správných písmen v pořadí)
# ============================================================
DIKTATY = {
    "B": [
        ("B_l jednou jeden starý ml_nář.", ["y", "ý"]),
        ("Musíš b_t do večera doma.", ["ý"]),
        ("Na dvoře stála hubená kob_la.", ["y"]),
        ("Náb_tek v ob_váku je nový.", ["y", "ý"]),
        ("B_strý chlapec b_dlí u lesa.", ["y", "y"]),
        ("Na louce se pásl velký b_k.", ["ý"]),
        ("Chlapec dostal b_lý b_č.", ["í", "i"]),
        ("To b_lo úplně ob_čejné ráno.", ["y", "y"]),
    ],
    "L": [
        ("Z dálky jsme sl_šeli hrom.", ["y"]),
        ("Starý ml_n stál u řeky.", ["ý"]),
        ("Na nebi se bl_skalo.", ["ý"]),
        ("Nesmíš pl_tvat vodou.", ["ý"]),
        ("Po běhu mě bolí l_tko.", ["ý"]),
        ("V zimě jezdíme na l_žích.", ["y"]),
        ("Dítě hlasitě vzl_kalo.", ["y"]),
        ("Na zahradě roste pel_něk a l_pa.", ["y", "í"]),
    ],
    "M": [
        ("Ráno si musíš um_t ruce.", ["ý"]),
        ("V trávě bzučel otravný hm_z.", ["y"]),
        ("Po cestě lezl pomalý hlem_žď.", ["ý"]),
        ("Nesmíš se v počtech m_lit.", ["ý"]),
        ("M_slivec šel brzy do lesa.", ["y"]),
        ("Doma máme malou bílou m_š.", ["y"]),
        ("Večer zapomněl zam_kat dveře.", ["y"]),
        ("M_lá holčička dostala nový m_č.", ["i", "í"]),
    ],
    "P": [
        ("Večer vylétl na lov netop_r.", ["ý"]),
        ("Kůň má tvrdé kop_to.", ["y"]),
        ("Nenos v sobě tolik p_chy.", ["ý"]),
        ("Dej brambory do p_tle.", ["y"]),
        ("Na sluníčku se třp_tí rosa.", ["y"]),
        ("Chlapec klop_tl o kámen.", ["ý"]),
        ("V trávě se mihl slep_š.", ["ý"]),
        ("P_lný žák psal p_smena.", ["i", "í"]),
    ],
    "S": [
        ("Na větvi seděla s_kora.", ["ý"]),
        ("K obědu byl dobrý s_r.", ["ý"]),
        ("Můj s_n chodí do školy.", ["y"]),
        ("Po velkém jídle byl s_tý.", ["y"]),
        ("Na poli pískal malý s_sel.", ["y"]),
        ("Venku bylo s_chravé počasí.", ["y"]),
        ("Had začal nebezpečně s_čet.", ["y"]),
        ("S_lný chlapec má velkou s_lu.", ["i", "í"]),
    ],
    "V": [
        ("Na stromě houkal v_r.", ["ý"]),
        ("U rybníka žila v_dra.", ["y"]),
        ("V_soká věž se tyčí k nebi.", ["y"]),
        ("Nesmíš žv_kat s plnou pusou.", ["ý"]),
        ("Musíš si na to zv_knout.", ["y"]),
        ("Na place byl velký pov_k.", ["y"]),
        ("Vlk začal v_t na měsíc.", ["ý"]),
        ("V_soký strom viděla v_la.", ["y", "í"]),
    ],
    "Z": [
        ("Přišel jsi dnes moc brz_.", ["y"]),
        ("Pejsek vyplázl růžový jaz_k.", ["y"]),
        ("Jak se to štěně bude naz_vat?", ["ý"]),
        ("Venku byla krutá z_ma.", ["i"]),
        ("Na bundě se zasekl z_p.", ["i"]),
        ("Firma měla letos velký z_sk.", ["i"]),
        ("Brz_ ráno mě bolel jaz_k.", ["y", "y"]),
    ],
}

DIKTATY_SKUPINY = list(DIKTATY.keys())  # B, L, M, P, S, V, Z


# ============================================================
# 2) PÁDY — napiš slovo ve správném pádě (jednotné číslo)
# ============================================================
PAD_OTAZKY = {
    1: "kdo, co",
    2: "koho, čeho",
    3: "komu, čemu",
    4: "koho, co",
    5: "oslovujeme, voláme",
    6: "o kom, o čem",
    7: "kým, čím",
}

PADY_SLOVA = [
    {"slovo": "pes", "formy": ["pes", "psa", "psovi", "psa", "pse", "psovi", "psem"]},
    {"slovo": "strom", "formy": ["strom", "stromu", "stromu", "strom", "strome", "stromě", "stromem"]},
    {"slovo": "hrad", "formy": ["hrad", "hradu", "hradu", "hrad", "hrade", "hradě", "hradem"]},
    {"slovo": "les", "formy": ["les", "lesa", "lesu", "les", "lese", "lese", "lesem"]},
    {"slovo": "muž", "formy": ["muž", "muže", "muži", "muže", "muži", "muži", "mužem"]},
    {"slovo": "žena", "formy": ["žena", "ženy", "ženě", "ženu", "ženo", "ženě", "ženou"]},
    {"slovo": "kniha", "formy": ["kniha", "knihy", "knize", "knihu", "kniho", "knize", "knihou"]},
    {"slovo": "ryba", "formy": ["ryba", "ryby", "rybě", "rybu", "rybo", "rybě", "rybou"]},
    {"slovo": "růže", "formy": ["růže", "růže", "růži", "růži", "růže", "růži", "růží"]},
    {"slovo": "město", "formy": ["město", "města", "městu", "město", "město", "městě", "městem"]},
    {"slovo": "okno", "formy": ["okno", "okna", "oknu", "okno", "okno", "okně", "oknem"]},
    {"slovo": "auto", "formy": ["auto", "auta", "autu", "auto", "auto", "autě", "autem"]},
]


# ============================================================
# 3) MLUVNICKÉ KATEGORIE — urči rod, číslo a pád zvýrazněného slova
# ============================================================
MLUVNICKE = [
    {"veta": "Na louce kvetou **květiny**.", "slovo": "květiny", "rod": "ž", "cislo": "mn", "pad": 1},
    {"veta": "Viděli jsme velkého **psa**.", "slovo": "psa", "rod": "m", "cislo": "j", "pad": 4},
    {"veta": "Maminka vaří dobrý **oběd**.", "slovo": "oběd", "rod": "m", "cislo": "j", "pad": 4},
    {"veta": "**Kočka** leží na gauči.", "slovo": "kočka", "rod": "ž", "cislo": "j", "pad": 1},
    {"veta": "Děti si hrají na **zahradě**.", "slovo": "zahradě", "rod": "ž", "cislo": "j", "pad": 6},
    {"veta": "Pavel dal dárek **babičce**.", "slovo": "babičce", "rod": "ž", "cislo": "j", "pad": 3},
    {"veta": "V lese rostou **houby**.", "slovo": "houby", "rod": "ž", "cislo": "mn", "pad": 1},
    {"veta": "Táta přijel novým **autem**.", "slovo": "autem", "rod": "s", "cislo": "j", "pad": 7},
    {"veta": "Na stole leží **kniha**.", "slovo": "kniha", "rod": "ž", "cislo": "j", "pad": 1},
    {"veta": "Mluvili jsme o **škole**.", "slovo": "škole", "rod": "ž", "cislo": "j", "pad": 6},
    {"veta": "Petr napsal **dopis**.", "slovo": "dopis", "rod": "m", "cislo": "j", "pad": 4},
    {"veta": "Na obloze svítí **hvězdy**.", "slovo": "hvězdy", "rod": "ž", "cislo": "mn", "pad": 1},
]


# ============================================================
# 4) STAVBA SLOVA — urči část slova (předpona / kořen / přípona)
# ============================================================
STAVBA = [
    {"slovo": "zahrádka", "predpona": "za", "koren": "hrád", "pripona": "ka"},
    {"slovo": "nápad", "predpona": "ná", "koren": "pad", "pripona": ""},
    {"slovo": "podchod", "predpona": "pod", "koren": "chod", "pripona": ""},
    {"slovo": "přístav", "predpona": "pří", "koren": "stav", "pripona": ""},
    {"slovo": "výlet", "predpona": "vý", "koren": "let", "pripona": ""},
    {"slovo": "zápis", "predpona": "zá", "koren": "pis", "pripona": ""},
    {"slovo": "učitel", "predpona": "", "koren": "uč", "pripona": "tel"},
    {"slovo": "lesík", "predpona": "", "koren": "les", "pripona": "ík"},
    {"slovo": "domek", "predpona": "", "koren": "dom", "pripona": "ek"},
    {"slovo": "rybník", "predpona": "", "koren": "ryb", "pripona": "ník"},
    {"slovo": "sklenička", "predpona": "", "koren": "sklen", "pripona": "ička"},
    {"slovo": "květina", "predpona": "", "koren": "květ", "pripona": "ina"},
]

CASTI_LABEL = {"predpona": "předpona", "koren": "kořen", "pripona": "přípona"}


# ============================================================
# Generátory
# ============================================================

def _vypln(text, odp):
    out = []
    k = 0
    for ch in text:
        if ch == "_":
            out.append(odp[k])
            k += 1
        else:
            out.append(ch)
    return "".join(out)


def diktat_vygeneruj(skupiny, pocet):
    zasoba = []
    for sk in skupiny:
        for veta, odp in DIKTATY.get(sk, []):
            zasoba.append((veta, odp))
    if not zasoba:
        return []
    random.shuffle(zasoba)
    if pocet <= len(zasoba):
        vybrane = zasoba[:pocet]
    else:
        vybrane = [random.choice(zasoba) for _ in range(pocet)]
    polozky = []
    for veta, odp in vybrane:
        polozky.append({"typ": "diktat", "text": veta, "odp": odp, "plny": _vypln(veta, odp)})
    return polozky


def pady_vygeneruj(pocet):
    polozky = []
    for _ in range(pocet):
        n = random.choice(PADY_SLOVA)
        pad = random.randint(2, 7)
        polozky.append({
            "typ": "pad",
            "zadani": f"Napiš slovo „{n['slovo']}“ v {pad}. pádě j. č. ({PAD_OTAZKY[pad]}):",
            "odp": n["formy"][pad - 1],
        })
    return polozky


def mluvnicke_vygeneruj(pocet):
    zasoba = MLUVNICKE[:]
    random.shuffle(zasoba)
    vybrane = zasoba[:pocet] if pocet <= len(zasoba) else [random.choice(MLUVNICKE) for _ in range(pocet)]
    return [{"typ": "kat", "veta": m["veta"], "slovo": m["slovo"],
             "rod": m["rod"], "cislo": m["cislo"], "pad": m["pad"]} for m in vybrane]


def stavba_vygeneruj(pocet):
    polozky = []
    for _ in range(pocet):
        s = random.choice(STAVBA)
        casti = [k for k in ("predpona", "koren", "pripona") if s[k]]
        cil = random.choice(casti)
        zvyrazneno = s["slovo"].replace(s[cil], f"<b>{s[cil]}</b>", 1)
        polozky.append({"typ": "stavba", "slovo": s["slovo"],
                        "zvyrazneno": zvyrazneno, "odp": CASTI_LABEL[cil]})
    return polozky


SUBMODULY = {
    "Diktát (vyjmenovaná slova)": "diktat",
    "Pády": "pady",
    "Mluvnické kategorie": "kat",
    "Stavba slova": "stavba",
}
