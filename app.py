import re
import urllib.parse

import streamlit as st

import matematika
import cteni
import cestina
import anglictina

st.set_page_config(page_title="Škola hrou", page_icon="🎒", layout="centered")


CERVENA = "#ff4b4b"  # barva pro špatně vyřešené zadání


def velky_text(text, velikost="2rem", barva=None):
    styl = f"font-size:{velikost};font-weight:600;margin:4px 0"
    if barva:
        styl += f";color:{barva}"
    st.markdown(
        f"<div style='{styl}'>{text}</div>",
        unsafe_allow_html=True,
    )


def whatsapp_odkazy(profil, modul_nazev, skore, pocet, chyby):
    radky = [f"📚 {profil} — {modul_nazev}", f"Skóre: {skore}/{pocet}"]
    if chyby:
        radky.append("")
        radky.append("Chyby:")
        for zadani, moje, spravne in chyby:
            radky.append(f"• {zadani}  tvá odpověď: {moje}  správně: {spravne}")
    else:
        radky.append("Všechno správně! 🎉")
    zprava = urllib.parse.quote("\n".join(radky))

    cisla = [("👩 mámě", st.secrets.get("WHATSAPP_MAMA")),
             ("👨 tátovi", st.secrets.get("WHATSAPP_TATA"))]
    sloupce = st.columns(2)
    i = 0
    for popisek, cislo in cisla:
        if cislo:
            with sloupce[i]:
                st.link_button(f"📲 Poslat {popisek}", f"https://wa.me/{cislo}?text={zprava}")
            i += 1
    if i == 0:
        st.caption("ℹ️ Pro odesílání na WhatsApp doplň čísla do Secrets (WHATSAPP_MAMA / WHATSAPP_TATA).")


def _mat_ok(profil, tid, i, p):
    # Je příklad vyřešený správně? (čte aktuální odpovědi ze session_state)
    if p["typ"] in ("cislo", "slovni"):
        return st.session_state.get(f"{profil}_odp_{tid}_{i}") == p["odpoved"]
    if p["typ"] == "zbytek":
        return (st.session_state.get(f"{profil}_podil_{tid}_{i}") == p["podil"]
                and st.session_state.get(f"{profil}_zbytek_{tid}_{i}") == p["zbytek"])
    return st.session_state.get(f"{profil}_cmp_{tid}_{i}") == p["odpoved"]  # porovnani


