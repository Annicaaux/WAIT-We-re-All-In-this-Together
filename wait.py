import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="StudyTogether", layout="wide")

# Farben und Schriftart global setzen
st.markdown("""
    <style>
        html, body, [class*="st"] {
            background-color: #fdfaf3;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: #2f2f2f;
        }
        .toggle-button {
            background: linear-gradient(135deg, #ffb6b9, #fcd5ce);
            color: #fff;
            font-weight: bold;
            padding: 0.8rem 1.2rem;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.15);
            width: 100%;
            text-align: left;
            font-size: 1.1rem;
            transition: all 0.2s ease-in-out;
        }
        .toggle-button:hover {
            background: linear-gradient(135deg, #e5989b, #f9dcc4);
        }
        .toggle-content {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin-top: 0.5rem;
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
            box-shadow: 4px 4px 10px rgba(0,0,0,0.15);
            transform: rotate(-2deg);
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📚 StudyTogether – Finde deine Lerngruppe")

# Tabs definieren
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Lerngruppen finden", "🛠️ Gruppe erstellen", "👥 Meine Gruppen", "📌 Pinnwand"])

# Farben definieren
farben = [
    ("#ffd6a5", "#ffb86f"),
    ("#b5ead7", "#70d6ff"),
    ("#caffbf", "#9bf6ff"),
    ("#ffc6ff", "#cdb4db"),
    ("#fdffb6", "#ffffa5")
]

# Session State
if "groups" not in st.session_state:
    st.session_state.groups = []
if "joined" not in st.session_state:
    st.session_state.joined = []

# Tab 1: Lerngruppen finden
with tab1:
    st.subheader("Offene Lerngruppen")
    for idx, group in enumerate(st.session_state.groups):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"**📖 {group['topic']}** – {group['time']} – {group['room']}")
        with col2:
            with st.expander("Anzeigen"):
                st.markdown(f"**Freie Plätze:** {group['max'] - len(group['members'])}")
                st.markdown(f"**Frage zum Einstieg:** _{group['question']}_")
                answer = st.text_input("Deine Antwort", key=f"answer_{idx}")
                color = farben[idx % len(farben)][0]
                if st.button("🚀 Beitreten", key=f"join_{idx}"):
                    if answer:
                        group['members'].append("Du")
                        group['answers']["Du"] = answer
                        st.session_state.joined.append(group['id'])
                        st.success("Du bist beigetreten!")
                    else:
                        st.warning("Bitte beantworte die Frage.")

# Tab 2: Gruppe erstellen
with tab2:
    with st.expander("➕ Neue Lerngruppe erstellen", expanded=True):
        topic = st.text_input("Thema")
        time = st.time_input("Uhrzeit", value=datetime.now().time())
        room = st.selectbox("Raum", ["Raum A1", "Bibliothek Gruppenraum", "Café Campus", "Lernwiese"])
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

# Tab 3: Meine Gruppen
with tab3:
    st.subheader("Deine Gruppen")
    for group in st.session_state.groups:
        if group['id'] in st.session_state.joined:
            with st.expander(f"🫱 {group['topic']} – {group['room']} – {group['time']}"):
                st.markdown("**Teilnehmer:innen:** " + ", ".join(group['members']))
                st.markdown("**Antworten:**")
                for name, ans in group['answers'].items():
                    st.markdown(f"- {name}: _{ans}_")

# Tab 4: Pinnwand
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

with tab4:
    st.subheader("Pinnwand")
    aktuelle = st.session_state.pinnwand[-1]
    letzte = st.session_state.pinnwand[-2]

    st.markdown(f"📅 **{aktuelle['question']}**")
    new = st.text_area("Deine Antwort", key="pin")
    if st.button("Absenden"):
        if new:
            aktuelle['entries'].append(new)
            st.success("Beitrag hinzugefügt!")

    st.markdown("### Beiträge der Woche")
    cols = st.columns(3)
    for i, text in enumerate(aktuelle['entries']):
        with cols[i % 3]:
            st.markdown(f"<div class='postit' style='background-color:#fff68f'>{text}</div>", unsafe_allow_html=True)

    st.markdown("### Letzte Woche")
    st.markdown(f"🕰️ **{letzte['question']}**")
    for i, text in enumerate(letzte['entries']):
        with cols[i % 3]:
            st.markdown(f"<div class='postit' style='background-color:#d0f4de'>{text}</div>", unsafe_allow_html=True)
