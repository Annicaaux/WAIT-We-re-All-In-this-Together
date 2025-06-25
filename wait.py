import streamlit as st
from datetime import date

st.set_page_config(page_title="Campus Lerngruppen App", layout="centered")
st.title("🎓 Campus Lerngruppen App")

# Initial Session State
if "groups" not in st.session_state:
    st.session_state.groups = [
        {
            "id": 1,
            "thema": "Statistik 1",
            "beschreibung": "",
            "groesse": "3/5",
            "zeit": "25. Juni, 14:00 Uhr",
            "ort": "Seminarraum A",
            "datum": date.today(),
            "frage": "Was machst du am liebsten in der Lernpause?",
            "antworten": [
                "Kaffee holen und spazieren",
                "Meditation oder Musik hören",
                "Kurz TikTok checken"
            ]
        },
        {
            "id": 2,
            "thema": "Allgemeine Psychologie: Aufmerksamkeit",
            "beschreibung": "",
            "groesse": "2/3",
            "zeit": "26. Juni, 10:00 Uhr",
            "ort": "Bibliothek 1. OG",
            "datum": date.today(),
            "frage": "Wie motivierst du dich an anstrengenden Tagen?",
            "antworten": ["Ich belohne mich mit Serien", "Ich erinnere mich an meine Ziele"]
        },
        {
            "id": 3,
            "thema": "Biopsychologie Prüfungsvorbereitung",
            "beschreibung": "",
            "groesse": "1/4",
            "zeit": "27. Juni, 16:00 Uhr",
            "ort": "Hörsaal 3",
            "datum": date.today(),
            "frage": "Was ist dein Lern-Life-Hack?",
            "antworten": ["Pomodoro-Timer", "Mit Karteikarten abfragen"]
        }
    ]

if "submitted_weekly" not in st.session_state:
    st.session_state.submitted_weekly = [
        "Ich will mein Studium wirklich gut abschließen.",
        "Mein Ziel ist der Masterplatz – das treibt mich an.",
        "Ich lerne mit Freund:innen, das macht es leichter.",
        "Ich will beim nächsten Test besser abschneiden.",
        "Wenn ich heute lerne, kann ich mir morgen frei nehmen.",
        "Ich möchte mir selbst beweisen, dass ich das kann.",
        "Die Deadline rückt näher.",
        "Ich möchte nicht wieder alles auf den letzten Drücker machen."
    ]

# Sidebar-Navigation
tab = st.sidebar.selectbox("Navigation", ["Lerngruppe erstellen", "Lerngruppen finden", "Pinnwand"])

# 🛠️ Tab: Lerngruppe erstellen
if tab == "Lerngruppe erstellen":
    st.header("Neue Lerngruppe erstellen")
    thema = st.text_input("Thema")
    beschreibung = st.text_area("Beschreibung")
    groesse = st.text_input("Größe (z.B. 3/5)")
    ort = st.text_input("Ort")
    zeit = st.text_input("Zeit (z.B. 14:00 Uhr)")
    datum = st.date_input("Datum", value=date.today())
    if st.button("➕ Gruppe erstellen"):
        new_id = max(g["id"] for g in st.session_state.groups) + 1
        st.session_state.groups.append({
            "id": new_id,
            "thema": thema,
            "beschreibung": beschreibung,
            "groesse": groesse,
            "zeit": zeit,
            "ort": ort,
            "datum": datum,
            "frage": "Was ist dein bestes Lern-Life-Hack?",
            "antworten": []
        })
        st.success("✅ Lerngruppe erstellt!")

# 🔍 Tab: Lerngruppen finden
elif tab == "Lerngruppen finden":
    st.header("Offene Lerngruppen")
    for group in st.session_state.groups:
        with st.expander(f"{group['thema']} • {group['zeit']} • {group['ort']}"):
            st.write(f"**Beschreibung:** {group['beschreibung']}")
            st.write(f"**Frage:** {group['frage']}")
            if "joined" not in group:
                antw = st.text_input("Antwort eingeben:", key=f"ans_{group['id']}")
                if st.button("Beitreten", key=f"join_{group['id']}") and antw:
                    group["antworten"].append(antw)
                    group["joined"] = True
                    st.success("🚀 Beigetreten!")
            else:
                st.write("**Antworten anderer:**")
                for a in group["antworten"]:
                    st.write(f"- {a}")

# 🖼️ Tab: Pinnwand
else:
    st.header("Frage der Woche")
    st.write("**Was motiviert dich aktuell am meisten beim Lernen?**")
    antwort = st.text_area("Anonym antworten")
    if st.button("Antwort absenden"):
        if antwort.strip():
            st.session_state.submitted_weekly.insert(0, antwort.strip())
            st.success("Danke für deine Antwort!")
    st.markdown("---")
    st.subheader("Antworten anderer (Post‑Its)")
    cols = st.columns(3)
    for i, a in enumerate(st.session_state.submitted_weekly):
        with cols[i % 3]:
            st.markdown(f"> {a}")