def spust_matematiku(profil, moduly):
    nazvy = list(moduly.keys())
    modul_nazev = st.selectbox("Vyber cvičení", nazvy, key=f"{profil}_modul")
    modul = moduly[modul_nazev]

    limit = 10
    if modul in ("scitani_odcitani", "porovnavani"):
        limit = st.radio("Do kolika počítáme?", [5, 10, 20], horizontal=True, index=1, key=f"{profil}_limit")

    pocet = st.slider("Počet příkladů", min_value=1, max_value=20, value=8, key=f"{profil}_pocet")

    if st.button("🎲 Vygenerovat příklady", type="primary", key=f"{profil}_gen"):
        test_id = st.session_state.get(f"{profil}_testid", 0) + 1
        st.session_state[f"{profil}_testid"] = test_id
        st.session_state[f"{profil}_test"] = {
            "polozky": matematika.vygeneruj_test(modul, pocet, limit),
            "modul_nazev": modul_nazev,
            "test_id": test_id,
            "zkontrolovano": False,
        }

    test = st.session_state.get(f"{profil}_test")
    if not test:
        return

    tid = test["test_id"]
    st.write("---")

    zkontrolovano = test.get("zkontrolovano")
    for i, p in enumerate(test["polozky"]):
        barva = CERVENA if (zkontrolovano and not _mat_ok(profil, tid, i, p)) else None
        if p["typ"] in ("cislo", "slovni"):
            if p["typ"] == "slovni":
                if barva:
                    st.markdown(f"<span style='color:{barva}'>{p['zadani']}</span>",
                                unsafe_allow_html=True)
                else:
                    st.markdown(p['zadani'])
            else:
                velky_text(p['zadani'], barva=barva)
            st.number_input("odpověď", value=None, step=1, format="%d",
                            key=f"{profil}_odp_{tid}_{i}", label_visibility="collapsed")
        elif p["typ"] == "zbytek":
            velky_text(p['zadani'], barva=barva)
            c1, c2 = st.columns(2)
            with c1:
                st.number_input("podíl", value=None, step=1, format="%d", key=f"{profil}_podil_{tid}_{i}")
            with c2:
                st.number_input("zbytek", value=None, step=1, format="%d", key=f"{profil}_zbytek_{tid}_{i}")
        elif p["typ"] == "porovnani":
            velky_text(f"{p['a']} &nbsp;?&nbsp; {p['b']}", "2.4rem", barva=barva)
            st.pills("znaménko", ["<", "=", ">"], selection_mode="single",
                     format_func=lambda z: {"<": "\\<", ">": "\\>"}.get(z, z),
                     key=f"{profil}_cmp_{tid}_{i}", label_visibility="collapsed")
        st.write("")

    if st.button("✅ Zkontrolovat", type="primary", key=f"{profil}_check_{tid}"):
        test["zkontrolovano"] = True
        st.rerun()

    if not test.get("zkontrolovano"):
        return

    st.write("---")
    skore = 0
    chyby = []
    for i, p in enumerate(test["polozky"]):
        if p["typ"] in ("cislo", "slovni"):
            moje = st.session_state.get(f"{profil}_odp_{tid}_{i}")
            spravne = p["odpoved"]
            ok = (moje == spravne)
            moje_str = "—" if moje is None else str(moje)
            spravne_str = str(spravne) + (f" {p['jednotka']}" if p["typ"] == "slovni" else "")
        elif p["typ"] == "zbytek":
            mp = st.session_state.get(f"{profil}_podil_{tid}_{i}")
            mz = st.session_state.get(f"{profil}_zbytek_{tid}_{i}")
            ok = (mp == p["podil"] and mz == p["zbytek"])
            moje_str = f"{'—' if mp is None else mp} zb. {'—' if mz is None else mz}"
            spravne_str = f"{p['podil']} zb. {p['zbytek']}"
        else:  # porovnani
            moje = st.session_state.get(f"{profil}_cmp_{tid}_{i}")
            ok = (moje == p["odpoved"])
            moje_str = moje or "—"
            spravne_str = p["odpoved"]
            p_zadani = f"{p['a']} ? {p['b']}"

        zadani = p["zadani"] if p["typ"] != "porovnani" else p_zadani
        if ok:
            skore += 1
            st.markdown(f"✅ {zadani}  →  {spravne_str}")
        else:
            st.markdown(f"❌ {zadani}  →  tvoje: {moje_str} · správně: **{spravne_str}**")
            chyby.append((zadani, moje_str, spravne_str))

    pocet = len(test["polozky"])
    st.write("---")
    velky_text(f"Skóre: {skore} / {pocet}", "1.6rem")
    if skore == pocet:
        st.balloons()
        st.success("🎉 Všechno správně! Výborně!")

    if profil == "Sára":
        st.write("---")
        whatsapp_odkazy(profil, test["modul_nazev"], skore, pocet, chyby)


