# anglictina.py — lokální cvičení angličtiny pro 4. třídu (bez AI)
import random
import unicodedata

# ============================================================
# 1) WH otázky — doplň tázací slovo (What / When / Where / Why / How)
#    Výslovnost podle sešitu: What [vot], When [ven], Where [vér], Why [vaj], How [hau]
# ============================================================
WH_MOZNOSTI = ["What", "When", "Where", "Why", "How"]

WH = [
    {"veta": "___ is your name?", "spravne": "What", "cesky": "Jak se jmenuješ?"},
    {"veta": "___ do you live?", "spravne": "Where", "cesky": "Kde bydlíš?"},
    {"veta": "___ is your birthday?", "spravne": "When", "cesky": "Kdy máš narozeniny?"},
    {"veta": "___ are you running?", "spravne": "Why", "cesky": "Proč běžíš?"},
    {"veta": "___ old are you?", "spravne": "How", "cesky": "Kolik ti je let?"},
    {"veta": "___ are you from?", "spravne": "Where", "cesky": "Odkud jsi?"},
    {"veta": "___ do you like?", "spravne": "What", "cesky": "Co máš rád(a)?"},
    {"veta": "___ are you today?", "spravne": "How", "cesky": "Jak se dnes máš?"},
    {"veta": "___ is your favourite colour?", "spravne": "What", "cesky": "Jaká je tvoje oblíbená barva?"},
    {"veta": "___ are you?", "spravne": "How", "cesky": "Jak se máš?"},
    {"veta": "___ is your favourite animal?", "spravne": "What", "cesky": "Jaké je tvoje oblíbené zvíře?"},
    {"veta": "___ are you crying?", "spravne": "Why", "cesky": "Proč pláčeš?"},
    {"veta": "___ is my bag?", "spravne": "Where", "cesky": "Kde je moje taška?"},
    {"veta": "___ old is your brother?", "spravne": "How", "cesky": "Kolik let je tvému bratrovi?"},
    {"veta": "___ do you get up?", "spravne": "When", "cesky": "Kdy vstáváš?"},
    {"veta": "___ is your favourite food?", "spravne": "What", "cesky": "Jaké je tvoje oblíbené jídlo?"},
    {"veta": "___ are you sad?", "spravne": "Why", "cesky": "Proč jsi smutný(á)?"},
    {"veta": "___ is the cat?", "spravne": "Where", "cesky": "Kde je ta kočka?"},
]


# ============================================================
# 2) Slovesa — to be (am/is/are), have got (have/has), can/can't
#    Každá položka má vlastní možnosti.
# ============================================================
_BE = ["am", "is", "are"]
_HAVE = ["have", "has"]
_CAN = ["can", "can't"]

# Při testu se u sloves nabízí vždy celá sada možností (ať to nenapovídá).
SLOVESA_MOZNOSTI = ["am", "is", "are", "have", "has", "can", "can't"]

SLOVESA = [
    # to be
    {"veta": "I ___ happy.", "moznosti": _BE, "spravne": "am", "cesky": "Jsem šťastný(á)."},
    {"veta": "You ___ my friend.", "moznosti": _BE, "spravne": "are", "cesky": "Jsi můj kamarád."},
    {"veta": "He ___ tall.", "moznosti": _BE, "spravne": "is", "cesky": "Je vysoký."},
    {"veta": "She ___ nice.", "moznosti": _BE, "spravne": "is", "cesky": "Je milá."},
    {"veta": "It ___ a cat.", "moznosti": _BE, "spravne": "is", "cesky": "Je to kočka."},
    {"veta": "We ___ ready.", "moznosti": _BE, "spravne": "are", "cesky": "Jsme připraveni."},
    {"veta": "They ___ at home.", "moznosti": _BE, "spravne": "are", "cesky": "Jsou doma."},
    {"veta": "I ___ nine years old.", "moznosti": _BE, "spravne": "am", "cesky": "Je mi devět let."},
    {"veta": "My name ___ Sára.", "moznosti": _BE, "spravne": "is", "cesky": "Jmenuji se Sára."},
    # have got
    {"veta": "I ___ got a dog.", "moznosti": _HAVE, "spravne": "have", "cesky": "Mám psa."},
    {"veta": "She ___ got a cat.", "moznosti": _HAVE, "spravne": "has", "cesky": "Má kočku."},
    {"veta": "He ___ got a bike.", "moznosti": _HAVE, "spravne": "has", "cesky": "Má kolo."},
    {"veta": "We ___ got a house.", "moznosti": _HAVE, "spravne": "have", "cesky": "Máme dům."},
    {"veta": "They ___ got a ball.", "moznosti": _HAVE, "spravne": "have", "cesky": "Mají míč."},
    {"veta": "It ___ got big ears.", "moznosti": _HAVE, "spravne": "has", "cesky": "Má velké uši."},
    # can / can't
    {"veta": "A bird ___ fly.", "moznosti": _CAN, "spravne": "can", "cesky": "Pták umí létat."},
    {"veta": "A fish ___ walk.", "moznosti": _CAN, "spravne": "can't", "cesky": "Ryba neumí chodit."},
    {"veta": "I ___ swim.", "moznosti": _CAN, "spravne": "can", "cesky": "Umím plavat."},
    {"veta": "A dog ___ talk.", "moznosti": _CAN, "spravne": "can't", "cesky": "Pes neumí mluvit."},
    {"veta": "She ___ sing well.", "moznosti": _CAN, "spravne": "can", "cesky": "Umí dobře zpívat."},
]


