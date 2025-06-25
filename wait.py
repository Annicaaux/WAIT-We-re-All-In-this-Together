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
        .postit {
            padding: 1rem;
            margin: 0.5rem;
            border-radius: 6px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
            height: 120px;
            font-family: "Patrick Hand", "Comic Sans MS", cursive;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
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
if "pinnwand" not in st.session_state:
    st.session_state.pinnwand = [
        {"week": "Letzte Woche", "question": "Wie gehst du mit Lernblockaden um?", "entries": [
            "Ich tanze durch die Wohnung zu ABBA.",
            "Ich tu so, als erkläre ich's meinem Meerschweinchen.",
            "Blockaden ignoriere ich bis zur Panikattacke 🫠"
        ]},
        {"week": "Diese Woche", "question": "Was gibt dir gerade Energie beim Lernen?", "entries": []}
    ]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Lerngruppen finden", "Gruppe erstellen", "Meine Gruppen", "📌 Pinnwand"])

with tab1:
    st.subheader("Offene Lerngruppen")
    for group in st.session_state.groups:
        if not all(k in group for k in ("members", "max", "id", "topic", "time", "room", "question")):
            continue  # skip corrupted entries
        if len(group["members"]) >= group["max"]:
            continue
        if group["id"] in st.session_state.joined:
            continue
        with st.expander(f"📖 {group['topic']} – {group['time']} – {group['room']}"):
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

with tab2:
    st.subheader("Neue Lerngruppe erstellen")
    topic = st.text_input("Thema")
    time = st.time_input("Uhrzeit", value=datetime.now().time())
    room = st.selectbox("Raum", ["Raum A1", "A2", "Bibliothek Gruppenraum 1", "Café Campus", "Lernwiese", "Lounge"])
    max_p = st.slider("Maximale Teilnehmerzahl", 2, 10, 4)
    frage = st.text_input("Einstiegsfrage", placeholder="Was willst du von deiner Gruppe wissen?")
    if st.button("Gruppe erstellen"):
        if topic and frage:
            new_group = {"id": random.randint(1000, 9999), "topic": topic, "time": time.strftime("%H:%M"), "room": room,
                         "max": max_p, "members": ["Du"], "question": frage, "answers": {"Du": "(noch keine Antwort)"}}
            st.session_state.groups.append(new_group)
            st.session_state.joined.append(new_group['id'])
            st.success("Gruppe erstellt und beigetreten!")
        else:
            st.warning("Bitte gib Thema und Frage an.")

with tab3:
    st.subheader("Deine Gruppen")
    for group in st.session_state.groups:
        if not all(k in group for k in ("members", "id", "topic", "room", "time", "answers")):
            continue
        if group["id"] in st.session_state.joined:
            with st.expander(f"🫱 {group['topic']} – {group['room']} – {group['time']}"):
                st.markdown("**Teilnehmer:innen:** " + ", ".join(group['members']))
                st.markdown("**Einstiegsfrage & Antworten:**")
                for name, ans in group['answers'].items():
                    st.markdown(f"- {name}: _{ans}_")
                chat = st.text_input(f"Nachricht an Gruppe ({group['id']})", key=f"chat_{group['id']}")
                if chat:
                    st.markdown(f"**Du:** {chat}")

with tab4:
    st.subheader("Frage der Woche")
    aktuelle = st.session_state.pinnwand[-1]
    st.markdown(f"🗓️ **{aktuelle['question']}**")
    new = st.text_area("Deine Antwort", key="pin")
    if st.button("Absenden"):
        if new:
            aktuelle['entries'].append(new)
            st.success("Danke für deinen Beitrag!")

    st.markdown("### Beiträge")
    cols = st.columns(3)
    colors = ["#fff9b1", "#fff4a3", "#ffe7a8", "#fffbe0", "#ffefc2"]
    for i, text in enumerate(aktuelle['entries']):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class='postit' style='background-color:{random.choice(colors)}; transform: rotate({random.choice([-2,-1,0,1,2])}deg);'>
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Letzte Woche")
    letzte = st.session_state.pinnwand[-2]
    st.markdown(f"**🗓️ {letzte['question']}**")
    for i, text in enumerate(letzte['entries']):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class='postit' style='background-color:{random.choice(colors)}; transform: rotate({random.choice([-3,-2,-1,1,2,3])}deg);'>
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )
