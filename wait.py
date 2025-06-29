
import streamlit as st
from datetime import datetime, time
import random
import uuid
import time as pytime

# --- Page Config ---
st.set_page_config(
    page_title="WAITT - Uni Lübeck",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Basis-Styles */
    .stApp {
        background: linear-gradient(135deg, #cd9b9b 0%, #bc8f8f 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Container-Anpassungen */
    .main .block-container {
        max-width: 1200px;
        padding: 1rem;
        margin: 0 auto;
    }
    
    /* Karten-Design */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        color: white;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Mobile Anpassungen */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .custom-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        /* Tabs mobil-freundlicher */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem;
            font-size: 0.8rem;
        }
    }
    
    /* Buttons mobil-optimiert */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #A0616A, #6B2C3A);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 25px;
        font-weight: 600;
        min-height: 44px; /* Touch-friendly */
    }
    
    /* Success/Warning/Info Messages */
    .stSuccess, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialisierung ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.groups = []
    st.session_state.groups = [
        {
            "id": "1",
            "topic": "Statistik Klausur - Gemeinsam schaffen",
            "time": "14:00",
            "room": "Bibliothek Gruppenraum 1",
            "max": 4,
            "members": ["Anna", "Ben"],
            "question": "Was ist deine größte Herausforderung beim Lernen?",
            "icon": "📊"
        },
        {
            "id": "2",
            "topic": "Anatomie Lerngruppe",
            "time": "16:00",
            "room": "Mensa Terrasse",
            "max": 6,
            "members": ["Lisa", "Tom", "Sarah"],
            "question": "Welche Lernmethode funktioniert bei dir am besten?",
            "icon": "🏥"
        }
    ]
    st.session_state.joined_groups = []
    st.session_state.pinnwand_entries = []
    st.session_state.pinnwand_entries = []  # Ändere das zu einer Liste mit Dictionaries für mehr Info
    st.session_state.pinnwand_archiv = {}  # NEU
    st.session_state.current_week = datetime.now().strftime("%Y-KW%U")  # NEU
    st.session_state.current_question = "Was hilft dir, beim Lernen nicht die Lebensfreude zu verlieren?"
    st.session_state.pause_statistics = {
        "solo_pausen": 0,
        "gruppen_pausen": 0,
        "total_time": 0,
        "trave_spaziergaenge": 0,
        "wakenitz_besuche": 0,
        "mensa_pausen": 0,
        "meditation_minuten": 0,
        "bewegung_minuten": 0
    }
    st.session_state.reward_stamps = 0
    st.session_state.reward_claimed = False
    st.session_state.countdown_active = False
    st.session_state.countdown_time = 120
    st.session_state.current_solo_activity = None
    st.session_state.current_group_activity = None

# --- Haupttitel ---
st.markdown("""
<h1 style="text-align: center; color: #8b3a3a; font-size: 3rem; margin-bottom: 0;">WAITT</h1>
<p style="text-align: center; color: #8b3a3a; font-size: 1.2rem; margin-bottom: 2rem;">We're All In This Together - Uni Lübeck</p>
""", unsafe_allow_html=True)

# --- Header mit Metriken ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{len(st.session_state.groups)}</p>
        <p class="metric-label">Aktive Gruppen</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_members = sum(len(group.get("members", [])) for group in st.session_state.groups)
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{total_members}</p>
        <p class="metric-label">Studierende</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_pauses = st.session_state.pause_statistics["solo_pausen"] + st.session_state.pause_statistics["gruppen_pausen"]
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{total_pauses}</p>
        <p class="metric-label">Pausen</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    stamps = st.session_state.reward_stamps
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{stamps}⭐</p>
        <p class="metric-label">Stempel</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌿 Pausengestaltung",
    "🔍 Gruppen finden", 
    "➕ Gruppe erstellen", 
    "👥 Meine Gruppen", 
    "📌 Community"
])