# ============================================================
# 3) Slovíčka — podle oblastí
#    Každé slovo: en (seznam přijatelných anglických tvarů),
#    vysl (výslovnost česky), cz (seznam přijatelných českých překladů).
#    První položka v en/cz je ta hlavní (zobrazuje se).
# ============================================================
SLOVICKA = {
    "Ovoce a zelenina": [
        {"en": ["apple"], "vysl": "[epl]", "cz": ["jablko"]},
        {"en": ["banana"], "vysl": "[benána]", "cz": ["banán"]},
        {"en": ["orange"], "vysl": "[orindž]", "cz": ["pomeranč"]},
        {"en": ["pear"], "vysl": "[pér]", "cz": ["hruška"]},
        {"en": ["plum"], "vysl": "[plam]", "cz": ["švestka"]},
        {"en": ["strawberry"], "vysl": "[stróberi]", "cz": ["jahoda"]},
        {"en": ["cherry"], "vysl": "[čeri]", "cz": ["třešně", "třešeň"]},
        {"en": ["lemon"], "vysl": "[lemon]", "cz": ["citron", "citrón"]},
        {"en": ["grapes"], "vysl": "[grejps]", "cz": ["hroznové víno", "hrozny", "víno"]},
        {"en": ["watermelon"], "vysl": "[votrmelon]", "cz": ["meloun", "vodní meloun"]},
        {"en": ["pineapple"], "vysl": "[pajnepl]", "cz": ["ananas"]},
        {"en": ["carrot"], "vysl": "[kerot]", "cz": ["mrkev"]},
        {"en": ["potato"], "vysl": "[potejto]", "cz": ["brambor", "brambora", "brambory"]},
        {"en": ["tomato"], "vysl": "[tomáto]", "cz": ["rajče", "rajské jablíčko"]},
        {"en": ["onion"], "vysl": "[aňjn]", "cz": ["cibule"]},
        {"en": ["cucumber"], "vysl": "[kjúkambr]", "cz": ["okurka"]},
        {"en": ["cabbage"], "vysl": "[kebidž]", "cz": ["zelí"]},
        {"en": ["mushroom"], "vysl": "[mašrum]", "cz": ["houba", "žampion"]},
        {"en": ["pea", "peas"], "vysl": "[pí]", "cz": ["hrášek", "hrách"]},
    ],
    "Dům": [
        {"en": ["house"], "vysl": "[haus]", "cz": ["dům"]},
        {"en": ["flat"], "vysl": "[flet]", "cz": ["byt"]},
        {"en": ["room"], "vysl": "[rúm]", "cz": ["pokoj", "místnost"]},
        {"en": ["kitchen"], "vysl": "[kičn]", "cz": ["kuchyně", "kuchyň"]},
        {"en": ["bathroom"], "vysl": "[bátrúm]", "cz": ["koupelna"]},
        {"en": ["bedroom"], "vysl": "[bedrúm]", "cz": ["ložnice"]},
        {"en": ["living room"], "vysl": "[living rúm]", "cz": ["obývací pokoj", "obývák"]},
        {"en": ["hall"], "vysl": "[hól]", "cz": ["předsíň", "hala", "chodba"]},
        {"en": ["garage"], "vysl": "[geráž]", "cz": ["garáž"]},
        {"en": ["garden"], "vysl": "[gárdn]", "cz": ["zahrada"]},
        {"en": ["door"], "vysl": "[dór]", "cz": ["dveře"]},
        {"en": ["window"], "vysl": "[vindou]", "cz": ["okno"]},
        {"en": ["wall"], "vysl": "[vól]", "cz": ["zeď", "stěna"]},
        {"en": ["roof"], "vysl": "[rúf]", "cz": ["střecha"]},
        {"en": ["floor"], "vysl": "[flór]", "cz": ["podlaha", "patro"]},
        {"en": ["stairs"], "vysl": "[stérs]", "cz": ["schody"]},
        {"en": ["table"], "vysl": "[tejbl]", "cz": ["stůl"]},
        {"en": ["chair"], "vysl": "[čér]", "cz": ["židle"]},
        {"en": ["bed"], "vysl": "[bed]", "cz": ["postel"]},
        {"en": ["sofa"], "vysl": "[soufa]", "cz": ["pohovka", "gauč"]},
        {"en": ["lamp"], "vysl": "[lemp]", "cz": ["lampa"]},
    ],
    "Rodina": [
        {"en": ["mother"], "vysl": "[madr]", "cz": ["matka"]},
        {"en": ["mum", "mom"], "vysl": "[mam]", "cz": ["máma", "maminka"]},
        {"en": ["father"], "vysl": "[fádr]", "cz": ["otec"]},
        {"en": ["dad"], "vysl": "[ded]", "cz": ["táta", "tatínek"]},
        {"en": ["sister"], "vysl": "[sistr]", "cz": ["sestra"]},
        {"en": ["brother"], "vysl": "[bradr]", "cz": ["bratr"]},
        {"en": ["grandmother"], "vysl": "[grendmadr]", "cz": ["babička"]},
        {"en": ["grandma", "granny"], "vysl": "[grenma]", "cz": ["babi", "babička"]},
        {"en": ["grandfather"], "vysl": "[grendfádr]", "cz": ["dědeček"]},
        {"en": ["grandpa", "grandad"], "vysl": "[grenpa]", "cz": ["děda", "dědeček"]},
        {"en": ["parents"], "vysl": "[pérents]", "cz": ["rodiče"]},
        {"en": ["son"], "vysl": "[san]", "cz": ["syn"]},
        {"en": ["daughter"], "vysl": "[dótr]", "cz": ["dcera"]},
        {"en": ["aunt"], "vysl": "[ánt]", "cz": ["teta"]},
        {"en": ["uncle"], "vysl": "[ankl]", "cz": ["strýc", "strejda"]},
        {"en": ["cousin"], "vysl": "[kazn]", "cz": ["bratranec", "sestřenice"]},
        {"en": ["baby"], "vysl": "[bejbi]", "cz": ["miminko", "mimino", "dítě"]},
        {"en": ["family"], "vysl": "[femili]", "cz": ["rodina"]},
    ],
}


