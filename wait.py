
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

# --- Custom CSS (vereinfacht für bessere Mobile-Darstellung) ---
st.markdown("""
<style>
    /* Basis-Styles */
    .stApp {
        background: linear-gradient(135deg, #A0616A 0%, #6B2C3A 100%);
    }
    
    /* Hauptcontainer mit max-width für Desktop */
    .main .block-container {
        max-width: 1200px;
        padding: 1rem;
    }
    
    /* Mobile-first approach */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialisierung ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.groups = []
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
