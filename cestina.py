# cestina.py — lokální databáze cvičení z češtiny pro 4. třídu (bez AI)
import random

# ============================================================
# 1) DIKTÁT — věty s vyjmenovanými slovy, doplň i/í/y/ý
#    Vyjmenovaná slova se píšou po B, L, M, P, S, V, Z.
#    Každá položka: (věta s mezerami "_", seznam správných písmen v pořadí)
# ============================================================
DIKTATY = {
    "B": [
        ("B_l jednou jeden starý ml_nář.", ["y", "y"]),
        ("Musíš b_t do večera doma.", ["ý"]),
        ("Na dvoře stála hubená kob_la.", ["y"]),
        ("Náb_tek v ob_váku je nový.", ["y", "ý"]),
        ("B_strý chlapec b_dlí u lesa.", ["y", "y"]),
        ("Na louce se pásl velký b_k.", ["ý"]),
        ("Chlapec dostal b_lý b_č.", ["í", "i"]),
        ("To b_lo úplně ob_čejné ráno.", ["y", "y"]),
        ("Pasáček měl na krku b_č.", ["i"]),
        ("Sníh byl úplně b_lý.", ["í"]),
        ("V kostele kázal starý b_skup.", ["i"]),
        ("Na poli dozrávalo zlaté ob_lí.", ["i"]),
        ("Rytíři svedli velkou b_tvu.", ["i"]),
        ("Dostali jsme výhodnou nab_dku.", ["í"]),
        ("K snídani si dal b_ftek.", ["i"]),
        ("Děti jely na b_cyklu.", ["i"]),
        ("B_strý žák psal b_lou křídou.", ["y", "í"]),
        ("Pasáček vzal b_č a hnal b_ka.", ["i", "ý"]),
        ("Na poli u b_dliště dozrálo ob_lí.", ["y", "i"]),
        ("Starý b_k měl na krku b_č.", ["ý", "i"]),
        ("Koupili jsme nový náb_tek i b_cykl.", ["y", "i"]),
        ("Dostali jsme nab_dku na nový náb_tek.", ["í", "y"]),
        ("Ob_vatelé města jedli b_fteky.", ["y", "i"]),
        ("B_lý kůň b_l na dvoře.", ["í", "y"]),
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
        ("Po lese běžela rezavá l_ška.", ["i"]),
        ("Na stole ležel popsaný l_st.", ["i"]),
        ("U cesty rostla vysoká l_pa.", ["í"]),
        ("Měj prosím trochu kl_du.", ["i"]),
        ("K obědu byla bramborová pol_vka.", ["í"]),
        ("Na keři dozrála sladká mal_na.", ["i"]),
        ("Dětem se l_bil nový film.", ["í"]),
        ("Kočka ráda l_že mléko.", ["í"]),
        ("Z dálky jsme sl_šeli l_šku.", ["y", "i"]),
        ("Starý ml_n stál u staré l_py.", ["ý", "í"]),
        ("Na l_žích jsem měl velký kl_d.", ["y", "i"]),
        ("Nesmíš pl_tvat, řekl to s kl_dem.", ["ý", "i"]),
        ("Dítě vzl_kalo, ale film se mu nakonec zal_bil.", ["y", "í"]),
        ("Na zahradě roste pel_něk i sladké mal_ny.", ["y", "i"]),
        ("Bolí mě l_tko, řekl s l_tostí.", ["ý", "í"]),
        ("Měl l_sou hlavu a v ruce l_st papíru.", ["y", "i"]),
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
        ("Byl to moc m_lý člověk.", ["i"]),
        ("Chlapec kopal do m_če.", ["í"]),
        ("Do automatu hodil m_nci.", ["i"]),
        ("Zbývá už jen jedna m_nuta.", ["i"]),
        ("Polévku nalila do m_sky.", ["i"]),
        ("Vyhrál nejlepší m_str.", ["i"]),
        ("Lukostřelec m_řil na terč.", ["í"]),
        ("Byla to krásná m_nulost.", ["i"]),
        ("M_slivec měl m_lou náladu.", ["y", "i"]),
        ("Doma máme m_š i malou m_sku.", ["y", "i"]),
        ("Nesmíš se m_lit o celou m_nutu.", ["ý", "i"]),
        ("Hlem_žď lezl pomalu k m_se.", ["ý", "í"]),
        ("V trávě byl hm_z i m_lý motýl.", ["y", "i"]),
        ("Musíš si zam_kat, řekl m_str.", ["y", "i"]),
        ("Ráno si musíš um_t m_sku.", ["ý", "i"]),
        ("M_val si hrál s m_čem.", ["ý", "í"]),
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
        ("K večeři měl táta p_vo.", ["i"]),
        ("Dědeček řezal dřevo p_lou.", ["i"]),
        ("Byl to moc p_lný žák.", ["i"]),
        ("Zazpívali jsme veselou p_seň.", ["í"]),
        ("Na tváři měl spoustu p_h.", ["i"]),
        ("Dopis podepsal jeho p_satel.", ["i"]),
        ("Letadlo řídil zkušený p_lot.", ["i"]),
        ("Napil se čisté p_tné vody.", ["i"]),
        ("P_lný chlapec zkoumal květní p_l.", ["i", "y"]),
        ("Kůň klop_tl o dřevěnou p_lu.", ["ý", "i"]),
        ("V p_tli si nesl láhev p_va.", ["y", "i"]),
        ("Slep_š se skrýval, když zněla p_seň.", ["ý", "í"]),
        ("Na sluníčku se třp_tí sklenice p_va.", ["y", "i"]),
        ("Netop_r přelétl nad p_lotovou kabinou.", ["ý", "i"]),
        ("Nenos v sobě tolik p_chy, řekl p_satel.", ["ý", "i"]),
        ("Dej brambory do p_tle a vedle polož p_lu.", ["y", "i"]),
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
        ("Byl to velmi s_lný muž.", ["i"]),
        ("Neměl už žádnou s_lu.", ["í"]),
        ("Škrtl o krabičku s_rkou.", ["i"]),
        ("Na semaforu svítil červený s_gnál.", ["i"]),
        ("Rybu chytili do velké s_tě.", ["í"]),
        ("Na palačinky si dal s_rup.", ["i"]),
        ("Bydlí na malém s_dlišti.", ["í"]),
        ("V dálce houkala s_réna.", ["i"]),
        ("Můj s_n je moc s_lný.", ["y", "i"]),
        ("S_kora se zamotala do s_tě.", ["ý", "í"]),
        ("Byl s_tý, ale měl ještě s_lu běžet.", ["y", "í"]),
        ("S_sel utíkal, když houkala s_réna.", ["y", "i"]),
        ("Na s_r nalil trochu s_rupu.", ["ý", "i"]),
        ("Bylo s_chravo, svítil jen s_gnál.", ["y", "i"]),
        ("Had začal s_čet, škrtl jsem s_rkou.", ["y", "i"]),
        ("S_n bydlí na s_dlišti.", ["y", "í"]),
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
        ("V pohádce vystupovala hodná v_la.", ["í"]),
        ("Seno nabíral na v_dle.", ["i"]),
        ("Venku foukal studený v_tr.", ["í"]),
        ("Obraz bude v_set na zdi.", ["i"]),
        ("Dospělí pili červené v_no.", ["í"]),
        ("Na pódium nastoupil v_těz.", ["í"]),
        ("Rád tě v_dím.", ["i"]),
        ("Hosty mile v_tali u dveří.", ["í"]),
        ("V_dra plavala, v dálce foukal v_tr.", ["y", "í"]),
        ("V_r houkal, když šla kolem v_la.", ["ý", "í"]),
        ("Na v_soké věži v_sel prapor.", ["y", "i"]),
        ("Musíš si zv_knout, že tě v_dí.", ["y", "i"]),
        ("Nesmíš žv_kat, když tě v_dí učitel.", ["ý", "i"]),
        ("Na place byl pov_k, pak nastoupil v_těz.", ["y", "í"]),
        ("Vlk začal v_t, všichni ho v_děli.", ["ý", "i"]),
        ("U rybníka žila v_dra i hodná v_la.", ["y", "í"]),
    ],
    "Z": [
        ("Přišel jsi dnes moc brz_.", ["y"]),
        ("Pejsek vyplázl růžový jaz_k.", ["y"]),
        ("Jak se to štěně bude naz_vat?", ["ý"]),
        ("Venku byla krutá z_ma.", ["i"]),
        ("Na bundě se zasekl z_p.", ["i"]),
        ("Firma měla letos velký z_sk.", ["i"]),
        ("Brz_ ráno mě bolel jaz_k.", ["y", "y"]),
        ("Letos byla mírná z_ma.", ["i"]),
        ("Rozbil se mi u bundy z_p.", ["i"]),
        ("Obchod měl velký z_sk.", ["i"]),
        ("Ráno jsem začal z_vat.", ["í"]),
        ("Snažil se z_skat dobré známky.", ["í"]),
        ("Nemůžu na to jen tak z_rat.", ["í"]),
        ("V plotě byla malá z_dka.", ["í"]),
        ("Brz_ ráno byla venku z_ma.", ["y", "i"]),
        ("Vyplázl jaz_k a zasekl si z_p.", ["y", "i"]),
        ("Obchod měl velký z_sk už brz_.", ["i", "y"]),
        ("Brz_ začal ze z_my z_vat.", ["y", "i", "í"]),
        ("Jaz_k ho bolel, začal z_rat do zdi.", ["y", "í"]),
        ("Chtěl z_skat míč hned brz_.", ["í", "y"]),
        ("Brz_ v z_mě napadl sníh.", ["y", "i"]),
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
    {"slovo": "pán", "formy": ["pán", "pána", "pánovi", "pána", "pane", "pánovi", "pánem"]},
    {"slovo": "syn", "formy": ["syn", "syna", "synovi", "syna", "synu", "synovi", "synem"]},
    {"slovo": "žák", "formy": ["žák", "žáka", "žákovi", "žáka", "žáku", "žákovi", "žákem"]},
    {"slovo": "učitel", "formy": ["učitel", "učitele", "učiteli", "učitele", "učiteli", "učiteli", "učitelem"]},
    {"slovo": "král", "formy": ["král", "krále", "králi", "krále", "králi", "králi", "králem"]},
    {"slovo": "kůň", "formy": ["kůň", "koně", "koni", "koně", "koni", "koni", "koněm"]},
    {"slovo": "stroj", "formy": ["stroj", "stroje", "stroji", "stroj", "stroji", "stroji", "strojem"]},
    {"slovo": "dům", "formy": ["dům", "domu", "domu", "dům", "dome", "domě", "domem"]},
    {"slovo": "škola", "formy": ["škola", "školy", "škole", "školu", "školo", "škole", "školou"]},
    {"slovo": "matka", "formy": ["matka", "matky", "matce", "matku", "matko", "matce", "matkou"]},
    {"slovo": "voda", "formy": ["voda", "vody", "vodě", "vodu", "vodo", "vodě", "vodou"]},
    {"slovo": "hlava", "formy": ["hlava", "hlavy", "hlavě", "hlavu", "hlavo", "hlavě", "hlavou"]},
    {"slovo": "píseň", "formy": ["píseň", "písně", "písni", "píseň", "písni", "písni", "písní"]},
    {"slovo": "kost", "formy": ["kost", "kosti", "kosti", "kost", "kosti", "kosti", "kostí"]},
    {"slovo": "moře", "formy": ["moře", "moře", "moři", "moře", "moře", "moři", "mořem"]},
    {"slovo": "pole", "formy": ["pole", "pole", "poli", "pole", "pole", "poli", "polem"]},
    {"slovo": "kuře", "formy": ["kuře", "kuřete", "kuřeti", "kuře", "kuře", "kuřeti", "kuřetem"]},
    {"slovo": "jablko", "formy": ["jablko", "jablka", "jablku", "jablko", "jablko", "jablku", "jablkem"]},
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
    {"veta": "Pod stolem spí **pes**.", "slovo": "pes", "rod": "m", "cislo": "j", "pad": 1},
    {"veta": "Děti pouštějí na louce **draka**.", "slovo": "draka", "rod": "m", "cislo": "j", "pad": 4},
    {"veta": "Na talíři zbyla **polévka**.", "slovo": "polévka", "rod": "ž", "cislo": "j", "pad": 1},
    {"veta": "Babička upekla sladké **koláče**.", "slovo": "koláče", "rod": "m", "cislo": "mn", "pad": 4},
    {"veta": "Chlapci hráli odpoledne **fotbal**.", "slovo": "fotbal", "rod": "m", "cislo": "j", "pad": 4},
    {"veta": "V akváriu plavou malé **rybky**.", "slovo": "rybky", "rod": "ž", "cislo": "mn", "pad": 1},
    {"veta": "Učitel psal na **tabuli**.", "slovo": "tabuli", "rod": "ž", "cislo": "j", "pad": 6},
    {"veta": "Maminka upekla výbornou **buchtu**.", "slovo": "buchtu", "rod": "ž", "cislo": "j", "pad": 4},
    {"veta": "Na nebi letí **ptáci**.", "slovo": "ptáci", "rod": "m", "cislo": "mn", "pad": 1},
    {"veta": "Dědeček sedí na **židli**.", "slovo": "židli", "rod": "ž", "cislo": "j", "pad": 6},
    {"veta": "Petr se bojí velké **bouřky**.", "slovo": "bouřky", "rod": "ž", "cislo": "j", "pad": 2},
    {"veta": "Dali jsme seno **koním**.", "slovo": "koním", "rod": "m", "cislo": "mn", "pad": 3},
    {"veta": "Na zahradě jsme našli **ježka**.", "slovo": "ježka", "rod": "m", "cislo": "j", "pad": 4},
    {"veta": "Pejsek vesele zavrtěl **ocasem**.", "slovo": "ocasem", "rod": "m", "cislo": "j", "pad": 7},
    {"veta": "Ve třídě visí velká **mapa**.", "slovo": "mapa", "rod": "ž", "cislo": "j", "pad": 1},
    {"veta": "Všichni se těšíme na **prázdniny**.", "slovo": "prázdniny", "rod": "ž", "cislo": "mn", "pad": 4},
    {"veta": "O víkendu pojedeme k **moři**.", "slovo": "moři", "rod": "s", "cislo": "j", "pad": 3},
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
    {"slovo": "učitel", "predpona": "", "koren": "uč", "pripona": "itel"},
    {"slovo": "lesík", "predpona": "", "koren": "les", "pripona": "ík"},
    {"slovo": "domek", "predpona": "", "koren": "dom", "pripona": "ek"},
    {"slovo": "rybník", "predpona": "", "koren": "ryb", "pripona": "ník"},
    {"slovo": "sklenička", "predpona": "", "koren": "sklen", "pripona": "ička"},
    {"slovo": "květina", "predpona": "", "koren": "květ", "pripona": "ina"},
    {"slovo": "prales", "predpona": "pra", "koren": "les", "pripona": ""},
    {"slovo": "nadpis", "predpona": "nad", "koren": "pis", "pripona": ""},
    {"slovo": "odchod", "predpona": "od", "koren": "chod", "pripona": ""},
    {"slovo": "rozchod", "predpona": "roz", "koren": "chod", "pripona": ""},
    {"slovo": "příchod", "predpona": "pří", "koren": "chod", "pripona": ""},
    {"slovo": "nálet", "predpona": "ná", "koren": "let", "pripona": ""},
    {"slovo": "stromek", "predpona": "", "koren": "strom", "pripona": "ek"},
    {"slovo": "lesník", "predpona": "", "koren": "les", "pripona": "ník"},
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
    zasoba = STAVBA[:]
    random.shuffle(zasoba)
    vyber = zasoba[:pocet] if pocet <= len(zasoba) else [random.choice(STAVBA) for _ in range(pocet)]
    return [{"typ": "stavba", "slovo": s["slovo"], "predpona": s["predpona"],
             "koren": s["koren"], "pripona": s["pripona"]} for s in vyber]


SUBMODULY = {
    "Diktát (vyjmenovaná slova)": "diktat",
    "Pády": "pady",
    "Mluvnické kategorie": "kat",
    "Stavba slova": "stavba",
}
