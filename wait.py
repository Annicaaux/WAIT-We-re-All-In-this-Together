import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="StudyTogether", layout="wide")

# Global styles
st.markdown("""
    <style>
        html, body, [class*="st"] {
            background-color: #fdf6ee;
            font-family: 'Segoe UI', sans-serif;
            color: #333333;
        }
        .postit {
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Patrick Hand', 'Comic Sans MS', cursive;
            text-align: center;
            padding: 1rem;
            margin: 0.5rem;
            width: 160px;
            height: 160px;
            border: 1px solid #e0d97a;
            border-radius: 4px;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.1);
            transform: rotate(-1.5deg);
            font-size: 1.1rem;
            background-color: #fff68f;
        }
        .postit-secondary {
            background-color: #d0f4de;
        }
    </style>
""", unsafe_allow_html=True)

# Session State
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

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Lerngruppen finden", "➕ Gruppe erstellen", "👥 Meine Gruppen", "📌 Pinnwand"])

# Farben
color_styles = [
    "linear-gradient(135deg, #81d4fa, #4fc3f7)",
    "linear-gradient(135deg, #aed581, #9ccc65)",
    "linear-gradient(135deg, #ffcc80, #ffb74d)",
    "linear-gradient(135deg, #f48fb1, #ce93d8)",
    "linear-gradient(135deg, #b39ddb, #9575cd)"
]

# Tab 1: Gruppen anzeigen
with tab1:
    st.subheader("Offene Lerngruppen")
    for idx, group in enumerate(st.session_state.groups):
        color = color_styles[idx % len(color_styles)]
        container = st.container()
        with container:
            with st.expander(f"📖 {group['topic']} – {group['time']} – {group['room']}"):
                st.markdown(f"**Freie Plätze:** {group['max'] - len(group['members'])}")
                st.markdown(f"**Frage zum Einstieg:** _{group['question']}_")
                answer = st.text_input("Deine Antwort", key=f"answer_{idx}")
                if st.button("🚀 Beitreten", key=f"join_{idx}"):
                    if answer:
                        if group['id'] not in st.session_state.joined:
                            group['members'].append("Du")
                            group['answers']['Du'] = answer
                            st.session_state.joined.append(group['id'])
                            st.success("Du bist der Gruppe beigetreten!")
                        else:
                            st.info("Du bist bereits Mitglied.")
                    else:
                        st.warning("Bitte beantworte die Frage, bevor du beitrittst.")

# Tab 2: Gruppe erstellen
with tab2:
    with st.form("Gruppe erstellen"):
        topic = st.text_input("📘 Thema")
        time = st.time_input("🕒 Uhrzeit", value=datetime.now().time())
        room = st.selectbox("🏫 Raum", ["Raum A1", "A2", "Bibliothek Gruppenraum", "Café Campus", "Lernwiese"])
        max_p = st.slider("👥 Maximale Teilnehmerzahl", 2, 10, 4)
        frage = st.text_input("🗨️ Einstiegsfrage", placeholder="Was willst du von deiner Gruppe wissen?")
        submitted = st.form_submit_button("➕ Gruppe erstellen")
        if submitted:
            if topic and frage:
                new_id = random.randint(1000, 9999)
                new_group = {
                    "id": new_id,
                    "topic": topic,
                    "time": time.strftime("%H:%M"),
                    "room": room,
                    "max": max_p,
                    "members": ["Du"],
                    "question": frage,
                    "answers": {"Du": "(noch keine Antwort)"}
                }
                st.session_state.groups.append(new_group)
                st.session_state.joined.append(new_id)
                st.success("Gruppe erfolgreich erstellt und beigetreten!")
            else:
                st.warning("Bitte gib sowohl Thema als auch Frage ein.")

# Tab 3: Meine Gruppen
with tab3:
    st.subheader("Deine Gruppen")
    for group in st.session_state.groups:
        if group['id'] in st.session_state.joined:
            with st.expander(f"🫱 {group['topic']} – {group['room']} – {group['time']}"):
                st.markdown("**Teilnehmer:innen:** " + ", ".join(group['members']))
                st.markdown("**Antworten auf die Frage:**")
                for name, ans in group['answers'].items():
                    st.markdown(f"- {name}: _{ans}_")

# Tab 4: Pinnwand
with tab4:
    aktuelle = st.session_state.pinnwand[-1]
    letzte = st.session_state.pinnwand[-2]

    st.subheader(f"📅 Frage der Woche: {aktuelle['question']}")
    pin_input = st.text_area("✍️ Deine Antwort", key="pin")
    if st.button("Antwort absenden"):
        if pin_input:
            aktuelle['entries'].append(pin_input)
            st.success("Antwort hinzugefügt!")

    st.markdown("### 📌 Beiträge")
    cols = st.columns(3)
    for i, entry in enumerate(aktuelle['entries']):
        with cols[i % 3]:
            st.markdown(f"<div class='postit'>{entry}</div>", unsafe_allow_html=True)

    st.markdown(f"### ⏪ Letzte Woche: {letzte['question']}")
    for i, entry in enumerate(letzte['entries']):
        with cols[i % 3]:
            st.markdown(f"<div class='postit postit-secondary'>{entry}</div>", unsafe_allow_html=True)