with tab1:
    st.header("🌿 Gesunde Pausen für Körper & Geist")
    
    st.markdown("""
    <div class="custom-card" style="background: #ffe4e1; border-left: 4px solid #0284C7;">
        <p style="margin: 0; color: #075985;">
            <strong>Du bist nicht allein!</strong> Viele Studierende kämpfen mit dem Gefühl, 
            nie genug zu tun. Doch oftmals sind Pausen gerade das, was am wichtigsten ist 
            und dennoch stets zukurz kommt. Doch egal was du heute geschafft hast, du hast 
            dir eine Pause verdient. Wer nur 10% hat und 10% gibt hat am Ende trotzdem 100%
            gegeben💙
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pausentyp wählen
    pause_type = st.radio(
        "Wie möchtest du deine Pause verbringen?",
        ["🧘 Solo-Pause (Zeit für mich)", "👥 Gruppen-Pause (Gemeinsam entspannen)"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # 2-Minuten Countdown (einfache Version)
    st.subheader("⏱️ Die 2-Minuten-Nichtstun-Challenge")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write("Nimm dir 2 Minuten nur für dich. Kein Handy, keine Ablenkung. Nur du und eine Gedanken (spooky)")
    with col2:
        # Externe Timer-Links
        st.link_button("⏰ Online Timer", "https://donothingfor2minutes.org")
    with col3:
        if st.button("✅ Fertig", key="timer_done"):
            st.session_state.pause_statistics["meditation_minuten"] += 2
            st.session_state.pause_statistics["solo_pausen"] += 1
            st.session_state.reward_stamps += 1
            st.success("✅ Super! 2 Minuten Ruhe - das hast du dir verdient! +1 Stempel")
            st.balloons()

    st.info("💡 Starte den Timer, lege dein Handy weg und konzentriere dich nur auf deine Atmung und Umgebung.")

    st.markdown("---")
    
    # Aktivitäten
    if "Solo-Pause" in pause_type:
        st.subheader("🌊 Solo-Aktivitäten")
        
        # Aktivitätskategorie wählen
        activity_cat = st.selectbox(
            "Was brauchst du gerade?",
            ["🏠 Vor Ort (Zimmer/Bibliothek)", "🚶 Bewegung (Rausgehen)", "🌿 Natur (Lübeck erkunden)"]
        )
        
        # Aktivitäten nach Kategorie
        activities = {
            "🏠 Vor Ort (Zimmer/Bibliothek)": [
                {
                    "name": "Schreibtisch-Yoga",
                    "duration": "3 Min",
                    "location": "Dein Arbeitsplatz",
                    "description": "Dehne Nacken, Schultern und Rücken direkt am Schreibtisch",
                    "anleitung": "1. Schultern kreisen (10x vor, 10x zurück)\n2. Kopf langsam von Seite zu Seite\n3. Arme über Kopf strecken\n4. Rücken durchstrecken",
                    "stamps": 1
                },
                {
                    "name": "Fenster-Meditation",
                    "duration": "5 Min",
                    "location": "Am Fenster",
                    "description": "Schaue aus dem Fenster und beobachte ohne zu bewerten",
                    "anleitung": "1. Fenster öffnen für frische Luft\n2. 5 Dinge die du siehst benennen\n3. 4 Geräusche wahrnehmen\n4. 3 tiefe Atemzüge\n5. Gedanken ziehen lassen wie Wolken",
                    "stamps": 1
                },
                {
                    "name": "Tee-Zeremonie",
                    "duration": "10 Min",
                    "location": "Küche/Pausenraum",
                    "description": "Bewusst Tee kochen und trinken - volle Achtsamkeit",
                    "anleitung": "1. Wasser bewusst aufkochen\n2. Tee mit Bedacht auswählen\n3. Während des Ziehens nur warten\n4. Ersten Schluck 30 Sek im Mund\n5. Wärme spüren",
                    "stamps": 1
                },
                {
                    "name": "Power-Nap",
                    "duration": "10 Min",
                    "location": "Ruhige Ecke",
                    "description": "Kurzer Powernap für neue Energie (Timer stellen!)",
                    "anleitung": "1. Timer auf 10 Min stellen\n2. Augen schließen\n3. An nichts denken\n4. Wenn Gedanken kommen: 'lass sie rein und wieder weiterziehen, wie die Wolken, werte sie nicht'\n5. Nach Timer: Strecken!",
                    "stamps": 1
                }
            ],
            "🚶 Bewegung (Rausgehen)": [
                {
                    "name": "Treppen-Workout",
                    "duration": "5 Min",
                    "location": "Treppenhaus",
                    "description": "Rauf und runter - Kreislauf aktivieren",
                    "anleitung": "1. 2x normal hoch und runter\n2. 1x zwei Stufen auf einmal\n3. 1x seitlich gehen\n4. Oben 10 Hampelmänner\n5. Unten dehnen",
                    "stamps": 1
                },
                {
                    "name": "Campus-Runde",
                    "duration": "10 Min",
                    "location": "Um den Campus",
                    "description": "Einmal ums Gebäude - frische Luft tanken",
                    "anleitung": "1. Zügig gehen (nicht schlendern)\n2. Bewusst atmen: 4 ein, 4 aus\n3. Himmel beobachten\n4. 3 schöne Details entdecken\n5. Lächeln!",
                    "stamps": 1
                },
                {
                    "name": "Mensa-Terrassen-Pause",
                    "duration": "10 Min",
                    "location": "Mensa Dachterrasse",
                    "description": "Frische Luft mit Aussicht über Lübeck",
                    "anleitung": "1. Zur Terrasse gehen\n2. Aussicht genießen\n3. 5 tiefe Atemzüge\n4. Arme weit ausbreiten\n5. Energie tanken",
                    "stamps": 1
                }
            ],
            "🌿 Natur (Lübeck erkunden)": [
                {
                    "name": "Wakenitz-Meditation",
                    "duration": "20 Min",
                    "location": "Wakenitz-Ufer (5 Min vom Campus)",
                    "description": "Entspannung am 'Amazonas des Nordens'",
                    "anleitung": "1. Zum Wakenitz-Ufer radeln/gehen\n2. Ruhigen Platz suchen\n3. Wasser beobachten\n4. Enten zählen\n5. Gedanken mit dem Wasser fließen lassen",
                    "stamps": 2
                },
                {
                    "name": "Trave-Spaziergang",
                    "duration": "15 Min",
                    "location": "Trave-Promenade",
                    "description": "Bewegung mit Blick auf die Altstadt",
                    "anleitung": "1. Zur Trave gehen\n2. Richtung Holstentor\n3. Schiffe beobachten\n4. 3 Fotos machen\n5. Auf Bank 2 Min sitzen",
                    "stamps": 2
                },
                {
                    "name": "Holstentor-Auszeit",
                    "duration": "15 Min",
                    "location": "Holstentor",
                    "description": "Geschichte trifft Gegenwart - Perspektivwechsel",
                    "anleitung": "1. Zum Holstentor (Rad/Bus)\n2. Details am Tor entdecken\n3. Touristen beobachten\n4. Selfie mit Tor\n5. Niederegger-Marzipan als Belohnung?",
                    "stamps": 2
                },
                {
                    "name": "Dom-Besuch",
                    "duration": "15 Min",
                    "location": "Lübecker Dom",
                    "description": "Ruhe in historischen Mauern finden",
                    "anleitung": "1. Zum Dom gehen\n2. Einmal durchgehen\n3. Kerze anzünden (optional)\n4. 5 Min still sitzen\n5. Akustik genießen",
                    "stamps": 2
                }
            ]
        }
        
        # Zufällige Aktivität aus gewählter Kategorie
        if st.button("🎲 Zufällige Aktivität", key="random_activity"):
            available_activities = activities.get(activity_cat, [])
            if available_activities:
                st.session_state.current_solo_activity = random.choice(available_activities)
        
        # Aktivität anzeigen
        if st.session_state.current_solo_activity:
            activity = st.session_state.current_solo_activity
            
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #059669;">
                <h4>📍 {activity['name']}</h4>
                <p><strong>Ort:</strong> {activity['location']} | <strong>Dauer:</strong> {activity['duration']}</p>
                <p style="font-style: italic;">{activity['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📝 Anleitung"):
                st.write(activity.get('anleitung', 'Keine Anleitung verfügbar'))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Pause gemacht!", key="done_activity", type="primary"):
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.reward_stamps += activity['stamps']
                    
                    # Spezifische Statistiken
                    if "Wakenitz" in activity['name']:
                        st.session_state.pause_statistics["wakenitz_besuche"] += 1
                    if "Trave" in activity['name']:
                        st.session_state.pause_statistics["trave_spaziergaenge"] += 1
                    if "Bewegung" in activity_cat:
                        st.session_state.pause_statistics["bewegung_minuten"] += int(activity['duration'].split()[0])
                    
                    st.success(f"Super! +{activity['stamps']} Stempel für deine Pause! 🌟")
                    st.session_state.current_solo_activity = None
                    st.balloons()
                    st.rerun()
            
            with col2:
                if st.button("🔄 Andere Aktivität", key="other_activity"):
                    st.session_state.current_solo_activity = None
                    st.session_state.current_solo_activity = None
                    st.rerun()
    
    else:
        st.subheader("👥 Gruppen-Aktivitäten")
        
        if not st.session_state.joined_groups:
            st.warning("Tritt erst einer Gruppe bei, um Gruppenpausen zu planen!")
            st.info("💡 Gemeinsame Pausen stärken den Zusammenhalt und machen mehr Spaß!")
        else:
            st.success("Gruppenaktivitäten kommen bald! Z.B. gemeinsame Spaziergänge, Spiele, Talk-Runden...")
    
    # Belohnungssystem
    if st.session_state.reward_stamps > 0:
        st.markdown("---")
        st.subheader("🏆 Deine Stempel-Sammlung")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            # Stempel visualisieren
            stamps_html = '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1rem;">'
            for i in range(10):
                if i < st.session_state.reward_stamps:
                    stamps_html += '<div style="width: 50px; height: 50px; background: #10B981; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">⭐</div>'
                else:
                    stamps_html += '<div style="width: 50px; height: 50px; background: #E5E7EB; border: 2px dashed #9CA3AF; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #9CA3AF;">' + str(i+1) + '</div>'
            stamps_html += '</div>'
            
            st.markdown(stamps_html, unsafe_allow_html=True)
            st.progress(st.session_state.reward_stamps / 10)
        
        with col2:
            st.metric("Stempel", f"{st.session_state.reward_stamps}/10")
        
        if st.session_state.reward_stamps >= 10:
            st.markdown("""
            <div class="custom-card" style="background: linear-gradient(135deg, #10B981, #059669); color: white; text-align: center;">
                <h2 style="margin: 0;">🎉 BELOHNUNG FREIGESCHALTET!</h2>
                <p style="font-size: 1.2rem; margin: 1rem 0;">Kostenloses Essen in der Mensa!</p>
                <p><strong>So geht's:</strong><br>
                1. Screenshot machen<br>
                2. In der Mensa zeigen<br>
                3. Gratis essen!</p>
                <p style="margin-top: 1rem;"><strong>📍 Mensa Uni Lübeck</strong><br>Mönkhofer Weg 241</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Belohnung eingelöst - Neu starten"):
                st.session_state.reward_stamps = 0
                st.success("Glückwunsch! Sammle wieder neue Stempel!")
                st.rerun()

with tab2:
    st.header("🔍 Lerngruppen finden & vernetzen")
    
    st.markdown("""
    <div class="custom-card" style="background: #FEE2E2; border-left: 4px solid #DC2626;">
        <p style="margin: 0; color: #991B1B;">
            <strong>Du fühlst dich allein mit dem Lernstress?</strong> 
            Hier findest du Menschen, die das gleiche durchmachen. 
            Gemeinsam ist man weniger einsam und erfolgreicher! ❤️
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Suche nach Thema", placeholder="z.B. Statistik, Anatomie...")
    with col2:
        only_free = st.checkbox("Nur freie Plätze", value=True)
    
    # Gruppen filtern
    filtered_groups = st.session_state.groups
    if search:
        filtered_groups = [g for g in filtered_groups if search.lower() in g['topic'].lower()]
    if only_free:
        filtered_groups = [g for g in filtered_groups if len(g['members']) < g['max']]
    
    # Gruppen anzeigen
    if not filtered_groups:
        st.info("Keine passenden Gruppen gefunden. Erstelle deine eigene!")
    else:
        for idx, group in enumerate(filtered_groups):
            free_spaces = group['max'] - len(group['members'])
            is_member = group['id'] in st.session_state.joined_groups
            
            # Gruppe anzeigen
            st.markdown(f"""
            <div class="custom-card" style="border-top: 4px solid #A0616A;">
                <h3>{group['icon']} {group['topic']}</h3>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0;">
                    <span style="background: #F3F4F6; padding: 0.5rem 1rem; border-radius: 20px;">
                        🕐 {group['time']}
                    </span>
                    <span style="background: #F3F4F6; padding: 0.5rem 1rem; border-radius: 20px;">
                        📍 {group['room']}
                    </span>
                    <span style="background: #F3F4F6; padding: 0.5rem 1rem; border-radius: 20px;">
                        👥 {len(group['members'])}/{group['max']}
                    </span>
                </div>
                <div style="background: #FDF2F8; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong style="color: #831843;">Einstiegsfrage:</strong><br>
                    <em>"{group['question']}"</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mitglieder anzeigen
            if group['members']:
                st.write("**Mitglieder:**", ", ".join(group['members']))
            
            # Beitritts-Interface
            if not is_member and free_spaces > 0:
                with st.form(f"join_form_{idx}"):
                    answer = st.text_area(
                        "Beantworte die Einstiegsfrage:",
                        placeholder="Deine ehrliche Antwort hilft der Gruppe, dich kennenzulernen...",
                        key=f"answer_{idx}"
                    )
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        submitted = st.form_submit_button("🚀 Gruppe beitreten", type="primary")
                    with col2:
                        st.write(f"**{free_spaces}** freie Plätze")
                    
                    if submitted:
                        if answer.strip():
                            # Zur Gruppe hinzufügen
                            group['members'].append("Du")
                            st.session_state.joined_groups.append(group['id'])
                            st.session_state.reward_stamps += 1
                            st.success("🎉 Willkommen in der Gruppe! +1 Stempel")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Bitte beantworte die Einstiegsfrage!")
            
            elif is_member:
                st.success("✅ Du bist Mitglied dieser Gruppe")
            else:
                st.warning("⚠️ Diese Gruppe ist voll")
            
            st.markdown("---")
           

with tab3:
    st.header("➕ Neue Lerngruppe gründen")
    
    st.markdown("""
    <div class="custom-card">
        <p style="text-align: center; color: #6B7280;">
            Keine passende Gruppe gefunden? Starte deine eigene und finde Gleichgesinnte!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("create_group"):
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("📚 Thema", placeholder="z.B. Statistik II - Gemeinsam schaffen")
            time_str = st.time_input("🕐 Treffzeit", value=time(14, 0))
            icon = st.selectbox("🎯 Icon", ["📊", "🧠", "⚕️", "💻", "🔬", "📚", "🎨"])
        
        with col2:
            room = st.selectbox("📍 Ort", [
                "Bibliothek Gruppenraum 1",
                "Bibliothek Gruppenraum 2",
                "Mensa Terrasse",
                "Wakenitz-Ufer",
                "Online (Discord/Zoom)",
                "Café Campus"
            ])
            max_members = st.slider("👥 Max. Teilnehmer", 2, 8, 4)
        
        question = st.text_area(
            "❓ Einstiegsfrage",
            placeholder="Eine Frage, die neue Mitglieder beantworten müssen...",
            help="Z.B. 'Was ist deine größte Herausforderung beim Lernen?'"
        )
        
        submitted = st.form_submit_button("🚀 Gruppe erstellen", type="primary")
        
        if submitted:
            if topic and question:
                new_group = {
                    "id": str(len(st.session_state.groups) + 1),
                    "topic": topic,
                    "time": time_str.strftime("%H:%M"),
                    "room": room,
                    "max": max_members,
                    "members": ["Du (Gründer:in)"],
                    "question": question,
                    "icon": icon
                }
                
                st.session_state.groups.append(new_group)
                st.session_state.joined_groups.append(new_group["id"])
                st.session_state.reward_stamps += 2
                
                st.success("🎉 Gruppe erfolgreich erstellt! +2 Stempel")
                st.balloons()
                st.rerun()
            else:
                st.error("Bitte fülle alle Felder aus!")

with tab4:
    st.header("👥 Meine Lerngruppen")
    
    # Filtere nur die Gruppen, in denen der User Mitglied ist
    my_groups = [g for g in st.session_state.groups if g['id'] in st.session_state.joined_groups]
    
    if not my_groups:
        # Keine Gruppen - Motivierende Nachricht
        st.markdown("""
        <div class="custom-card" style="text-align: center; padding: 3rem;">
            <h2 style="color: #6B7280;">Du bist noch in keiner Gruppe 😔</h2>
            <p style="color: #9CA3AF; font-size: 1.1rem; margin: 1rem 0;">
                Lerngruppen helfen nicht nur beim Studium - sie sind auch ein Schutz gegen Einsamkeit!
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 2rem;">
                <span style="background: #E0E7FF; color: #4338CA; padding: 0.5rem 1.5rem; border-radius: 25px; font-weight: 600;">
                    🤝 Gemeinsam stärker
                </span>
                <span style="background: #FEE2E2; color: #DC2626; padding: 0.5rem 1.5rem; border-radius: 25px; font-weight: 600;">
                    ❤️ Weniger allein
                </span>
                <span style="background: #D1FAE5; color: #059669; padding: 0.5rem 1.5rem; border-radius: 25px; font-weight: 600;">
                    🎯 Mehr Motivation
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Gruppe finden", type="primary", use_container_width=True):
                st.info("Wechsle zum Tab 'Gruppen finden'!")
        with col2:
            if st.button("➕ Gruppe gründen", type="secondary", use_container_width=True):
                st.info("Wechsle zum Tab 'Gruppe erstellen'!")
    
    else:
        # Übersicht
        st.markdown(f"""
        <div class="custom-card" style="background: linear-gradient(135deg, #EDE9FE, #DDD6FE); margin-bottom: 1rem;">
            <p style="margin: 0; color: #5B21B6; text-align: center; font-size: 1.1rem;">
                <strong>Du bist in {len(my_groups)} Gruppe{'n' if len(my_groups) > 1 else ''}!</strong> 
                Das sind etwa {sum(len(g['members']) for g in my_groups)} Studierende, die dich unterstützen. 💜
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gruppen anzeigen
        for idx, group in enumerate(my_groups):
            st.markdown(f"""
            <div class="custom-card" style="border-left: 5px solid #A0616A;">
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="font-size: 3rem;">{group['icon']}</div>
                    <div style="flex: 1;">
                        <h3 style="margin: 0; color: #1F2937;">{group['topic']}</h3>
                        <div style="display: flex; gap: 1rem; margin: 0.5rem 0; flex-wrap: wrap;">
                            <span style="color: #6B7280;">🕐 {group['time']}</span>
                            <span style="color: #6B7280;">📍 {group['room']}</span>
                            <span style="color: #6B7280;">👥 {len(group['members'])}/{group['max']}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabs für verschiedene Funktionen
            tab_a, tab_b, tab_c, tab_d = st.tabs(["👥 Mitglieder", "🌿 Gruppenpause", "💬 Chat", "⚙️ Aktionen"])
            
            with tab_a:
                # Mitglieder anzeigen
                st.write("**Gruppenmitglieder:**")
                member_cols = st.columns(4)
                for i, member in enumerate(group['members']):
                    with member_cols[i % 4]:
                        if member == "Du" or member == "Du (Gründer:in)":
                            st.markdown(f"""
                            <div style="background: #10B981; color: white; padding: 0.5rem; 
                                        border-radius: 20px; text-align: center; margin: 0.2rem;">
                                {member} ⭐
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background: #E5E7EB; color: #374151; padding: 0.5rem; 
                                        border-radius: 20px; text-align: center; margin: 0.2rem;">
                                {member}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Einladen
                if len(group['members']) < group['max']:
                    st.write("")
                    invite_text = f"Hey! Wir haben noch {group['max'] - len(group['members'])} Plätze frei in unserer {group['topic']}-Gruppe. Komm dazu! 🎓"
                    if st.button(f"📤 Einladungstext kopieren", key=f"invite_{idx}"):
                        st.code(invite_text, language=None)
                        st.info("Text markieren und kopieren!")
            
            with tab_b:
                # Gruppenpause planen
                st.write("**🌿 Gemeinsame Pause planen**")
                
                pause_activities = [
                    {
                        "name": "Wakenitz-Gruppenpicknick",
                        "duration": "45 Min",
                        "description": "Gemeinsam am Wasser entspannen",
                        "location": "Wakenitz-Wiesen"
                    },
                    {
                        "name": "Mensa-Kaffeepause",
                        "duration": "20 Min", 
                        "description": "Quatschen bei Kaffee & Snacks",
                        "location": "Mensa Café"
                    },
                    {
                        "name": "Altstadt-Spaziergang",
                        "duration": "30 Min",
                        "description": "Bewegung & frische Luft",
                        "location": "Holstentor Treffpunkt"
                    }
                ]
                
                if st.button("🎲 Pausenvorschlag", key=f"pause_{idx}"):
                    activity = random.choice(pause_activities)
                    st.session_state[f"group_pause_{idx}"] = activity
                
                if f"group_pause_{idx}" in st.session_state:
                    activity = st.session_state[f"group_pause_{idx}"]
                    st.markdown(f"""
                    <div style="background: #D1FAE5; padding: 1rem; border-radius: 10px;">
                        <h4 style="color: #065F46; margin: 0;">{activity['name']}</h4>
                        <p style="color: #047857; margin: 0.5rem 0;">{activity['description']}</p>
                        <p style="color: #059669; margin: 0;">📍 {activity['location']} | ⏱️ {activity['duration']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Pause gemacht!", key=f"pause_done_{idx}"):
                            st.session_state.pause_statistics["gruppen_pausen"] += 1
                            st.session_state.reward_stamps += 2
                            st.success("Super! Gruppenpause = doppelte Stempel! +2 ⭐")
                            del st.session_state[f"group_pause_{idx}"]
                            st.balloons()
                            st.rerun()
                    with col2:
                        if st.button("🔄 Andere Aktivität", key=f"pause_other_{idx}"):
                            del st.session_state[f"group_pause_{idx}"]
                            st.rerun()
            
            with tab_c:
                # Gruppen-Chat (vereinfacht)
                st.write("**💬 Gruppen-Nachrichten**")
                
                # Chat-Key für diese Gruppe
                chat_key = f"chat_{group['id']}"
                if chat_key not in st.session_state:
                    st.session_state[chat_key] = []
                
                # Nachricht senden
                with st.form(f"chat_form_{idx}"):
                    message = st.text_input("Nachricht:", placeholder="Schreibe etwas Nettes...")
                    if st.form_submit_button("📤 Senden"):
                        if message.strip():
                            st.session_state[chat_key].append({
                                "author": "Du",
                                "message": message.strip(),
                                "time": datetime.now().strftime("%H:%M")
                            })
                            st.rerun()
                
                # Nachrichten anzeigen
                if st.session_state[chat_key]:
                    for msg in st.session_state[chat_key][-5:]:  # Nur letzte 5
                        if msg["author"] == "Du":
                            st.markdown(f"""
                            <div style="background: #DBEAFE; padding: 0.5rem 1rem; border-radius: 15px; 
                                        margin: 0.5rem 0; margin-left: 20%;">
                                <strong>{msg["author"]}</strong> <small>{msg["time"]}</small><br>
                                {msg["message"]}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background: #F3F4F6; padding: 0.5rem 1rem; border-radius: 15px; 
                                        margin: 0.5rem 0; margin-right: 20%;">
                                <strong>{msg["author"]}</strong> <small>{msg["time"]}</small><br>
                                {msg["message"]}
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("Noch keine Nachrichten. Sei der/die Erste!")
            
            with tab_d:
                # Aktionen
                st.write("**⚙️ Gruppenaktionen**")
                
                # Nächstes Treffen
                next_meeting = st.date_input(
                    "📅 Nächstes Treffen:",
                    key=f"meeting_{idx}",
                    min_value=datetime.now().date()
                )
                
                # Gruppe verlassen
                st.write("")
                st.warning("⚠️ Gruppe verlassen?")
                if st.button("🚪 Gruppe verlassen", key=f"leave_{idx}"):
                    st.session_state[f"confirm_leave_{idx}"] = True
                
                if st.session_state.get(f"confirm_leave_{idx}", False):
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Ja, verlassen", key=f"confirm_{idx}"):
                            # Aus Gruppe entfernen
                            group['members'] = [m for m in group['members'] if m not in ["Du", "Du (Gründer:in)"]]
                            st.session_state.joined_groups.remove(group['id'])
                            st.info("Du hast die Gruppe verlassen.")
                            st.rerun()
                    with col2:
                        if st.button("❌ Abbrechen", key=f"cancel_{idx}"):
                            st.session_state[f"confirm_leave_{idx}"] = False
                            st.rerun()
            
            st.markdown("---")
        
        # Zusammenfassung
        st.markdown("### 📊 Deine Lerngruppen-Statistik")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Aktive Gruppen", len(my_groups))
        with col2:
            total_members = sum(len(g['members']) for g in my_groups)
            st.metric("Lernpartner:innen", total_members)
        with col3:
            st.metric("Gruppenpausen", st.session_state.pause_statistics["gruppen_pausen"])

with tab5:
    st.header("📌 Community-Pinnwand")
    
    # Pinnwand-Hintergrund
    st.markdown("""
    <style>
    .pinnwand {
        background: linear-gradient(135deg, #D2691E 0%, #A0522D 100%);
        border: 15px solid #8B4513;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.3);
        min-height: 400px;
        position: relative;
    }
    
    .postit {
        background: #FFEB3B;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        transform: rotate(-2deg);
        position: relative;
        font-family: 'Comic Sans MS', cursive;
        transition: all 0.3s ease;
    }
    
    .postit:hover {
        transform: rotate(0deg) scale(1.05);
        z-index: 10;
    }
    
    .postit-pink { background: #FF69B4; transform: rotate(2deg); }
    .postit-green { background: #90EE90; transform: rotate(-1deg); }
    .postit-blue { background: #87CEEB; transform: rotate(1deg); }
    .postit-orange { background: #FFB347; transform: rotate(-3deg); }
    
    .pin {
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 2rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialisiere Archiv wenn nicht vorhanden
    if "pinnwand_archiv" not in st.session_state:
        st.session_state.pinnwand_archiv = {}
    
    if "current_week" not in st.session_state:
        st.session_state.current_week = datetime.now().strftime("%Y-KW%U")
    
    # Aktuelle Frage anzeigen
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg, #FDF2F8, #FCE7F3); border: 3px solid #F9A8D4;">
        <h2 style="text-align: center; color: #831843; margin: 0;">
            🌟 Frage der Woche 🌟
        </h2>
        <h3 style="text-align: center; color: #BE185D; margin: 1rem 0;">
            "{st.session_state.current_question}"
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Archiv-Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.pinnwand_archiv:
            selected_week = st.selectbox(
                "📅 Woche anzeigen:",
                options=[st.session_state.current_week] + list(st.session_state.pinnwand_archiv.keys()),
                format_func=lambda x: "Aktuelle Woche" if x == st.session_state.current_week else x
            )
        else:
            selected_week = st.session_state.current_week
    
    # Neue Antwort hinzufügen (nur für aktuelle Woche)
    if selected_week == st.session_state.current_week:
        with st.form("neue_antwort"):
            antwort = st.text_area(
                "✍️ Deine Antwort:",
                placeholder="Teile deine Gedanken mit der Community...",
                max_chars=200
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                submitted = st.form_submit_button("📌 An Pinnwand heften", type="primary")
            with col2:
                anonym = st.checkbox("Anonym")
            
            if submitted and antwort.strip():
                entry = {
                    "text": antwort.strip(),
                    "author": "Anonym" if anonym else f"Student:in #{len(st.session_state.pinnwand_entries)+1}",
                    "timestamp": datetime.now().strftime("%d.%m. %H:%M")
                }
                st.session_state.pinnwand_entries.append(entry)
                st.session_state.reward_stamps += 1
                st.success("📌 Angepinnt! +1 Stempel")
                st.rerun()
    
    # Pinnwand anzeigen
    st.markdown('<div class="pinnwand">', unsafe_allow_html=True)
    
    # Einträge als Post-its
    if selected_week == st.session_state.current_week:
        entries = st.session_state.pinnwand_entries
    else:
        entries = st.session_state.pinnwand_archiv.get(selected_week, {}).get("entries", [])
    
    if entries:
        # Post-its in Reihen anordnen
        cols = st.columns(3)
        colors = ["postit", "postit-pink", "postit-green", "postit-blue", "postit-orange"]
        
        for idx, entry in enumerate(entries):
            with cols[idx % 3]:
                color = colors[idx % len(colors)]
                
                # Einfache Version für Streamlit
                st.markdown(f"""
                <div class="{color}" style="margin-bottom: 1rem;">
                    <div class="pin">📌</div>
                    <p style="margin: 0; color: #333; font-size: 0.9rem;">
                        "{entry.get('text', entry)}"
                    </p>
                    <p style="text-align: right; margin-top: 1rem; font-size: 0.8rem; color: #666;">
                        - {entry.get('author', 'Anonym')}<br>
                        <small>{entry.get('timestamp', '')}</small>
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🤔 Noch keine Einträge. Sei der/die Erste!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Admin-Bereich
    st.markdown("---")
    
    with st.expander("🔧 Admin-Bereich"):
        password = st.text_input("Passwort:", type="password")
        
        if password == "wearethepower":
            st.success("✅ Admin-Zugang gewährt")
            
            new_question = st.text_input(
                "Neue Frage der Woche:",
                value=st.session_state.current_question
            )
            
            if st.button("🔄 Frage ändern & Archivieren", type="primary"):
                if new_question.strip() and new_question != st.session_state.current_question:
                    # Aktuelle Einträge archivieren
                    if st.session_state.pinnwand_entries:
                        st.session_state.pinnwand_archiv[st.session_state.current_week] = {
                            "question": st.session_state.current_question,
                            "entries": st.session_state.pinnwand_entries.copy()
                        }
                    
                    # Neue Woche beginnen
                    st.session_state.current_question = new_question.strip()
                    st.session_state.pinnwand_entries = []
                    st.session_state.current_week = datetime.now().strftime("%Y-KW%U")
                    
                    st.success("✅ Neue Frage gesetzt! Alte Einträge wurden archiviert.")
                    st.rerun()
            
            # Archiv-Verwaltung
            if st.session_state.pinnwand_archiv:
                st.write("**📚 Archivierte Wochen:**")
                for week, data in st.session_state.pinnwand_archiv.items():
                    st.write(f"- {week}: '{data['question']}' ({len(data['entries'])} Einträge)")
        
        elif password and password != "wearethepower":
            st.error("❌ Falsches Passwort")
    
    # Motivations-Bereich
    st.markdown("---")
    st.subheader("💪 Motivation der Woche")
    
    motivations = [
        "Jeder Schritt zählt - auch der kleinste!",
        "Pausen machen dich produktiver, nicht fauler.",
        "Du bist genug, so wie du bist.",
        "Fehler sind Lernchancen in Verkleidung.",
        "Gemeinsam schaffen wir das!"
    ]
    
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg, #E0F2FE, #DBEAFE); text-align: center;">
        <h3 style="color: #0369A1; margin: 0;">✨ {random.choice(motivations)} ✨</h3>
    </div>
    """, unsafe_allow_html=True)
