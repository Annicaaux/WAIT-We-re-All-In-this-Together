
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
    
    # 2-Minuten Countdown
    st.subheader("⏱️ Die 2-Minuten-Nichtstun-Challenge")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Nimm dir 2 Minuten nur für dich. Kein Handy, keine Ablenkung.")
    with col2:
        if st.button("▶️ Timer starten", key="start_timer"):
            st.session_state.countdown_active = True
            st.session_state.countdown_time = 120
    
    if st.session_state.countdown_active:
        placeholder = st.empty()
        
        while st.session_state.countdown_time > 0 and st.session_state.countdown_active:
            mins, secs = divmod(st.session_state.countdown_time, 60)
            placeholder.markdown(f"""
            <div class="custom-card" style="text-align: center; background: #FEF3C7;">
                <h1 style="font-size: 4rem; color: #92400E; margin: 0;">{mins:02d}:{secs:02d}</h1>
                <p style="color: #78350F;">Atme tief ein und aus... 🌸</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⏸️ Pause"):
                    st.session_state.countdown_active = False
            with col2:
                if st.button("⏹️ Stopp"):
                    st.session_state.countdown_active = False
                    st.session_state.countdown_time = 120
            with col3:
                if st.button("✅ Fertig"):
                    st.session_state.countdown_active = False
                    st.session_state.countdown_time = 0
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.pause_statistics["meditation_minuten"] += 2
                    st.session_state.reward_stamps += 1
                    st.success("Super! Du hast dir 2 Minuten gegönnt. +1 Stempel! 🌟")
                    st.balloons()
            
            pytime.sleep(1)
            st.session_state.countdown_time -= 1
            
            if st.session_state.countdown_time == 0:
                st.session_state.countdown_active = False
                placeholder.empty()
                st.success("🎉 Geschafft! Du hast 2 Minuten nur für dich genommen!")
                st.session_state.pause_statistics["solo_pausen"] += 1
                st.session_state.reward_stamps += 1
                st.balloons()
    
    st.markdown("---")
    
    # Aktivitäten
    if "Solo-Pause" in pause_type:
        st.subheader("🌊 Solo-Aktivitäten in Lübeck")
        
        activities = [
            {
                "name": "Wakenitz-Spaziergang",
                "duration": "15 Min",
                "location": "Wakenitz-Ufer",
                "description": "Entspanne am 'Amazonas des Nordens'",
                "stamps": 1
            },
            {
                "name": "Trave-Meditation", 
                "duration": "10 Min",
                "location": "Trave-Promenade",
                "description": "Beobachte die Schiffe und atme tief durch",
                "stamps": 1
            },
            {
                "name": "Mensa-Terrassen-Yoga",
                "duration": "5 Min", 
                "location": "Mensa Dachterrasse",
                "description": "Kurze Dehnübungen mit Aussicht",
                "stamps": 1
            }
        ]
        
        if st.button("🎲 Zufällige Aktivität", key="random_solo"):
            activity = random.choice(activities)
            st.session_state.current_solo_activity = activity
        
        if st.session_state.current_solo_activity:
            activity = st.session_state.current_solo_activity
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #059669;">
                <h4>📍 {activity['name']}</h4>
                <p><strong>Ort:</strong> {activity['location']} | <strong>Dauer:</strong> {activity['duration']}</p>
                <p>{activity['description']}</p>
                <p>⭐ Belohnung: +{activity['stamps']} Stempel</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ Pause gemacht!", key="done_solo"):
                st.session_state.pause_statistics["solo_pausen"] += 1
                st.session_state.reward_stamps += activity['stamps']
                st.success(f"Toll! +{activity['stamps']} Stempel für deine Pause! 🌟")
                st.session_state.current_solo_activity = None
                st.rerun()
    
    else:
        st.subheader("👥 Gruppen-Aktivitäten")
        
        if not st.session_state.joined_groups:
            st.warning("Tritt erst einer Gruppe bei, um Gruppenpausen zu planen!")
        else:
            st.info("Gruppenaktivitäten kommen bald!")
    
    # Belohnungssystem anzeigen
    if st.session_state.reward_stamps > 0:
        st.markdown("---")
        st.subheader("🏆 Deine Stempel")
        
        # Stempel visualisieren
        stamps_html = '<div style="display: flex; gap: 10px; flex-wrap: wrap;">'
        for i in range(10):
            if i < st.session_state.reward_stamps:
                stamps_html += '<div style="width: 40px; height: 40px; background: #10B981; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;">⭐</div>'
            else:
                stamps_html += '<div style="width: 40px; height: 40px; background: #E5E7EB; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #9CA3AF;">' + str(i+1) + '</div>'
        stamps_html += '</div>'
        
        st.markdown(stamps_html, unsafe_allow_html=True)
        st.progress(st.session_state.reward_stamps / 10)
        
        if st.session_state.reward_stamps >= 10:
            st.markdown("""
            <div class="custom-card" style="background: #10B981; color: white; text-align: center;">
                <h3>🎉 Belohnung freigeschaltet!</h3>
                <p>Zeige diese Seite in der Mensa für ein kostenloses Essen!</p>
                <p><strong>Mensa Uni Lübeck</strong><br>Mönkhofer Weg 241</p>
            </div>
            """, unsafe_allow_html=True)

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