# ============================================================
# Generátory a pomocné funkce
# ============================================================

def dopln_vygeneruj(skupina, pocet):
    zdroj = WH if skupina == "wh" else SLOVESA
    zasoba = zdroj[:]
    random.shuffle(zasoba)
    vyber = zasoba[:pocet] if pocet <= len(zasoba) else [random.choice(zdroj) for _ in range(pocet)]
    moznosti = WH_MOZNOSTI if skupina == "wh" else SLOVESA_MOZNOSTI
    polozky = []
    for p in vyber:
        polozky.append({
            "typ": "dopln",
            "veta": p["veta"],
            "moznosti": moznosti,
            "spravne": p["spravne"],
            "cesky": p["cesky"],
        })
    return polozky


def slovicka_sekce():
    return list(SLOVICKA.keys())


def slovicka_test_vygeneruj(sekce_list, smer, pocet):
    zasoba = []
    for s in sekce_list:
        zasoba += SLOVICKA.get(s, [])
    if not zasoba:
        return []
    random.shuffle(zasoba)
    vyber = zasoba[:pocet] if pocet <= len(zasoba) else [random.choice(zasoba) for _ in range(pocet)]
    polozky = []
    for w in vyber:
        if smer == "cz2en":
            polozky.append({"typ": "voc", "otazka": w["cz"][0], "spravne": w["en"],
                            "smer": smer, "vysl": w["vysl"]})
        else:
            polozky.append({"typ": "voc", "otazka": w["en"][0], "spravne": w["cz"],
                            "smer": smer, "vysl": w["vysl"]})
    return polozky


def _bez_diakritiky(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def _norm_en(s):
    s = (s or "").strip().lower()
    for pref in ("the ", "an ", "a "):
        if s.startswith(pref):
            s = s[len(pref):]
    return " ".join(s.split())


def _norm_cz(s):
    s = _bez_diakritiky((s or "").strip().lower())
    return " ".join(s.split())


def voc_ok(moje, spravne_list, smer):
    norm = _norm_en if smer == "cz2en" else _norm_cz
    m = norm(moje)
    if not m:
        return False
    return m in {norm(x) for x in spravne_list}
