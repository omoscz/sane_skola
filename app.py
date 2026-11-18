import urllib.parse

import streamlit as st

import matematika
import cteni

st.set_page_config(page_title="Škola hrou", page_icon="🎒", layout="centered")


def velky_text(text, velikost="2rem"):
    st.markdown(
        f"<div style='font-size:{velikost};font-weight:600;margin:4px 0'>{text}</div>",
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

    for i, p in enumerate(test["polozky"]):
        if p["typ"] in ("cislo", "slovni"):
            if p["typ"] == "slovni":
                st.markdown(f"**{i + 1}.** {p['zadani']}")
            else:
                velky_text(f"{i + 1}.&nbsp;&nbsp;{p['zadani']}")
            st.number_input("odpověď", value=None, step=1, format="%d",
                            key=f"{profil}_odp_{tid}_{i}", label_visibility="collapsed")
        elif p["typ"] == "zbytek":
            velky_text(f"{i + 1}.&nbsp;&nbsp;{p['zadani']}")
            c1, c2 = st.columns(2)
            with c1:
                st.number_input("podíl", value=None, step=1, format="%d", key=f"{profil}_podil_{tid}_{i}")
            with c2:
                st.number_input("zbytek", value=None, step=1, format="%d", key=f"{profil}_zbytek_{tid}_{i}")
        elif p["typ"] == "porovnani":
            velky_text(f"{i + 1}.&nbsp;&nbsp;{p['a']} &nbsp;?&nbsp; {p['b']}", "2.4rem")
            st.radio("znaménko", ["<", "=", ">"], index=None, horizontal=True,
                     format_func=lambda z: {"<": "\\<", ">": "\\>"}.get(z, z),
                     key=f"{profil}_cmp_{tid}_{i}", label_visibility="collapsed")
        st.write("")

    if st.button("✅ Zkontrolovat", type="primary", key=f"{profil}_check_{tid}"):
        test["zkontrolovano"] = True

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
            st.markdown(f"✅ **{i + 1}.** {zadani}  →  {spravne_str}")
        else:
            st.markdown(f"❌ **{i + 1}.** {zadani}  →  tvoje: {moje_str} · správně: **{spravne_str}**")
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


def spust_cteni():
    st.caption("Rodič: zaškrtni písmena, která už Nela zná. Appka složí slabiky a slova jen z nich.")

    vybrane_samohlasky = []
    with st.expander("🔵 Samohlásky", expanded=True):
        cols = st.columns(7)
        for idx, p in enumerate(cteni.SAMOHLASKY):
            with cols[idx % 7]:
                if st.checkbox(p, key=f"cteni_sam_{p}"):
                    vybrane_samohlasky.append(p)

    vybrane_souhlasky = []
    with st.expander("🟢 Souhlásky", expanded=True):
        cols = st.columns(7)
        for idx, p in enumerate(cteni.SOUHLASKY):
            with cols[idx % 7]:
                if st.checkbox(p, key=f"cteni_souh_{p}"):
                    vybrane_souhlasky.append(p)

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
                        f"padding:14px;margin:6px 0;border-radius:12px;"
                        f"background:rgba(120,120,120,0.12)'>{slovo}</div>",
                        unsafe_allow_html=True,
                    )


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
    st.title("🧒 Sára — 4. třída")
    tab_mat, tab_cj = st.tabs(["🔢 Matematika", "✏️ Český jazyk"])
    with tab_mat:
        spust_matematiku("Sára", matematika.SARA_MODULY)
    with tab_cj:
        st.info("✏️ Český jazyk připravujeme (Fáze 3).")
