import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="StudyTogether", layout="wide")

# Farben und Schriftart global setzen
st.markdown("""
    <style>
        html, body, [class*="st"] {
            background-color: #f5f0e6;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: #2f2f2f;
        }
        .toggle-btn {
            background: linear-gradient(135deg, #aed581, #9ccc65);
            color: #fff;
            font-weight: bold;
            padding: 0.7rem 1.4rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.15);
            transition: all 0.2s ease-in-out;
            width: 100%;
            text-align: left;
        }
        .toggle-btn:hover {
            background: linear-gradient(135deg, #9ccc65, #8bc34a);
        }
        .collapsible {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1rem;
            margin-top: 0.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.title("📚 StudyTogether – Finde deine Lerngruppe")

# Session State Init
if "groups" not in st.session_state:
    st.session_state.groups = [
        {"id": 1, "topic": "Statistik Klausur", "time": "10:00", "room": "Raum A1", "max": 4, "members": ["Anna", "Ben"], "question": "Was ist deine größte Prokrastinationsgefahr?", "answers": {}},
        {"id": 2, "topic": "Klinische Psychologie", "time": "14:30", "room": "Bibliothek Gruppenraum 2", "max": 3, "members": ["Chris"], "question": "Was motiviert dich heute zu lernen?", "answers": {}},
        {"id": 3, "topic": "Biopsychologie", "time": "09:00", "room": "Café Campus", "max": 5, "members": [], "question": "Wenn dein Gehirn eine Farbe hätte – welche?", "answers": {}}
    ]
if "joined" not in st.session_state:
    st.session_state.joined = []
if "show_create" not in st.session_state:
    st.session_state.show_create = False
if "expanded_groups" not in st.session_state:
    st.session_state.expanded_groups = set()

st.subheader("Offene Lerngruppen")

for group in st.session_state.groups:
    label = f"📖 {group['topic']} – {group['time']} – {group['room']}"
    if st.button(label, key=f"btn_{group['id']}", help="Klicke, um mehr zu sehen", use_container_width=True):
        if group['id'] in st.session_state.expanded_groups:
            st.session_state.expanded_groups.remove(group['id'])
        else:
            st.session_state.expanded_groups.add(group['id'])

    if group['id'] in st.session_state.expanded_groups:
        with st.container():
            st.markdown("<div class='collapsible'>", unsafe_allow_html=True)
            st.markdown(f"**Freie Plätze:** {group['max'] - len(group['members'])}")
            st.markdown(f"**Frage zum Einstieg:** _{group['question']}_")
            answer = st.text_input(f"Deine Antwort ({group['id']})", key=f"answer_{group['id']}")
            if st.button(f"Beitreten ({group['id']})"):
                if answer:
                    group['members'].append("Du")
                    group['answers']['Du'] = answer
                    st.session_state.joined.append(group['id'])
                    st.success("Du bist der Gruppe beigetreten!")
                else:
                    st.warning("Bitte beantworte die Frage, bevor du beitrittst.")
            st.markdown("</div>", unsafe_allow_html=True)

# Umschaltbarer Bereich für Gruppenerstellung
if st.button("➕ Neue Lerngruppe erstellen", key="create_toggle_btn", use_container_width=True):
    st.session_state.show_create = not st.session_state.show_create

if st.session_state.show_create:
    st.markdown("<div class='collapsible'>", unsafe_allow_html=True)
    topic = st.text_input("Thema")
    time = st.time_input("Uhrzeit", value=datetime.now().time())
    room = st.selectbox("Raum", ["Raum A1", "A2", "Bibliothek Gruppenraum 1", "Café Campus", "Lernwiese", "Lounge"])
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
    st.markdown("</div>", unsafe_allow_html=True)
