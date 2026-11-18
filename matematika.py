# matematika.py — lokální generátory matematických příkladů (bez AI)
import random

JMENA_Z = ["Sára", "Nela", "Eliška", "Anička", "Klárka"]
JMENA_M = ["Adam", "Tomáš", "Honza", "Petr", "Kuba"]
DOSPELI_Z = ["Maminka", "Babička", "Teta"]
DOSPELI_M = ["Tatínek", "Dědeček", "Strýček"]


# ---------- NELA (1. třída) ----------

def nela_scitani_odcitani(limit):
    if random.random() < 0.5:
        a = random.randint(0, limit)
        b = random.randint(0, limit - a)
        return {"typ": "cislo", "zadani": f"{a} + {b} =", "odpoved": a + b}
    a = random.randint(0, limit)
    b = random.randint(0, a)
    return {"typ": "cislo", "zadani": f"{a} − {b} =", "odpoved": a - b}


def nela_porovnavani(limit):
    a = random.randint(0, limit)
    if random.random() < 0.25:
        b = a
    else:
        b = random.randint(0, limit)
    odp = "=" if a == b else ("<" if a < b else ">")
    return {"typ": "porovnani", "a": a, "b": b, "odpoved": odp}


# ---------- SÁRA (4. třída) ----------

def sara_nasobilka():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    if random.random() < 0.5:
        return {"typ": "cislo", "zadani": f"{a} · {b} =", "odpoved": a * b}
    soucin = a * b
    return {"typ": "cislo", "zadani": f"{soucin} : {b} =", "odpoved": a}


def sara_dvojciferne():
    a = random.randint(11, 99)
    b = random.randint(2, 9)
    return {"typ": "cislo", "zadani": f"{a} · {b} =", "odpoved": a * b}


def sara_deleni_se_zbytkem():
    delitel = random.randint(2, 9)
    podil = random.randint(2, 10)
    zbytek = random.randint(1, delitel - 1)
    delenec = delitel * podil + zbytek
    return {"typ": "zbytek", "zadani": f"{delenec} : {delitel} =", "podil": podil, "zbytek": zbytek}


def sara_pisemne_scitani():
    a = random.randint(10, 980)
    b = random.randint(10, 1000 - a)
    return {"typ": "cislo", "zadani": f"{a} + {b} =", "odpoved": a + b}


def sara_pisemne_odcitani():
    a = random.randint(100, 999)
    b = random.randint(10, a)
    return {"typ": "cislo", "zadani": f"{a} − {b} =", "odpoved": a - b}


# ---------- SLOVNÍ ÚLOHY (šablony s dopočítaným výsledkem) ----------
# Princip: nejdřív zvolíme výsledek a mezičísla, pak dopočítáme celek.
# Tím je úloha vždy matematicky čistá a řešitelná pro 4. třídu.

def _sklon(n, jeden, dva, pet):
    # Česká shoda s číslem: 1 → jeden, 2–4 → dva, jinak → pet
    if n == 1:
        return jeden
    if 2 <= n <= 4:
        return dva
    return pet


def _ulp_sesity_tuzky():
    dosp = random.choice(DOSPELI_Z)
    k = random.randint(2, 5)
    cena_s = random.randint(12, 30)
    t = random.randint(2, 6)
    tuzka = random.randint(5, 20)
    celkem = k * cena_s + t * tuzka
    text = (f"{dosp} koupila {k} {_sklon(k, 'sešit', 'sešity', 'sešitů')} po {cena_s} Kč "
            f"a {t} {_sklon(t, 'tužku', 'tužky', 'tužek')}. "
            f"Za celý nákup zaplatila {celkem} Kč. Kolik stála jedna tužka?")
    return text, tuzka, "Kč"


def _ulp_jablka_hrusky():
    a = random.randint(3, 8)
    b = random.randint(3, 8)
    cj = random.randint(15, 30)
    ch = random.randint(15, 30)
    celkem = a * cj + b * ch
    text = (f"Maminka koupila {a} kg jablek a {b} kg hrušek. "
            f"Jeden kilogram jablek stál {cj} Kč. Za všechno zaplatila {celkem} Kč. "
            f"Kolik stál jeden kilogram hrušek?")
    return text, ch, "Kč"


