
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
        background: linear-gradient(135deg, #A0616A 0%, #6B2C3A 100%);
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
<h1 style="text-align: center; color: white; font-size: 3rem; margin-bottom: 0;">WAITT</h1>
<p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 2rem;">We're All In This Together - Uni Lübeck</p>
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
    <div class="custom-card" style="background: #E0F2FE; border-left: 4px solid #0284C7;">
        <p style="margin: 0; color: #075985;">
            <strong>Du bist nicht allein!</strong> Viele Studierende kämpfen mit dem Gefühl, 
            nie genug zu tun. Diese Pausen helfen dir, aus dem Hamsterrad auszusteigen 
            und wieder Freude am Studium zu finden. 💙
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
    
    # 2-Minuten Countdown (vereinfachte Version)
    st.subheader("⏱️ Die 2-Minuten-Nichtstun-Challenge")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Nimm dir 2 Minuten nur für dich. Kein Handy, keine Ablenkung, nur atmen.")
    with col2:
        if st.button("▶️ Start", key="timer_btn"):
            st.session_state.pause_statistics["meditation_minuten"] += 2
            st.session_state.pause_statistics["solo_pausen"] += 1
            st.session_state.reward_stamps += 1
            st.success("✅ Super! 2 Minuten Ruhe - das hast du dir verdient! +1 Stempel")
            st.balloons()
    
    st.info("💡 Tipp: Stelle dir einen Timer auf deinem Handy und lege es dann weg. Schaue aus dem Fenster oder schließe die Augen.")
    
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
                    "anleitung": "1. Timer auf 10 Min stellen\n2. Augen schließen\n3. An nichts denken\n4. Wenn Gedanken kommen: 'Später'\n5. Nach Timer: Strecken!",
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
                st.write(activity['anleitung'])
            
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
    st.header("🔍 Gruppen finden")
    
    # Zeige die Beispielgruppen
    for group in st.session_state.groups:
        with st.container():
            st.markdown(f"""
            <div class="custom-card">
                <h3>{group['icon']} {group['topic']}</h3>
                <p>🕐 {group['time']} | 📍 {group['room']}</p>
                <p>👥 {len(group['members'])}/{group['max']} Mitglieder</p>
                <p><strong>Einstiegsfrage:</strong> {group['question']}</p>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.header("➕ Gruppe erstellen")
    st.write("Hier kannst du eine neue Lerngruppe gründen.")

with tab4:
    st.header("👥 Meine Gruppen")
    if not st.session_state.joined_groups:
        st.info("Du bist noch in keiner Gruppe. Finde eine passende Gruppe oder gründe deine eigene!")

with tab5:
    st.header("📌 Community-Pinnwand")
    st.write(f"**Frage der Woche:** {st.session_state.current_question}")
