# cestina.py — lokální databáze cvičení z češtiny pro 4. třídu (bez AI)
import random

# ============================================================
# 1) VYJMENOVANÁ SLOVA — doplň i/í/y/ý
#    Každá položka: z = zadání s mezerou, o = správné písmeno, s = celé slovo
#    Skupiny mají vyvážený poměr tvrdého (y/ý) a měkkého (i/í).
# ============================================================
VYJMENOVANA = {
    "B": [
        {"z": "b_t", "o": "ý", "s": "být"},
        {"z": "náb_tek", "o": "y", "s": "nábytek"},
        {"z": "b_strý", "o": "y", "s": "bystrý"},
        {"z": "kob_la", "o": "y", "s": "kobyla"},
        {"z": "b_č", "o": "i", "s": "bič"},
        {"z": "b_lý", "o": "í", "s": "bílý"},
        {"z": "b_tva", "o": "i", "s": "bitva"},
        {"z": "nab_dka", "o": "í", "s": "nabídka"},
    ],
    "F": [
        {"z": "f_zika", "o": "y", "s": "fyzika"},
        {"z": "f_zik", "o": "y", "s": "fyzik"},
        {"z": "f_lm", "o": "i", "s": "film"},
        {"z": "f_alka", "o": "i", "s": "fialka"},
    ],
    "L": [
        {"z": "sl_šet", "o": "y", "s": "slyšet"},
        {"z": "ml_n", "o": "ý", "s": "mlýn"},
        {"z": "pl_n", "o": "y", "s": "plyn"},
        {"z": "l_ko", "o": "ý", "s": "lýko"},
        {"z": "l_ška", "o": "i", "s": "liška"},
        {"z": "l_st", "o": "i", "s": "list"},
        {"z": "l_pa", "o": "í", "s": "lípa"},
        {"z": "kl_d", "o": "i", "s": "klid"},
    ],
    "M": [
        {"z": "m_t", "o": "ý", "s": "mýt"},
        {"z": "m_š", "o": "y", "s": "myš"},
        {"z": "hm_z", "o": "y", "s": "hmyz"},
        {"z": "m_lit", "o": "ý", "s": "mýlit"},
        {"z": "m_č", "o": "í", "s": "míč"},
        {"z": "m_lý", "o": "i", "s": "milý"},
        {"z": "m_nce", "o": "i", "s": "mince"},
        {"z": "m_nuta", "o": "i", "s": "minuta"},
    ],
    "P": [
        {"z": "p_cha", "o": "ý", "s": "pýcha"},
        {"z": "p_tel", "o": "y", "s": "pytel"},
        {"z": "kop_to", "o": "y", "s": "kopyto"},
        {"z": "netop_r", "o": "ý", "s": "netopýr"},
        {"z": "p_vo", "o": "i", "s": "pivo"},
        {"z": "p_smeno", "o": "í", "s": "písmeno"},
        {"z": "p_la", "o": "i", "s": "pila"},
        {"z": "p_lný", "o": "i", "s": "pilný"},
    ],
    "S": [
        {"z": "s_n", "o": "y", "s": "syn"},
        {"z": "s_r", "o": "ý", "s": "sýr"},
        {"z": "s_tý", "o": "y", "s": "sytý"},
        {"z": "s_kora", "o": "ý", "s": "sýkora"},
        {"z": "s_lný", "o": "i", "s": "silný"},
        {"z": "s_la", "o": "í", "s": "síla"},
        {"z": "s_rka", "o": "i", "s": "sirka"},
        {"z": "s_gnál", "o": "i", "s": "signál"},
    ],
    "V": [
        {"z": "v_soký", "o": "y", "s": "vysoký"},
        {"z": "v_r", "o": "ý", "s": "výr"},
        {"z": "v_dra", "o": "y", "s": "vydra"},
        {"z": "žv_kat", "o": "ý", "s": "žvýkat"},
        {"z": "v_la", "o": "í", "s": "víla"},
        {"z": "v_dle", "o": "i", "s": "vidle"},
        {"z": "v_tr", "o": "í", "s": "vítr"},
        {"z": "v_set", "o": "i", "s": "viset"},
    ],
    "Z": [
        {"z": "brz_", "o": "y", "s": "brzy"},
        {"z": "jaz_k", "o": "y", "s": "jazyk"},
        {"z": "naz_vat", "o": "ý", "s": "nazývat"},
        {"z": "jaz_ček", "o": "ý", "s": "jazýček"},
        {"z": "z_ma", "o": "i", "s": "zima"},
        {"z": "z_p", "o": "i", "s": "zip"},
        {"z": "z_sk", "o": "i", "s": "zisk"},
        {"z": "z_dka", "o": "í", "s": "zídka"},
    ],
}

VYJMENOVANA_SKUPINY = list(VYJMENOVANA.keys())  # B, F, L, M, P, S, V, Z


# ============================================================
# 2) PÁDY — napiš slovo ve správném pádě (jednotné číslo)
#    Pořadí forem: 1.–7. pád
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
#    rod: m/ž/s · cislo: j/mn · pad: 1–7
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
#    U každého slova jsou vyplněné jen ty části, které slovo má.
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

def vyj_vygeneruj(skupiny, pocet):
    zasoba = []
    for sk in skupiny:
        for polozka in VYJMENOVANA.get(sk, []):
            zasoba.append(polozka)
    if not zasoba:
        return []
    polozky = []
    for _ in range(pocet):
        p = random.choice(zasoba)
        polozky.append({"typ": "vyj", "zadani": p["z"], "odp": p["o"], "slovo": p["s"]})
    return polozky


def pady_vygeneruj(pocet):
    polozky = []
    for _ in range(pocet):
        n = random.choice(PADY_SLOVA)
        pad = random.randint(2, 7)
        polozky.append({
            "typ": "pad",
            "slovo1": n["slovo"],
            "pad": pad,
            "zadani": f"Napiš slovo „{n['slovo']}“ v {pad}. pádě j. č. ({PAD_OTAZKY[pad]}):",
            "odp": n["formy"][pad - 1],
        })
    return polozky


def mluvnicke_vygeneruj(pocet):
    zasoba = MLUVNICKE[:]
    random.shuffle(zasoba)
    vybrane = zasoba[:pocet] if pocet <= len(zasoba) else [random.choice(MLUVNICKE) for _ in range(pocet)]
    polozky = []
    for m in vybrane:
        polozky.append({
            "typ": "kat",
            "veta": m["veta"], "slovo": m["slovo"],
            "rod": m["rod"], "cislo": m["cislo"], "pad": m["pad"],
        })
    return polozky


def stavba_vygeneruj(pocet):
    polozky = []
    for _ in range(pocet):
        s = random.choice(STAVBA)
        casti = [k for k in ("predpona", "koren", "pripona") if s[k]]
        cil = random.choice(casti)
        # zvýrazníme hledanou část tučně
        cast_text = s[cil]
        zvyrazneno = s["slovo"].replace(cast_text, f"<b>{cast_text}</b>", 1)
        polozky.append({
            "typ": "stavba",
            "slovo": s["slovo"],
            "zvyrazneno": zvyrazneno,
            "odp": CASTI_LABEL[cil],
        })
    return polozky


SUBMODULY = {
    "Vyjmenovaná slova (i/y)": "vyj",
    "Pády": "pady",
    "Mluvnické kategorie": "kat",
    "Stavba slova": "stavba",
}