def _vyber_pismen(nadpis, pismena, key):
    # Výběr písmen přes klikací pilulky (zalamují se v pořadí na PC i mobilu).
    with st.expander(nadpis, expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Označit vše", key=f"{key}_all", use_container_width=True):
                st.session_state[key] = list(pismena)
                st.rerun()
        with c2:
            if st.button("Zrušit", key=f"{key}_clear", use_container_width=True):
                st.session_state[key] = []
                st.rerun()
        vybrane = st.pills(nadpis, pismena, selection_mode="multi",
                           format_func=str.upper, key=key, label_visibility="collapsed")
    return vybrane or []


def spust_cteni():
    st.caption("Rodič: označ písmena, která už Nela zná. Appka složí slabiky a slova jen z nich.")

    vybrane_samohlasky = _vyber_pismen("🔵 Samohlásky", cteni.SAMOHLASKY, "cteni_sam")
    vybrane_souhlasky = _vyber_pismen("🟢 Souhlásky", cteni.SOUHLASKY, "cteni_souh")

    rezim = st.radio("Co trénujeme?", ["Slabiky", "Slova"], horizontal=True, key="cteni_rezim")
    pocet = st.slider("Kolik jich ukázat?", min_value=3, max_value=24, value=9, key="cteni_pocet")

    if st.button("👀 Ukázat", type="primary", key="cteni_gen"):
        pismena = vybrane_samohlasky + vybrane_souhlasky
        if rezim == "Slabiky":
            if not vybrane_samohlasky or not vybrane_souhlasky:
                st.warning("Vyber aspoň jednu samohlásku a jednu souhlásku.")
                st.session_state.pop("cteni_polozky", None)
            else:
                st.session_state["cteni_polozky"] = cteni.vygeneruj_slabiky(
                    pocet, vybrane_samohlasky, vybrane_souhlasky)
        else:
            polozky = cteni.vygeneruj_slova(pocet, pismena)
            if not polozky:
                st.warning("Z vybraných písmen zatím nejde složit žádné slovo. Zkus přidat další písmena.")
                st.session_state.pop("cteni_polozky", None)
            else:
                st.session_state["cteni_polozky"] = polozky

    polozky = st.session_state.get("cteni_polozky")
    if polozky:
        st.write("---")
        for radek_start in range(0, len(polozky), 3):
            cols = st.columns(3)
            for j, slovo in enumerate(polozky[radek_start:radek_start + 3]):
                with cols[j]:
                    st.markdown(
                        f"<div style='font-size:2.6rem;font-weight:700;text-align:center;"
                        f"text-transform:uppercase;letter-spacing:2px;"
                        f"padding:14px;margin:6px 0;border-radius:12px;"
                        f"background:rgba(120,120,120,0.12)'>{slovo}</div>",
                        unsafe_allow_html=True,
                    )


ROD_MAP = {"mužský": "m", "ženský": "ž", "střední": "s"}
CISLO_MAP = {"jednotné": "j", "množné": "mn"}
ROD_NAZEV = {"m": "mužský", "ž": "ženský", "s": "střední"}
CISLO_NAZEV = {"j": "jednotné", "mn": "množné"}


def _cj_ok(tid, i, p):
    # Je položka češtiny vyřešená správně? (čte aktuální odpovědi ze session_state)
    if p["typ"] == "diktat":
        return all(st.session_state.get(f"cj_{tid}_{i}_b{j}") == sp
                   for j, sp in enumerate(p["odp"]))
    if p["typ"] == "stavba":
        mpr_ = (st.session_state.get(f"cj_{tid}_{i}_pred") or "").strip().lower()
        mk = (st.session_state.get(f"cj_{tid}_{i}_kor") or "").strip().lower()
        mpp = (st.session_state.get(f"cj_{tid}_{i}_prip") or "").strip().lower()
        return mpr_ == p["predpona"] and mk == p["koren"] and mpp == p["pripona"]
    if p["typ"] == "druhy":
        moje_pj = set(st.session_state.get(f"cj_{tid}_{i}_pj") or [])
        moje_sl = set(st.session_state.get(f"cj_{tid}_{i}_sl") or [])
        return moje_pj == set(p["podst"]) and moje_sl == set(p["slovesa"])
    if p["typ"] == "pad":
        return (st.session_state.get(f"cj_{tid}_{i}") or "").strip().lower() == p["odp"].lower()
    # kat
    mr = st.session_state.get(f"cj_{tid}_{i}_rod")
    mc = st.session_state.get(f"cj_{tid}_{i}_cislo")
    mp_ = st.session_state.get(f"cj_{tid}_{i}_pad")
    return (ROD_MAP.get(mr) == p["rod"] and CISLO_MAP.get(mc) == p["cislo"]
            and mp_ == str(p["pad"]))


def spust_cestinu():
    nazvy = list(cestina.SUBMODULY.keys())
    sub_nazev = st.selectbox("Vyber cvičení", nazvy, key="cj_sub")
    sub = cestina.SUBMODULY[sub_nazev]

    skupiny = None
    if sub == "diktat":
        skupiny = st.multiselect("Skupiny (podle písmene)", cestina.DIKTATY_SKUPINY,
                                 default=cestina.DIKTATY_SKUPINY, key="cj_skupiny")

    pocet_label = "Počet vět" if sub == "diktat" else "Počet příkladů"
    pocet = st.slider(pocet_label, min_value=1, max_value=20, value=8, key="cj_pocet")

    if st.button("🎲 Vygenerovat", type="primary", key="cj_gen"):
        if sub == "diktat" and not skupiny:
            st.warning("Vyber aspoň jednu skupinu písmen.")
        else:
            tid = st.session_state.get("cj_testid", 0) + 1
            st.session_state["cj_testid"] = tid
            if sub == "diktat":
                pol = cestina.diktat_vygeneruj(skupiny, pocet)
            elif sub == "pady":
                pol = cestina.pady_vygeneruj(pocet)
            elif sub == "kat":
                pol = cestina.mluvnicke_vygeneruj(pocet)
            elif sub == "druhy":
                pol = cestina.druhy_vygeneruj(pocet)
            else:
                pol = cestina.stavba_vygeneruj(pocet)
            st.session_state["cj_test"] = {
                "polozky": pol, "sub_nazev": sub_nazev, "test_id": tid, "zkontrolovano": False,
            }

    test = st.session_state.get("cj_test")
    if not test:
        return
    tid = test["test_id"]
    st.write("---")

    zkontrolovano = test.get("zkontrolovano")
    for i, p in enumerate(test["polozky"]):
        barva = CERVENA if (zkontrolovano and not _cj_ok(tid, i, p)) else None
        cislo = f"{i + 1}.&nbsp;&nbsp;"
        if p["typ"] == "diktat":
            velky_text(f"{cislo}{p['text']}", "1.3rem", barva=barva)
            pocet_mezer = len(p["odp"])
            cols = st.columns(pocet_mezer)
            for j in range(pocet_mezer):
                with cols[j]:
                    st.radio(f"mezera {j + 1}", ["i", "í", "y", "ý"], index=None,
                             key=f"cj_{tid}_{i}_b{j}", label_visibility="collapsed")
        elif p["typ"] == "pad":
            velky_text(f"{cislo}{p['zadani']}", "1.1rem", barva=barva)
            st.text_input("odpověď", key=f"cj_{tid}_{i}", label_visibility="collapsed")
        elif p["typ"] == "kat":
            veta_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p["veta"])
            velky_text(f"{cislo}{veta_html}", "1.1rem", barva=barva)
            st.caption(f"Urči u slova „{p['slovo']}“:")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.radio("rod", ["mužský", "ženský", "střední"], index=None, key=f"cj_{tid}_{i}_rod")
            with c2:
                st.radio("číslo", ["jednotné", "množné"], index=None, key=f"cj_{tid}_{i}_cislo")
            with c3:
                st.radio("pád", ["1", "2", "3", "4", "5", "6", "7"], index=None, key=f"cj_{tid}_{i}_pad")
        elif p["typ"] == "stavba":
            velky_text(f"{cislo}{p['slovo']}", barva=barva)
            st.caption("Rozděl slovo. Pokud některá část chybí, nech políčko prázdné.")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input("Předpona", key=f"cj_{tid}_{i}_pred")
            with c2:
                st.text_input("Kořen", key=f"cj_{tid}_{i}_kor")
            with c3:
                st.text_input("Přípona", key=f"cj_{tid}_{i}_prip")
        elif p["typ"] == "druhy":
            velky_text(f"{cislo}{p['veta']}", "1.3rem", barva=barva)
            st.caption("Klikni na podstatná jména (můžeš jich označit víc):")
            st.pills("podstatná jména", p["slova"], selection_mode="multi",
                     key=f"cj_{tid}_{i}_pj", label_visibility="collapsed")
            st.caption("Klikni na slovesa:")
            st.pills("slovesa", p["slova"], selection_mode="multi",
                     key=f"cj_{tid}_{i}_sl", label_visibility="collapsed")
        st.write("")

    if st.button("✅ Zkontrolovat", type="primary", key=f"cj_check_{tid}"):
        test["zkontrolovano"] = True
        st.rerun()
    if not test.get("zkontrolovano"):
        return

    st.write("---")
    ziskano = 0
    maximum = 0
    chyby = []
    for i, p in enumerate(test["polozky"]):
        if p["typ"] == "diktat":
            spravne_blanky = 0
            moje_pismena = []
            for j, spravne_p in enumerate(p["odp"]):
                moje_p = st.session_state.get(f"cj_{tid}_{i}_b{j}")
                moje_pismena.append(moje_p or "_")
                if moje_p == spravne_p:
                    spravne_blanky += 1
            maximum += len(p["odp"])
            ziskano += spravne_blanky
            ok = (spravne_blanky == len(p["odp"]))
            zadani = p["text"]
            moje_str = cestina._vypln(p["text"], moje_pismena) if "_" not in moje_pismena else " / ".join(moje_pismena)
            spravne_str = p["plny"]
        elif p["typ"] == "stavba":
            mpr_ = (st.session_state.get(f"cj_{tid}_{i}_pred") or "").strip().lower()
            mk = (st.session_state.get(f"cj_{tid}_{i}_kor") or "").strip().lower()
            mpp = (st.session_state.get(f"cj_{tid}_{i}_prip") or "").strip().lower()
            cor = int(mpr_ == p["predpona"]) + int(mk == p["koren"]) + int(mpp == p["pripona"])
            maximum += 3
            ziskano += cor
            ok = (cor == 3)
            zadani = f"rozděl „{p['slovo']}“"
            moje_str = f"před: {mpr_ or '–'} / kořen: {mk or '–'} / příp: {mpp or '–'}"
            spravne_str = (f"před: {p['predpona'] or '–'} / kořen: {p['koren']} / "
                           f"příp: {p['pripona'] or '–'}")
        elif p["typ"] == "druhy":
            moje_pj = set(st.session_state.get(f"cj_{tid}_{i}_pj") or [])
            moje_sl = set(st.session_state.get(f"cj_{tid}_{i}_sl") or [])
            spr_pj = set(p["podst"])
            spr_sl = set(p["slovesa"])
            # bod za každé správně označené slovo, mínus za chybně označené (min. 0)
            bod_pj = max(0, len(moje_pj & spr_pj) - len(moje_pj - spr_pj))
            bod_sl = max(0, len(moje_sl & spr_sl) - len(moje_sl - spr_sl))
            maximum += len(spr_pj) + len(spr_sl)
            ziskano += bod_pj + bod_sl
            ok = (moje_pj == spr_pj and moje_sl == spr_sl)
            zadani = p["veta"]
            moje_str = (f"podst.: {', '.join(sorted(moje_pj)) or '—'} · "
                        f"slovesa: {', '.join(sorted(moje_sl)) or '—'}")
            spravne_str = (f"podst.: {', '.join(p['podst'])} · "
                           f"slovesa: {', '.join(p['slovesa'])}")
        else:
            maximum += 1
            if p["typ"] == "pad":
                moje = (st.session_state.get(f"cj_{tid}_{i}") or "").strip()
                ok = (moje.lower() == p["odp"].lower())
                zadani = p["zadani"]
                moje_str = moje or "—"
                spravne_str = p["odp"]
            else:  # kat
                mr = st.session_state.get(f"cj_{tid}_{i}_rod")
                mc = st.session_state.get(f"cj_{tid}_{i}_cislo")
                mp_ = st.session_state.get(f"cj_{tid}_{i}_pad")
                ok = (ROD_MAP.get(mr) == p["rod"] and CISLO_MAP.get(mc) == p["cislo"] and mp_ == str(p["pad"]))
                zadani = f"„{p['slovo']}“ — rod/číslo/pád"
                moje_str = f"{mr or '—'} / {mc or '—'} / {mp_ or '—'}"
                spravne_str = f"{ROD_NAZEV[p['rod']]} / {CISLO_NAZEV[p['cislo']]} / {p['pad']}."
            if ok:
                ziskano += 1

        if ok:
            st.markdown(f"✅ **{i + 1}.** {zadani}  →  {spravne_str}")
        else:
            st.markdown(f"❌ **{i + 1}.** {zadani}  →  tvoje: {moje_str} · správně: **{spravne_str}**")
            chyby.append((zadani, moje_str, spravne_str))

    st.write("---")
    velky_text(f"Skóre: {ziskano} / {maximum}", "1.6rem")
    if maximum and ziskano == maximum:
        st.balloons()
        st.success("🎉 Všechno správně! Výborně!")

    st.write("---")
    whatsapp_odkazy("Sára", test["sub_nazev"], ziskano, maximum, chyby)