def _ulp_penezenka():
    dosp = random.choice(DOSPELI_M)
    n = random.randint(3, 6)
    cena = random.randint(40, 120)
    cepice = random.randint(50, 200)
    zbytek = random.randint(20, 150)
    start = n * cena + cepice + zbytek
    text = (f"{dosp} měl v peněžence {start} Kč. Koupil {n} {_sklon(n, 'tričko', 'trička', 'triček')} "
            f"po {cena} Kč a jednu čepici. "
            f"V peněžence mu zbylo {zbytek} Kč. Kolik stála čepice?")
    return text, cepice, "Kč"


def _ulp_pastelky():
    krabic = random.randint(4, 8)
    v_krabici = random.randint(20, 50)
    deti = random.randint(3, 9)
    na_dite = random.randint(5, 20)
    zlomene = krabic * v_krabici - deti * na_dite
    if zlomene < 5:  # ať sedí shoda "pastelek bylo zlomených" (5+)
        return _ulp_pastelky()
    text = (f"Do třídy přivezli {krabic} {_sklon(krabic, 'krabici', 'krabice', 'krabic')} "
            f"po {v_krabici} pastelkách. "
            f"{zlomene} pastelek bylo zlomených. Zbylé pastelky se rozdělily rovným dílem "
            f"mezi {deti} {_sklon(deti, 'dítě', 'děti', 'dětí')}. Kolik pastelek dostalo každé dítě?")
    return text, na_dite, "pastelek"


def _ulp_pochod():
    e1 = random.randint(8, 18)
    treti = random.randint(5, 25)
    celkem = e1 + 2 * e1 + treti
    text = (f"Turistický pochod měl tři etapy. První etapa měla {e1} km, "
            f"druhá byla dvakrát delší než první. Celý pochod měl {celkem} km. "
            f"Kolik km měla třetí etapa?")
    return text, treti, "km"


def _ulp_bonbony():
    deti = random.randint(3, 8)
    na_dite = random.randint(4, 12)
    zbylo = random.randint(1, deti - 1) if deti > 1 else 1
    celkem = deti * na_dite + zbylo
    text = (f"V míse bylo {celkem} bonbonů. Rozdělily se rovným dílem "
            f"mezi {deti} {_sklon(deti, 'dítě', 'děti', 'dětí')}. "
            f"Kolik bonbonů dostalo každé dítě? (napiš počet na jedno dítě)")
    return text, na_dite, "bonbonů"


def _ulp_knihy():
    jm = random.choice(JMENA_Z + JMENA_M)
    za_den = random.randint(8, 25)
    dni = random.randint(3, 7)
    text = (f"{jm} čte každý den {za_den} stran. "
            f"Kolik stran přečte za {dni} {_sklon(dni, 'den', 'dny', 'dní')}?")
    return text, za_den * dni, "stran"


_SLOVNI_SABLONY = [
    _ulp_sesity_tuzky,
    _ulp_jablka_hrusky,
    _ulp_penezenka,
    _ulp_pastelky,
    _ulp_pochod,
    _ulp_bonbony,
    _ulp_knihy,
]


def sara_slovni_uloha():
    text, odp, jednotka = random.choice(_SLOVNI_SABLONY)()
    return {"typ": "slovni", "zadani": text, "odpoved": odp, "jednotka": jednotka}


# ---------- Sestavení testu ----------

NELA_MODULY = {
    "Sčítání a odčítání": "scitani_odcitani",
    "Porovnávání čísel (<, >, =)": "porovnavani",
}

SARA_MODULY = {
    "Malá násobilka a dělení": "nasobilka",
    "Násobení dvojciferného čísla": "dvojciferne",
    "Dělení se zbytkem": "zbytek",
    "Písemné sčítání (do 1000)": "pis_scitani",
    "Písemné odčítání (do 1000)": "pis_odcitani",
    "Slovní úlohy": "slovni",
}


def vygeneruj_test(modul, pocet, limit=10):
    polozky = []
    for _ in range(pocet):
        if modul == "scitani_odcitani":
            polozky.append(nela_scitani_odcitani(limit))
        elif modul == "porovnavani":
            polozky.append(nela_porovnavani(limit))
        elif modul == "nasobilka":
            polozky.append(sara_nasobilka())
        elif modul == "dvojciferne":
            polozky.append(sara_dvojciferne())
        elif modul == "zbytek":
            polozky.append(sara_deleni_se_zbytkem())
        elif modul == "pis_scitani":
            polozky.append(sara_pisemne_scitani())
        elif modul == "pis_odcitani":
            polozky.append(sara_pisemne_odcitani())
        elif modul == "slovni":
            polozky.append(sara_slovni_uloha())
    return polozky
