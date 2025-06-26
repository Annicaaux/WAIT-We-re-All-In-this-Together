import streamlit as st
from datetime import datetime
import random

# --- Seiten-Setup ---
st.set_page_config(page_title="WAITT", layout="wide")

# --- Titel der App ---
st.title("WAITT – we´re all in this together")

# --- Globales CSS Styling ---
st.markdown("""
    <style>
        html, body, [class*="st"] {
            background-color: #fdf6ee;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: #2f2f2f;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #3b3b3b;
        }

        .postit {
            font-family: 'Patrick Hand', 'Comic Sans MS', cursive;
        }
    </style>
""", unsafe_allow_html=True)

# ----- Session State Initialisierung -----
if "groups" not in st.session_state:
    st.session_state.groups = [
        {"id": 1, "topic": "Statistik Klausur", "time": "10:00", "room": "Raum A1", "max": 4, "members": ["Anna", "Ben"], "question": "Was ist deine größte Prokrastinationsgefahr?", "answers": {}},
        {"id": 2, "topic": "Klinische Psychologie", "time": "14:30", "room": "Bibliothek Gruppenraum 2", "max": 3, "members": ["Chris"], "question": "Was motiviert dich heute zu lernen?", "answers": {}},
        {"id": 3, "topic": "Biopsychologie", "time": "09:00", "room": "Café Campus", "max": 5, "members": [], "question": "Wenn dein Gehirn eine Farbe hätte – welche?", "answers": {}}
    ]

if "joined" not in st.session_state:
    st.session_state.joined = []

if "pinnwand" not in st.session_state:
    st.session_state.pinnwand = [
        {"week": "Letzte Woche", "question": "Was würde dein 13-jähriges Ich niemals von dir erwarten?", "entries": [
            "Dass ich freiwillig Steuern bezahle.",
            "Dass ich um 6:30 Uhr jogge und es mag.",
            "Dass ich Salat esse und dazu Wasser trinke.",
            "Dass ich mal 'Danke für die Therapiestunde' sage.",
            "Dass ich manchmal keine Ahnung hab – und das okay finde."
        ]},
        {"week": "Diese Woche", "question": "Was gibt dir gerade Energie beim Lernen?", "entries": []}
    ]

# ----- Tabs Setup -----
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Lerngruppen finden", "🛠️ Gruppe erstellen", "👥 Meine Gruppen", "📌 Pinnwand"])

# ----- Tab 1: Lerngruppen finden -----
with tab1:
    st.subheader("Offene Lerngruppen")
    color_styles = [
        "linear-gradient(135deg, #81d4fa, #4fc3f7)",
        "linear-gradient(135deg, #aed581, #9ccc65)",
        "linear-gradient(135deg, #ffcc80, #ffb74d)",
        "linear-gradient(135deg, #f48fb1, #ce93d8)",
        "linear-gradient(135deg, #b39ddb, #9575cd)"
    ]

    for idx, group in enumerate(st.session_state.groups):
        group_key = f"grp_{group['id']}"
        style = color_styles[idx % len(color_styles)]

        st.markdown(f"""
            <button class='toggle-button' style='background: {style};' onclick="var el = document.getElementById('{group_key}'); el.style.display = el.style.display === 'none' ? 'block' : 'none';">
                📖 {group['topic']} – {group['time']} – {group['room']}
            </button>
        """, unsafe_allow_html=True)

        st.markdown(f"<div id='{group_key}' style='display:none' class='toggle-content'>", unsafe_allow_html=True)
        st.markdown(f"**Freie Plätze:** {group['max'] - len(group['members'])}")
        st.markdown(f"**Frage zum Einstieg:** _{group['question']}_")
        answer = st.text_input(f"Deine Antwort ({group['id']})", key=f"answer_{group['id']}")

        if st.button("🚀 Beitreten", key=f"btn_{group['id']}"):
            if answer:
                if group['id'] not in st.session_state.joined:
                    group['members'].append("Du")
                    group['answers']['Du'] = answer
                    st.session_state.joined.append(group['id'])
                    st.success("Du bist der Gruppe beigetreten!")
                else:
                    st.info("Du bist bereits Mitglied dieser Gruppe.")
            else:
                st.warning("Bitte beantworte die Frage.")

        st.markdown("</div>", unsafe_allow_html=True)

# ----- Tab 2: Gruppe erstellen -----
with tab2:
    with st.expander("➕ Neue Lerngruppe erstellen", expanded=True):
        topic = st.text_input("Thema")
        time = st.time_input("Uhrzeit", value=datetime.now().time())
        room = st.selectbox("Raum", ["Raum A1", "A2", "Bibliothek Gruppenraum", "Café Campus", "Lernwiese"])
        max_p = st.slider("Maximale Teilnehmerzahl", 2, 10, 4)
        frage = st.text_input("Einstiegsfrage", placeholder="Was willst du von deiner Gruppe wissen?")

        if st.button("Gruppe erstellen"):
            if topic and frage:
                new_group = {
                    "id": random.randint(1000, 9999),
                    "topic": topic,
                    "time": time.strftime("%H:%M"),
                    "room": room,
                    "max": max_p,
                    "members": ["Du"],
                    "question": frage,
                    "answers": {"Du": "(noch keine Antwort)"}
                }
                st.session_state.groups.append(new_group)
                st.session_state.joined.append(new_group['id'])
                st.success("Gruppe erstellt und beigetreten!")
            else:
                st.warning("Bitte gib Thema und Frage an.")

# ----- Tab 3: Meine Gruppen -----
with tab3:
    st.subheader("Deine Gruppen")
    for group in st.session_state.groups:
        if group['id'] in st.session_state.joined:
            with st.expander(f"🫱 {group['topic']} – {group['room']} – {group['time']}"):
                st.markdown("**Teilnehmer:innen:** " + ", ".join(group['members']))
                st.markdown("**Einstiegsfrage & Antworten:**")
                for name, ans in group['answers'].items():
                    st.markdown(f"- {name}: _{ans}_")

# ----- Tab 4: Pinnwand -----
with tab4:
    aktuelle = st.session_state.pinnwand[-1]
    letzte = st.session_state.pinnwand[-2]

    st.subheader("Frage der Woche")
    st.markdown(f"📅 **{aktuelle['question']}**")
    new = st.text_area("Deine Antwort", key="pin")
    if st.button("Absenden"):
        if new:
            aktuelle['entries'].append(new)
            st.success("Danke für deinen Beitrag!")

    st.markdown("### Beiträge")
    cols = st.columns(3)
    for i, text in enumerate(aktuelle['entries']):
        with cols[i % 3]:
            st.markdown(f"<div class='postit'>{text}</div>", unsafe_allow_html=True)

    st.markdown("### Letzte Woche")
    st.markdown(f"🕰️ **{letzte['question']}**")
    for i, text in enumerate(letzte['entries']):
        with cols[i % 3]:
            st.markdown(f"<div class='postit postit-secondary'>{text}</div>", unsafe_allow_html=True)