# ===================== ANGLIČTINA =====================

def _aj_dopln(skupina, nazev):
    # Doplňovací cvičení s pilulkami (WH otázky i slovesa)
    pocet = st.slider("Počet vět", min_value=1, max_value=20, value=8, key=f"aj_{skupina}_pocet")
    if st.button("🎲 Vygenerovat", type="primary", key=f"aj_{skupina}_gen"):
        tid = st.session_state.get(f"aj_{skupina}_tid", 0) + 1
        st.session_state[f"aj_{skupina}_tid"] = tid
        st.session_state[f"aj_{skupina}_test"] = {
            "polozky": anglictina.dopln_vygeneruj(skupina, pocet), "tid": tid, "zkont": False,
        }

    test = st.session_state.get(f"aj_{skupina}_test")
    if not test:
        return
    tid = test["tid"]
    st.write("---")
    zkont = test.get("zkont")

    for i, p in enumerate(test["polozky"]):
        moje = st.session_state.get(f"aj_{skupina}_{tid}_{i}")
        barva = CERVENA if (zkont and moje != p["spravne"]) else None
        velky_text(p["veta"].replace("___", "_____"), "1.4rem", barva=barva)
        st.caption(p["cesky"])
        st.pills("odpoved", p["moznosti"], selection_mode="single",
                 key=f"aj_{skupina}_{tid}_{i}", label_visibility="collapsed")
        st.write("")

    if st.button("✅ Zkontrolovat", type="primary", key=f"aj_{skupina}_check_{tid}"):
        test["zkont"] = True
        st.rerun()
    if not test.get("zkont"):
        return

    st.write("---")
    skore = 0
    chyby = []
    for i, p in enumerate(test["polozky"]):
        moje = st.session_state.get(f"aj_{skupina}_{tid}_{i}")
        zadani = p["veta"].replace("___", "_____")
        if moje == p["spravne"]:
            skore += 1
            st.markdown(f"✅ {zadani}  →  **{p['spravne']}**")
        else:
            st.markdown(f"❌ {zadani}  →  tvoje: {moje or '—'} · správně: **{p['spravne']}**")
            chyby.append((zadani, moje or "—", p["spravne"]))

    pocet = len(test["polozky"])
    st.write("---")
    velky_text(f"Skóre: {skore} / {pocet}", "1.6rem")
    if skore == pocet:
        st.balloons()
        st.success("🎉 Všechno správně! Výborně!")
    st.write("---")
    whatsapp_odkazy("Sára", f"Angličtina – {nazev}", skore, pocet, chyby)


