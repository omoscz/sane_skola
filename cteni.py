# cteni.py — lokální generátor slabik a slov pro trénink čtení (1. třída)
import random

SAMOHLASKY = ["a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú", "ů", "y", "ý"]

SOUHLASKY = ["b", "c", "č", "d", "f", "g", "h", "j", "k", "l", "m",
             "n", "p", "r", "ř", "s", "š", "t", "v", "z", "ž"]

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
    # --- rozšíření: krátká a středně dlouhá slova (nic příliš dlouhého) ---
    "lev", "vůl", "osel", "bobr", "orel", "kos", "sokol", "holub", "brouk",
    "komár", "sumec", "ježek", "krtek", "beran", "kozel", "srna", "srnec",
    "labuť", "kachna", "kohout", "slepice", "vrabec", "straka", "vrána",
    "datel", "páv", "krocan", "delfín", "žralok", "velryba", "tygr", "slon",
    "tele", "kotě", "štěně", "kůzle", "prase", "mech",
    "dort", "koláč", "perník", "bonbon", "knedlík", "guláš", "buchta",
    "citron", "okurka", "rajče", "cibule", "brambor", "zelí", "hrách",
    "fazole", "paprika", "špenát", "rýže", "mandle", "rozinka", "malina",
    "borůvka", "meruňka", "broskev", "tvaroh", "jogurt",
    "hrnek", "miska", "pánev", "konev", "kbelík", "koště", "hadr", "mýdlo",
    "ručník", "hřeben", "deka", "peřina", "záclona", "police", "lavice",
    "křeslo", "truhla", "klíč", "zámek", "kladivo", "šroub", "hřebík",
    "kleště", "koberec", "skříň", "polštář",
    "keř", "lístek", "větev", "kořen", "šiška", "žalud", "kaštan", "kámen",
    "skála", "potok", "jezero", "kopec", "písek", "hlína", "bláto", "rosa",
    "blesk", "hrom", "mrak", "obloha", "hvězda", "měsíc", "vítr", "bouře",
    "hlava", "ústa", "jazyk", "brada", "tvář", "čelo", "krk", "dlaň", "prst",
    "nehet", "koleno", "pata", "břicho", "obočí", "řasa", "rameno", "loket",
    "strýc", "vnuk", "kluk", "holka", "dítě", "soused", "doktor", "svetr",
    "košile", "bunda", "mikina", "plavky", "klobouk", "kalhoty", "babička",
    "dědeček", "kamarád",
    "drak", "balón", "brusle", "sáňky", "lyže", "vláček", "autíčko", "hřiště",
    "nula", "jedna", "dva", "tři", "pět", "šest", "sedm", "osm", "devět", "deset",
    "lama", "kra", "jáma", "sláma", "brána", "váha", "páka", "síla", "víla",
    "lupa", "mez", "dar", "sad", "pár", "pán", "bod",
    "dnes", "zítra", "týden",
    "spí", "jí", "pije", "běží", "skáče", "letí", "zpívá", "maluje", "kreslí",
    "čte", "píše", "myje", "vaří", "peče", "kope", "hází", "nese", "veze",
    "sedí", "leží", "stojí",
    "máma mele", "táta volá", "pes spí", "ryba plave", "sova houká",
]


def _slabiky_vse(samohlasky, souhlasky):
    # Otevřené slabiky typu souhláska + samohláska (ma, le, pí, ...)
    return [s + v for s in souhlasky for v in samohlasky]


def vygeneruj_slabiky(pocet, samohlasky, souhlasky):
    vse = _slabiky_vse(samohlasky, souhlasky)
    if not vse:
        return []
    # bez opakování; když je možných míň než pocet, vrátíme jen tolik, kolik jde
    return random.sample(vse, min(pocet, len(vse)))


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
    # bez opakování; když je dostupných míň než pocet, vrátíme jen tolik, kolik jde
    return random.sample(dostupna, min(pocet, len(dostupna)))
