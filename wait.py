
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

# Test ob alles läuft
st.title("WAITT - We're All In This Together")
st.write("Uni Lübeck")

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
    st.header("Pausengestaltung")
    st.write("Hier kommen die Pausen-Features")

with tab2:
    st.header("Gruppen finden")
    st.write("Hier kommen die Gruppen")

with tab3:
    st.header("Gruppe erstellen")
    st.write("Hier kann man Gruppen erstellen")

with tab4:
    st.header("Meine Gruppen")
    st.write("Hier sieht man seine Gruppen")

with tab5:
    st.header("Community-Pinnwand")
    st.write("Hier ist die Pinnwand")