def _aj_slovicka():
    rezim = st.radio("Co chceš dělat?", ["Prohlížet slovíčka", "Test"],
                     horizontal=True, key="aj_voc_rezim")
    sekce = st.multiselect("Oblasti slovíček", anglictina.slovicka_sekce(),
                           default=anglictina.slovicka_sekce(), key="aj_voc_sekce")
    if not sekce:
        st.warning("Vyber aspoň jednu oblast.")
        return

    if rezim == "Prohlížet slovíčka":
        for s in sekce:
            st.subheader(s)
            radky = [{"Anglicky": w["en"][0], "Výslovnost": w["vysl"], "Česky": " / ".join(w["cz"])}
                     for w in anglictina.SLOVICKA[s]]
            st.table(radky)
        return

    # --- Test ---
    smer_label = st.radio("Varianta testu", ["Česky → anglicky", "Anglicky → česky"], key="aj_voc_smer")
    smer = "cz2en" if smer_label.startswith("Česky") else "en2cz"
    pocet = st.slider("Počet slovíček", min_value=1, max_value=30, value=10, key="aj_voc_pocet")

    if st.button("🎲 Vygenerovat", type="primary", key="aj_voc_gen"):
        tid = st.session_state.get("aj_voc_tid", 0) + 1
        st.session_state["aj_voc_tid"] = tid
        st.session_state["aj_voc_test"] = {
            "polozky": anglictina.slovicka_test_vygeneruj(sekce, smer, pocet),
            "tid": tid, "zkont": False, "smer": smer,
        }

    test = st.session_state.get("aj_voc_test")
    if not test:
        return
    tid = test["tid"]
    smer = test["smer"]
    napoveda = "napiš anglicky" if smer == "cz2en" else "napiš česky"
    st.write("---")
    zkont = test.get("zkont")

    for i, p in enumerate(test["polozky"]):
        moje = st.session_state.get(f"aj_voc_{tid}_{i}", "")
        barva = CERVENA if (zkont and not anglictina.voc_ok(moje, p["spravne"], smer)) else None
        velky_text(p["otazka"], "1.6rem", barva=barva)
        st.text_input(napoveda, key=f"aj_voc_{tid}_{i}", label_visibility="collapsed",
                      placeholder=napoveda)
        st.write("")

    if st.button("✅ Zkontrolovat", type="primary", key=f"aj_voc_check_{tid}"):
        test["zkont"] = True
        st.rerun()
    if not test.get("zkont"):
        return

    st.write("---")
    skore = 0
    chyby = []
    for i, p in enumerate(test["polozky"]):
        moje = st.session_state.get(f"aj_voc_{tid}_{i}", "")
        spravne_str = " / ".join(p["spravne"])
        if anglictina.voc_ok(moje, p["spravne"], smer):
            skore += 1
            st.markdown(f"✅ {p['otazka']}  →  **{spravne_str}**")
        else:
            st.markdown(f"❌ {p['otazka']}  →  tvoje: {moje or '—'} · správně: **{spravne_str}**")
            chyby.append((p["otazka"], moje or "—", spravne_str))

    pocet = len(test["polozky"])
    st.write("---")
    velky_text(f"Skóre: {skore} / {pocet}", "1.6rem")
    if skore == pocet:
        st.balloons()
        st.success("🎉 Všechno správně! Výborně!")
    st.write("---")
    whatsapp_odkazy("Sára", "Angličtina – slovíčka", skore, pocet, chyby)


