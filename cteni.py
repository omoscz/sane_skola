# cteni.py — lokální generátor slabik a slov pro trénink čtení (1. třída)
import random

SAMOHLASKY = ["a", "e", "i", "o", "u", "y", "á", "é", "í", "ó", "ú", "ů", "ý"]

SOUHLASKY = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n",
             "p", "r", "s", "t", "v", "z", "č", "ř", "š", "ž"]

# Kurátorský seznam jednoduchých českých slov pro začínající čtenáře.
# Slovo se nabídne jen tehdy, když jsou všechna jeho písmena mezi vybranými.
SLOVA = [
    "máma", "táta", "baba", "děda", "teta", "syn", "sestra", "bratr",
    "pes", "kočka", "koza", "kráva", "ovce", "myš", "ryba", "rak", "sova",
    "liška", "vlk", "los", "jelen", "zajíc", "husa", "kuře", "sele", "kůň",
    "oko", "ucho", "nos", "pusa", "ruka", "noha", "vlasy", "zub", "záda",
    "voda", "led", "sníh", "oheň", "mráz", "déšť", "duha", "mlha",
    "les", "pole", "louka", "hora", "řeka", "moře", "nebe", "slunce",
    "lípa", "dub", "růže", "mák", "tráva", "list", "květ", "houba",
    "auto", "kolo", "vlak", "loď", "letadlo", "míč", "panenka", "kostka",
    "dům", "okno", "dveře", "stůl", "židle", "postel", "lampa", "váza",
    "hrnec", "lžíce", "nůž", "talíř", "mísa", "sklo", "koš", "pytel",
    "sýr", "máslo", "chléb", "rohlík", "salám", "med", "sůl", "cukr",
    "mléko", "čaj", "polévka", "maso", "vejce", "jablko", "hruška",
    "banán", "meloun", "švestka", "třešně", "jahoda", "ořech", "mrkev",
    "pila", "mapa", "kniha", "sešit", "tužka", "guma", "pastelka",
    "lak", "luk", "sen", "den", "noc", "ráno", "večer", "rok", "léto",
    "zima", "jaro", "podzim", "čas", "hodiny", "minuta",
    "les", "sob", "vosa", "moucha", "včela", "pavouk", "motýl", "mravenec",
    "had", "žába", "ještěrka", "šnek", "rybník", "kapr", "štika",
    "lano", "síť", "jehla", "nit", "knoflík", "boty", "čepice", "šála",
    "tričko", "sukně", "ponožky", "rukavice", "kabát", "šaty",
    "malý", "velký", "nový", "starý", "teplý", "studený", "rychlý", "pomalý",
    "bílý", "černý", "modrý", "žlutý", "zelený", "hnědý", "šedý",
    "ano", "ne", "tady", "tam", "doma", "venku", "nahoře", "dole",
    "máma mele", "táta volá", "pes spí", "ryba plave", "sova houká",
]


def _slabiky_vse(samohlasky, souhlasky):
    # Otevřené slabiky typu souhláska + samohláska (ma, le, pí, ...)
    return [s + v for s in souhlasky for v in samohlasky]


def vygeneruj_slabiky(pocet, samohlasky, souhlasky):
    vse = _slabiky_vse(samohlasky, souhlasky)
    if not vse:
        return []
    if pocet <= len(vse):
        return random.sample(vse, pocet)
    return [random.choice(vse) for _ in range(pocet)]


def slova_pro_pismena(pismena):
    povolena = set(pismena)
    vysledek = []
    for slovo in SLOVA:
        # povolíme i mezeru (krátká spojení typu "pes spí")
        pismena_slova = set(slovo.replace(" ", ""))
        if pismena_slova <= povolena:
            vysledek.append(slovo)
    # odstraníme případné duplicity, zachováme pořadí
    videno = set()
    unikatni = []
    for s in vysledek:
        if s not in videno:
            videno.add(s)
            unikatni.append(s)
    return unikatni


def vygeneruj_slova(pocet, pismena):
    dostupna = slova_pro_pismena(pismena)
    if not dostupna:
        return []
    if pocet <= len(dostupna):
        return random.sample(dostupna, pocet)
    return [random.choice(dostupna) for _ in range(pocet)]