def spust_anglictinu():
    oblast = st.selectbox(
        "Vyber oblast",
        ["Tázací slova (WH)", "Slovesa (to be / have got / can)",
         "There is / There are", "Slovíčka"],
        key="aj_oblast",
    )
    if oblast.startswith("Tázací"):
        _aj_dopln("wh", "tázací slova")
    elif oblast.startswith("Slovesa"):
        _aj_dopln("slovesa", "slovesa")
    elif oblast.startswith("There"):
        _aj_dopln("there", "there is / there are")
    else:
        _aj_slovicka()


# --- UI ---
st.sidebar.title("🎒 Škola hrou")
profil = st.sidebar.radio("Kdo cvičí?", ["Nela (1. třída)", "Sára (4. třída)"])

if profil.startswith("Nela"):
    st.title("👧 Nela — 1. třída")
    tab_mat, tab_cteni = st.tabs(["➕ Matematika", "📖 Čtení"])
    with tab_mat:
        spust_matematiku("Nela", matematika.NELA_MODULY)
    with tab_cteni:
        spust_cteni()
else:
    st.title("🌈 Sára — 4. třída")
    tab_mat, tab_cj, tab_aj = st.tabs(["🔢 Matematika", "✏️ Český jazyk", "🌍 Angličtina"])
    with tab_mat:
        spust_matematiku("Sára", matematika.SARA_MODULY)
    with tab_cj:
        spust_cestinu()
    with tab_aj:
        spust_anglictinu()
