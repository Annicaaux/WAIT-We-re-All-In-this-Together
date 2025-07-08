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

# --- CSS-Block ---
st.markdown ("""
<style>
    /* Root Variables */
    :root {
        /* Hauptfarbpalette - 5 harmonische rote Pastelltöne basierend auf #880608 */
        --color-1: #F4E6E7;  /* Sehr helles Rosé */
        --color-2: #E8C1C5;  /* Sanftes Rosa */
        --color-3: #D89DA3;  /* Mittleres Rosa */
        --color-4: #C87882;  /* Kräftigeres Rosa */
        --color-5: #B85461;  /* Intensives Rosa (basierend auf #880608) */
        
        /* Gradients */
        --primary-gradient: linear-gradient(135deg, var(--color-1) 0%, var(--color-2) 100%);
        --secondary-gradient: linear-gradient(135deg, var(--color-2), var(--color-3));
        --card-bg: rgba(255, 255, 255, 0.95);
        --text-primary: #000000;
        --text-secondary: #333333;
        --accent-pink: var(--color-4);
        --accent-light: var(--color-5);
    }
    
    /* Global Styles */
    .stApp {
        background: var(--primary-gradient);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }

    /* Zentriertes Layout */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem 2rem;
    }    

    /* Streamlit Standard-Container überschreiben */
    .st-emotion-cache-1y4p8pa {
        max-width: 1200px;
        padding: 2rem 1rem;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Hauptinhalt zentrieren */
    .main {
        display: flex;
        justify-content: center;
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

    /* Tabs größer und präsenter */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.3) !important;
        padding: 0.5rem !important;
        border-radius: 15px !important;
        margin-bottom: 1.5rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.8rem 1.5rem !important;
        min-height: 50px !important;
        background: var(--color-5) !important;
        color: black !important;
        border-radius: 12px !important;
        margin: 0 0.2rem !important;
    }

    .stTabs [aria-selected="true"] {
        background: white !important;
        color: black !important;
        box-shadow: 0 4px 12px rgba(200, 159, 163, 0.3) !important;
    }

    /* Metriken kleiner */
    .metric-card {
        padding: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    .metric-value {
        font-size: 1.2rem !important;
    }

    .metric-label {
        font-size: 0.7rem !important;
    }
    
    /* Karten-Design */
    .custom-card {
        background: white !important;
        border-radius: 15px;
        padding: 1.5rem;
        color: black !important;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        color: white !important;
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
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem !important;
            padding: 0.6rem 0.8rem !important;
            min-height: 40px !important;
        }
        .main .block-container {
            max-width: 100%;
            padding: 0.5rem;
            margin: 0 auto;
        }
        
        .custom-card {
            padding: 1rem;
            background: white !important;
            color: black !important;
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
    
    /* Buttons */
    .stButton > button {
        background: var(--color-5) !important;
        color: black !important;
        border: 1px solid var(--color-4) !important;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(200, 159, 163, 0.2);
    }

    .stButton > button:hover {
        background: var(--color-2) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(200, 159, 163, 0.3);
    }
    
    /* Success/Warning/Info Messages */
    .stSuccess, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    .anleitung-box {
        background: white !important;
        color: black !important;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--color-4);
    }

    .anleitung-button {
        background: white !important;
        color: black !important;
        border: 2px solid var(--color-4) !important;
    }

    /* Pinnwand Styles (behält bunte Post-Its) */
    .pinnwand {
        background: var(--color-2) !important;
        border: 10px solid var(--color-4) !important;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        min-height: 400px;
        position: relative;
        margin: 1rem 0;
    }

    /* Post-Its pastelliger und richtig positioniert */
    .postit {
        background: #FFF8E1 !important; /* Pastellgelb */
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        transform: rotate(-2deg);
        position: relative;
        font-family: 'Comic Sans MS', cursive;
        transition: all 0.3s ease;
        border-radius: 8px;
        border: 1px solid #F0F0F0;
    }

    .postit-pink { 
        background: #FCE4EC !important; /* Pastellrosa */
        transform: rotate(2deg); 
    }

    .postit-green { 
        background: #E8F5E8 !important; /* Pastellgrün */
        transform: rotate(-1deg); 
    }

    .postit-blue { 
        background: #E3F2FD !important; /* Pastellblau */
        transform: rotate(1deg); 
    }

    .postit-orange { 
        background: #FFF3E0 !important; /* Pastellorange */
        transform: rotate(-3deg); 
    }
    
    .postit:hover {
        transform: rotate(0deg) scale(1.05);
        z-index: 10;
    }
    
    .pin {
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 2rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
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
    st.session_state.user_level = "Neuling"
    st.session_state.user_avatar = "🌚"
    st.session_state.reward_claimed = False
    st.session_state.countdown_active = False
    st.session_state.countdown_time = 120
    st.session_state.current_solo_activity = None
    st.session_state.current_group_activity = None
    st.session_state.conversation_history = []
    st.session_state.favorite_questions = []
    st.session_state.conversation_badges = {
        "icebreaker": False,
        "deep_diver": False,
        "empathy_master": False,
        "story_collector": False,
        "connection_builder": False
    }

def calculate_user_level():
    """Berechnet das lustige User-Level basierend auf Aktivitäten"""
    stats = st.session_state.pause_statistics
    stamps = st.session_state.reward_stamps
    
    # Level basierend auf verschiedenen Aktivitäten
    levels = []
    
    # Pausen-basierte Level
    if stats["solo_pausen"] >= 10:
        levels.append(("Pausen-Profi", "🛋️", "Du gönnst dir regelmäßig Auszeiten!"))
    elif stats["solo_pausen"] >= 5:
        levels.append(("Entspannungs-Entdecker", "😌", "Du lernst, dir Pausen zu gönnen!"))
    
    # Meditation/Nichtstun Level
    if stats["meditation_minuten"] >= 20:
        levels.append(("Achtsamkeits-Guru", "🧘", "Du bist ein Meister der Stille!"))
    elif stats["meditation_minuten"] >= 10:
        levels.append(("Zen-Schüler", "🕉️", "Du findest deine innere Ruhe!"))
    
    # Natur-Level
    if stats["wakenitz_besuche"] >= 5:
        levels.append(("Wakenitz-Wanderer", "🦆", "Die Natur ist dein zweites Zuhause!"))
    if stats["trave_spaziergaenge"] >= 3:
        levels.append(("Trave-Tourist", "⛵", "Du kennst jeden Winkel am Wasser!"))
    
    # Gruppen-Level
    if stats["gruppen_pausen"] >= 5:
        levels.append(("Social Butterfly", "🦋", "Gemeinsam macht alles mehr Spaß!"))
    elif len(st.session_state.joined_groups) >= 2:
        levels.append(("Gruppen-Liebhaber", "👥", "Du weißt: Zusammen ist man weniger allein!"))
    
    # Stempel-Level
    if stamps >= 10:
        levels.append(("Stempel-König", "👑", "Du hast das System gemeistert!"))
    elif stamps >= 5:
        levels.append(("Stempel-Sammler", "⭐", "Auf dem besten Weg zur Belohnung!"))
    
    # Bewegungs-Level
    if stats["bewegung_minuten"] >= 60:
        levels.append(("Bewegungs-Champion", "🏃", "Sitzen war gestern!"))
    elif stats["bewegung_minuten"] >= 30:
        levels.append(("Aktiv-Student", "🚶", "Du bringst Schwung ins Studium!"))
    
    # Standard-Level wenn nichts zutrifft
    if not levels:
        return "Neuling", "🌱", "Starte deine WAITT-Reise!"
    
    # Wähle das höchste erreichte Level
    return levels[-1]

# --- Helper Funktion für kleine Metriken ---
def show_mini_metrics():
    """Zeigt kleine Metriken am unteren Rand"""
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: rgba(255,255,255,0.05);">
            <p class="metric-value">{len(st.session_state.groups)}</p>
            <p class="metric-label">Gruppen</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_members = sum(len(group.get("members", [])) for group in st.session_state.groups)
        st.markdown(f"""
        <div class="metric-card" style="background: rgba(255,255,255,0.05);">
            <p class="metric-value">{total_members}</p>
            <p class="metric-label">Studierende</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_pauses = st.session_state.pause_statistics["solo_pausen"] + st.session_state.pause_statistics["gruppen_pausen"]
        st.markdown(f"""
        <div class="metric-card" style="background: rgba(255,255,255,0.05);">
            <p class="metric-value">{total_pauses}</p>
            <p class="metric-label">Pausen</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: rgba(255,255,255,0.05);">
            <p class="metric-value">{stamps}⭐</p>
            <p class="metric-label">Stempel</p>
    </div>
    """, unsafe_allow_html=True)

# --- Haupttitel mit Level ---
st.markdown('<h1 style="text-align: center; color: #8b0000; font-size: 5rem; margin-bottom: -1rem;">WAITT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8b0000; font-size: 1.8rem; margin-top: 0; margin-bottom: 1rem;">We\'re All In This Together</p>', unsafe_allow_html=True)

    
# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Pausenraum",
    "Gruppen finden", 
    "Gruppe erstellen", 
    "Meine Gruppen", 
    "Gemeinschaftsraum",
    "Gesprächsfetzen",
    "Zukunftsgedanken" 
])


with tab1:
    st.markdown(
        '<h1 style="color: #8b3a3a;">Gesunde Pausen für Körper & Geist</h1>',
        unsafe_allow_html=True
    )
   
    
    st.markdown("""
    <div class="custom-card" style="background: #ffe4e1; border-left: 4px solid #8b3a3a;">
        <p style="margin: 0; color: #8b3a3a;">
            <strong>Du bist nicht allein!</strong> Es ist völlig okay und sogar richtig wichtig beim 
            Lernen Pausen zu machen. Dein Gehirn braucht diese kleinen Auszeiten, 
            um das Gelernte zu verarbeiten und neue Energie zu tanken. Statt dich durchzubeißen, 
            helfen dir bewusste Pausen dabei, konzentrierter und entspannter weiterzumachen. 
            Gönn dir also ruhig mal eine Pause!
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
                    "anleitung": "1. Timer auf 10 Min stellen\n2. Augen schließen\n3. An nichts denken\n4. Wenn Gedanken kommen:'lass sie rein und wieder weiterziehen, wie die Wolken, werte sie nicht'\n5. Nach Timer: Strecken!",
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
        if st.button("Zufällige Aktivität", key="random_activity"):
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
            
            with st.expander("Anleitung"):
                st.markdown(f'<div class="anleitung-box">{activity.get("anleitung", "Keine Anleitung verfügbar")}</div>', unsafe_allow_html=True)
                st.markdown('<style>div.row-widget.stButton:nth-of-type(1) > button {background: #F5E6D3 !important; color: black !important;}</style>', unsafe_allow_html=True)
           
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Pause gemacht!", key="done_activity", type="primary"):
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.reward_stamps += activity['stamps']
                    
                    # Spezifische Statistiken
                    if "Wakenitz" in activity['name']:
                        st.session_state.pause_statistics["wakenitz_besuche"] += 1
                    if "Trave" in activity['name']:
                        st.session_state.pause_statistics["trave_spaziergaenge"] += 1
                    if "Bewegung" in activity_cat:
                        st.session_state.pause_statistics["bewegung_minuten"] += int(activity['duration'].split()[0])
                   
                    old_level = st.session_state.user_level
                    new_level, new_avatar, _ = calculate_user_level()
                    if new_level != old_level:
                        st.balloons()
                        st.success(f"Level Up! Du bist jetzt: {new_avatar} {new_level}!")
                    st.success(f"Super! +{activity['stamps']} Stempel für deine Pause!")
                    st.session_state.current_solo_activity = None
                    st.rerun()
            
            with col2:
                if st.button("Andere Aktivität", key="other_activity"):
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

    # 2-Minuten Countdown (einfache Version)
    st.subheader("Die 2-Minuten-Nichtstun-Challenge")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write("Nimm dir 2 Minuten nur für dich. Kein Handy, keine Ablenkung. Nur du und eine Gedanken (spooky)")
    with col2:
        # Externe Timer-Links
        st.link_button("Online Timer", "https://donothingfor2minutes.org")
    with col3:
        if st.button("Fertig", key="timer_done"):
            st.session_state.pause_statistics["meditation_minuten"] += 2
            st.session_state.pause_statistics["solo_pausen"] += 1
            st.session_state.reward_stamps += 1
            st.success("Super! 2 Minuten Ruhe - das hast du dir verdient! +1 Stempel")
            st.balloons()

    st.info("Starte den Timer, lege dein Handy weg und konzentriere dich nur auf deine Atmung und Umgebung.")

    st.markdown("---")
    
    # Belohnungssystem
    if st.session_state.reward_stamps > 0:
        st.markdown("---")
        st.subheader("Deine Stempel-Sammlung")
        
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
                <h2 style="margin: 0;">BELOHNUNG FREIGESCHALTET!</h2>
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
    st.markdown(
        '<h1 style="color: #8b3a3a;">Lerngruppen finden & vernetzen</h1>',
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <div class="custom-card" style="background: #FEE2E2; border-left: 4px solid #cd9b9b;">
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
        search = st.text_input("Suche nach Thema", placeholder="z.B. Statistik, Anatomie...")
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
                     <span style="background: #cd9b9b; padding: 0.5rem 1rem; border-radius: 20px;">
                        🕐 {group['time']}
                    </span>
                    <span style="background: #cd9b9b; padding: 0.5rem 1rem; border-radius: 20px;">
                        📍 {group['room']}
                    </span>
                    <span style="background: #cd9b9b; padding: 0.5rem 1rem; border-radius: 20px;">
                        👥 {len(group['members'])}/{group['max']}
                    </span>
                </div>
                <div style="background: #cd9b9b; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
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
                        submitted = st.form_submit_button("Gruppe beitreten", type="primary")
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
        
        submitted = st.form_submit_button("Gruppe erstellen", type="primary")
        
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
            <h2 style="color: #6B7280;">Du bist noch in keiner Gruppe</h2>
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
                Das sind etwa {sum(len(g['members']) for g in my_groups)} Studierende, die dich unterstützen. 
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
                    if st.button(f"Einladungstext kopieren", key=f"invite_{idx}"):
                        st.code(invite_text, language=None)
                        st.info("Text markieren und kopieren!")
            
            with tab_b:
                # Gruppenpause planen
                st.write("**Gemeinsame Pause planen**")
                
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
                
                if st.button("Pausenvorschlag", key=f"pause_{idx}"):
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
                        if st.button("Pause gemacht!", key=f"pause_done_{idx}"):
                            st.session_state.pause_statistics["gruppen_pausen"] += 1
                            st.session_state.reward_stamps += 2
                            st.success("Super! Gruppenpause = doppelte Stempel! +2 ⭐")
                            del st.session_state[f"group_pause_{idx}"]
                            st.balloons()
                            st.rerun()
                    with col2:
                        if st.button("Andere Aktivität", key=f"pause_other_{idx}"):
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
                    if st.form_submit_button("Senden"):
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
                st.write("**Gruppenaktionen**")
                
                # Nächstes Treffen
                next_meeting = st.date_input(
                    "📅 Nächstes Treffen:",
                    key=f"meeting_{idx}",
                    min_value=datetime.now().date()
                )
                
                # Gruppe verlassen
                st.write("")
                st.warning("⚠️ Gruppe verlassen?")
                if st.button("Gruppe verlassen", key=f"leave_{idx}"):
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
        st.markdown("### Deine Lerngruppen-Statistik")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Aktive Gruppen", len(my_groups))
        with col2:
            total_members = sum(len(g['members']) for g in my_groups)
            st.metric("Lernpartner:innen", total_members)
        with col3:
            st.metric("Gruppenpausen", st.session_state.pause_statistics["gruppen_pausen"])
        
        # Motivations-Tipps
        st.markdown("---")
        st.markdown("### 💡 Tipps für erfolgreiche Lerngruppen")
        
        tips = [
            "🕐 **Regelmäßige Treffen**: Feste Termine schaffen Verbindlichkeit",
            "🎯 **Klare Ziele**: Definiert, was ihr in jeder Session erreichen wollt",
            "⏰ **Pausen einplanen**: 50 Min lernen, 10 Min Pause - gemeinsam!",
            "🤝 **Alle einbeziehen**: Jeder hat Stärken - nutzt sie!",
            "🌿 **Gemeinsame Pausen**: Stärken den Zusammenhalt",
            "📱 **Erreichbar bleiben**: Tauscht Kontaktdaten aus"
        ]
        
        tip_cols = st.columns(2)
        for i, tip in enumerate(tips):
            with tip_cols[i % 2]:
                st.markdown(f"""
                <div style="background: #F3F4F6; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    {tip}
                </div>
                """, unsafe_allow_html=True)
    

with tab5:
    st.header("Gemeinschaftsraum")
    
    # Initialisiere Archiv wenn nicht vorhanden
    if "pinnwand_archiv" not in st.session_state:
        st.session_state.pinnwand_archiv = {}
    
    if "current_week" not in st.session_state:
        st.session_state.current_week = datetime.now().strftime("%Y-KW%U")
    
    # Aktuelle Frage anzeigen
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg, #FDF2F8, #FCE7F3); border: 3px solid #F9A8D4;">
        <h2 style="text-align: center; color: #831843; margin: 0;">
             Frage der Woche 
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
                "Woche anzeigen:",
                options=[st.session_state.current_week] + list(st.session_state.pinnwand_archiv.keys()),
                format_func=lambda x: "Aktuelle Woche" if x == st.session_state.current_week else x
            )
        else:
            selected_week = st.session_state.current_week
    
    # Neue Antwort hinzufügen (nur für aktuelle Woche)
    if selected_week == st.session_state.current_week:
        with st.form("neue_antwort"):
            antwort = st.text_area(
                "Deine Antwort:",
                placeholder="Teile deine Gedanken mit der Community...",
                max_chars=200
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                submitted = st.form_submit_button("An Pinnwand heften", type="primary")
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
                st.success("Angepinnt! +1 Stempel")
                st.rerun()
    # Pinnwand anzeigen
    st.markdown('<div class="pinnwand" style="margin-top: 1rem;">', unsafe_allow_html=True)

    # Einträge als Post-its
    if selected_week == st.session_state.current_week:
        entries = st.session_state.pinnwand_entries
    else:
        entries = st.session_state.pinnwand_archiv.get(selected_week, {}).get("entries", [])
   
    # Alternative: Card-Layout
    st.markdown("### 💭 Community-Gedanken")

    if entries:
        cols = st.columns(3)
        for idx, entry in enumerate(entries):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="background: var(--color-1); padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; transform: rotate({random.choice([-2, -1, 0, 1, 2])}deg);
                            box-shadow: 2px 2px 8px rgba(0,0,0,0.1); border: 2px solid var(--color-3);">
                    <p style="margin: 0; color: #333; font-style: italic;">
                        "{entry.get('text', entry)}"
                    </p>
                    <p style="text-align: right; margin-top: 0.5rem; font-size: 0.8rem; color: #666;">
                        - {entry.get('author', 'Anonym')}<br>
                        <small>{entry.get('timestamp', '')}</small>
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Noch keine Einträge. Sei der/die Erste!")

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
    st.subheader("Motivation der Woche")
    
    motivations = [
        "Jeder Schritt zählt - auch der kleinste!",
        "Pausen machen dich produktiver, nicht fauler.",
        "Du bist genug, so wie du bist.",
        "Fehler sind Lernchancen in Verkleidung.",
        "Gemeinsam schaffen wir das!"
    ]
    
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg, #E0F2FE, #DBEAFE); text-align: center;">
        <h3 style="color: #0369A1; margin: 0;"> {random.choice(motivations)} </h3>
    </div>
    """, unsafe_allow_html=True)

with tab6:
    st.header("Gesprächsfetzen")
    
    st.markdown("""
    <div class="custom-card" style="background: linear-gradient(135deg, #FEF3C7, #FED7AA); border-left: 4px solid #F59E0B;">
        <p style="margin: 0; color: #92400E;">
            <strong>Echte Verbindungen entstehen durch echte Gespräche.</strong> 
            Hier findest du wissenschaftlich fundierte Fragen und Techniken, um aus Small Talk 
            bedeutsame Verbindungen zu machen. Basierend auf Forschung zu sozialer Verbundenheit 
            und interpersoneller Nähe.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gesprächskategorien
    categories = {
        "Eisbrecher": {
            "description": "Leichte Einstiegsfragen für den ersten Kontakt",
            "color": "#d89da3",
            "level": "Anfänger",
            "questions": [
                "Was war das Highlight deiner letzten Woche?",
                "Wenn du einen Tag lang eine Superkraft hättest, welche wäre es?",
                "Was ist deine aktuelle Lieblings-Playlist oder Podcast?",
                "Welche kleine Sache hat dich heute zum Lächeln gebracht?",
                "Was ist dein Go-to Comfort Food?",
                "Wenn du jetzt spontan verreisen könntest, wohin würdest du gehen?",
                "Was ist eine Fähigkeit, die du gerne hättest?",
                "Welches Buch/Film/Serie hat dich zuletzt begeistert?"
            ]
        },
        "Tiefgang": {
            "description": "Fragen für bedeutsamere Verbindungen (36 Fragen Prinzip)",
            "color": "#d89da3",
            "level": "Ein Schritt weiter",
            "questions": [
                "Was bedeutet Heimat für dich?",
                "Wann hast du dich das letzte Mal richtig lebendig gefühlt?",
                "Was würdest du ändern, wenn du wüsstest, niemand würde dich verurteilen?",
                "Welche Lektion hat das Leben dir auf die harte Tour beigebracht?",
                "Was ist eine Überzeugung, die du früher hattest und jetzt nicht mehr?",
                "Wofür bist du in deinem Leben am dankbarsten?",
                "Was macht dich verletzlich?",
                "Wenn du mit einer Person aus der Vergangenheit sprechen könntest, wer wäre es?"
            ]
        },
        "Philosophisch": {
            "description": "Zum gemeinsamen Nachdenken und Philosophieren",
            "color": "#d89da3",
            "level": "Nachdenklich",
            "questions": [
                "Glaubst du, dass alles aus einem Grund passiert?",
                "Was macht ein erfülltes Leben für dich aus?",
                "Wie definierst du Erfolg für dich persönlich?",
                "Was denkst du, ist der Sinn von Kunst?",
                "Glaubst du an Schicksal oder freien Willen?",
                "Was macht einen Menschen zu einem guten Menschen?",
                "Wie wichtig ist dir Authentizität?",
                "Was bedeutet Freiheit für dich?"
            ]
        },
        "Klassenclown": {
            "description": "Lustige hypothetische Szenarien",
            "color": "#d89da3",
            "level": "Scherzkeks",
            "questions": [
                "Du kannst drei fiktive Charaktere zum Dinner einladen - wen wählst du?",
                "Welche drei Gegenstände würdest du auf eine einsame Insel mitnehmen?",
                "Wenn dein Leben ein Film wäre, welches Genre wäre es?",
                "Du kannst eine Regel für die ganze Welt aufstellen - welche?",
                "Welches Tier repräsentiert deine Persönlichkeit am besten?",
                "Wenn du eine Zeitmaschine hättest - Vergangenheit oder Zukunft?",
                "Du gewinnst 10 Millionen, musst aber alles in 24h ausgeben - was kaufst du?",
                "Welche übernatürliche Kreatur wärst du gerne?"
            ]
        },
        "Deep-Dive-Buddy": {
            "description": "Fragen die Nähe und Verständnis fördern",
            "color": "##d89da3",
            "level": "Soulmates",
            "questions": [
                "Was ist eine Eigenschaft an dir, die andere oft übersehen?",
                "Wobei fühlst du dich am meisten wie du selbst?",
                "Was war ein Moment, in dem du dich wirklich verstanden gefühlt hast?",
                "Welche Ängste teilst du ungern mit anderen?",
                "Was brauchst du, wenn es dir nicht gut geht?",
                "Welche Art von Unterstützung schätzt du am meisten?",
                "Was ist etwas, wofür du dir selbst vergeben musstest?",
                "Wie zeigst du Menschen, dass sie dir wichtig sind?"
            ]
        }
    }
    
    # Wissenschaftlicher Hintergrund (collapsed)
    with st.expander("FunFacts"):
        st.markdown("""
        **Eine Prise Wissen:**
        
        🧠 **36 Fragen Studie (Aron et al., 1997)**
        - Fremde können durch strukturierte, zunehmend persönliche Fragen Intimität aufbauen
        - Gegenseitige Verletzlichkeit schafft Verbindung
        
        🤝 **Social Penetration Theory**
        - Beziehungen entwickeln sich von oberflächlich zu tief
        - Schrittweise Selbstoffenbarung ist der Schlüssel
        
        ⚡ **Peak-End Rule**
        - Wir erinnern uns an den emotionalen Höhepunkt und das Ende eines Gesprächs
        - Ein positiver Abschluss ist wichtig!
        """)
    
    # Hauptinterface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_category = st.selectbox(
            "Wähle eine Gesprächskategorie:",
            options=list(categories.keys()),
            format_func=lambda x: f"{x} - {categories[x]['level']}"
        )
    
    with col2:
        st.markdown(f"""
        <div style="background: {categories[selected_category]['color']}; 
                    padding: 1rem; border-radius: 10px; text-align: center;">
            <strong>{categories[selected_category]['level']}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"💡 {categories[selected_category]['description']}")
    
    # Zufällige Frage Generator
    st.markdown("### Deine Gesprächsfrage")
    
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    
    questions = categories[selected_category]['questions']
    current_question = questions[st.session_state.current_question_index % len(questions)]
    
    # Frage anzeigen
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg, #F0F9FF, #E0F2FE); 
                                    border: 2px solid #0EA5E9; text-align: center; padding: 2rem;">
        <h2 style="color: #0C4A6E; margin: 0; font-size: 1.5rem;">
            "{current_question}"
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Button-Zeile mit besserer Zentrierung
    st.markdown("<div style='margin: 1rem 0;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Vorherige", key="prev_q", use_container_width=True):
            st.session_state.current_question_index -= 1
            st.rerun()
    
    with col2:
        if st.button("Zufällige Frage", key="random_q", type="primary", use_container_width=True):
            st.session_state.current_question_index = random.randint(0, len(questions)-1)
            st.rerun()
    
    with col3:
        if st.button("Nächste", key="next_q", use_container_width=True):
            st.session_state.current_question_index += 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Favoriten speichern
    if st.button("Zu Favoriten hinzufügen", key="fav_q"):
        if current_question not in st.session_state.favorite_questions:
            st.session_state.favorite_questions.append(current_question)
            st.success("Zur Favoritenliste hinzugefügt!")
    
    # Gesprächstipps - Mobile-optimiert
    st.markdown("---")
    st.markdown("### Gesprächstipps")
    
    tips = [
        ("👂 Aktives Zuhören", "Zeige echtes Interesse durch Nachfragen und Körpersprache"),
        ("🤝 Reziprozität", "Teile auch etwas von dir - Gespräche sind keine Interviews"),
        ("🌟 Authentizität", "Sei du selbst - echte Verbindungen brauchen Ehrlichkeit"),
        ("🚫 Kein Druck", "Respektiere Grenzen - niemand muss alles teilen")
    ]
    
    # Mobile-freundliche Darstellung
    for idx in range(0, len(tips), 2):
        cols = st.columns(2)
        for col_idx, col in enumerate(cols):
            if idx + col_idx < len(tips):
                title, desc = tips[idx + col_idx]
                with col:
                    st.markdown(f"""
                    <div class="custom-card" style="min-height: 120px; margin-bottom: 1rem;">
                        <h4 style="margin: 0; color: var(--color-5); text-align: center;">{title}</h4>
                        <p style="font-size: 0.85rem; margin-top: 0.5rem; text-align: center;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Gesprächs-Challenges
    st.markdown("---")
    st.markdown("### 🏆 Wochen-Challenges")
    
    challenges = [
        {
            "name": "Small Talk Transformer",
            "task": "Verwandle diese Woche 3 Small Talks in meaningful Gespräche",
            "reward": "🏅 +3 Stempel",
            "stamps": 3
        },
        {
            "name": "Vulnerability Champion",
            "task": "Teile etwas Persönliches mit jemandem (wenn es sich richtig anfühlt)",
            "reward": "💎 +2 Stempel",
            "stamps": 2
        },
        {
            "name": "Curiosity Cat",
            "task": "Stelle 5 verschiedenen Menschen eine 'Tiefgang'-Frage",
            "reward": "🌟 +4 Stempel",
            "stamps": 4
        }
    ]
    
    for challenge in challenges:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div class="custom-card" style="margin-bottom: 0.5rem;">
                <strong>{challenge['name']}</strong><br>
                {challenge['task']}<br>
                <small style="color: var(--color-4);">{challenge['reward']}</small>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Geschafft!", key=f"challenge_{challenge['name']}", use_container_width=True):
                st.session_state.reward_stamps += challenge['stamps']
                st.success(f"Wow! {challenge['reward']}")
                st.balloons()
    
    # Favoriten anzeigen
    if st.session_state.favorite_questions:
        st.markdown("---")
        st.markdown("### ⭐ Deine Lieblingsfragen")
        
        for q in st.session_state.favorite_questions[-5:]:  # Zeige letzte 5
            st.markdown(f"""
            <div class="custom-card" style="background: #FFFBEB; border-left: 3px solid #F59E0B;">
                <p style="margin: 0; font-style: italic;">"{q}"</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Reflexions-Tagebuch
    st.markdown("---")
    st.markdown("### 📝 Reflexions-Ecke")
    st.markdown("*Welches Gespräch hat dich heute berührt? Was hast du über dich oder andere gelernt?*")
    
    with st.form("reflection_form"):
        reflection = st.text_area(
            "Deine Gedanken:",
            placeholder="Heute habe ich gelernt, dass...",
            max_chars=500
        )
        
        submitted = st.form_submit_button("Speichern", type="primary", use_container_width=True)
        
        if submitted:
            if reflection.strip():
                st.session_state.conversation_history.append({
                    "date": datetime.now().strftime("%d.%m.%Y"),
                    "text": reflection.strip()
                })
                st.session_state.reward_stamps += 1
                st.success("Danke fürs Teilen! +1 Stempel für deine Reflexion")
                
                # Badge Check
                if len(st.session_state.conversation_history) >= 5:
                    st.session_state.conversation_badges["story_collector"] = True
                    st.balloons()
                    st.success("🏆 Badge freigeschaltet: Story Collector!")

# Tab 7 mit eigenem Video und Spotify-Song-Button - KORRIGIERT
with tab7:
    st.header("Zukunftsgedanken")
    
    st.markdown("""
    <div class="custom-card" style="background: linear-gradient(135deg, #E0F2FE, #BAE6FD); border-left: 4px solid #0EA5E9;">
        <p style="margin: 0; color: #0C4A6E;">
            <strong>Das wars erstmal, passt auf euch auf</strong> 
            Und vergiss nicht: egal wie alleine du dich fühlst, 
            es gibt jemanden, der für dich da ist. Es gibt immer eine Lösung. We ARE all in this together
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # SPOTIFY SONG SECTION
    st.markdown("---")
    st.markdown("### Abschiedslied")
    
    # Song-Informationen - NUR die ID, ohne ?si=...
    song_info = {
        "title": "Welches Lied hat eure letzte Woche am meisten geprägt?", 
        "artist": "uns allen",
        "spotify_id": "062JO6PmxDjuL3MfYZtA2h",  # KORRIGIERT: Nur die ID
        "message": "Let´s start connecting with a shared Playlist"
    }

    # Song-Card
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg, #1DB954, #1ED760); color: white; text-align: center; padding: 2rem;">
        <h2 style="color: black; margin: 0;">🎶 {song_info['title']}</h2>
        <p style="color: black; margin: 0.5rem 0; font-size: 1.2rem;">von {song_info['artist']}</p>
        <p style="color: black; margin: 1rem 0; font-style: italic;">"{song_info['message']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Spotify-Button zentriert
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Spotify Song URL - KORRIGIERT
        spotify_song_url = f"https://open.spotify.com/playlist/062JO6PmxDjuL3MfYZtA2h?si=6418baa8c6884994&pt=1f8b6894e436577897f00501a6627672/{song_info['spotify_id']}"
        
        # Großer Spotify-Button mit HTML/CSS - KORRIGIERT
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="{spotify_song_url}" target="_blank" style="text-decoration: none;">
                <button style="
                    background-color: #1DB954;
                    color: white;
                    border: none;
                    padding: 1rem 2.5rem;
                    font-size: 1.2rem;
                    font-weight: bold;
                    border-radius: 50px;
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.8rem;
                    box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
                    transition: all 0.3s ease;
                    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                "
                onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(29, 185, 84, 0.4)';"
                onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(29, 185, 84, 0.3)';">
                    <svg style="width: 24px; height: 24px;" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                    </svg>
                    Auf Spotify anhören
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    

# --- Level-System am Ende der Seite ---

st.markdown("---")
st.markdown("## Dein WAITT-Level")

level_name, avatar, description = calculate_user_level()
st.session_state.user_level = level_name
st.session_state.user_avatar = avatar

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #E8C1C5, #D89DA3); 
         border-radius: 25px; 
         padding: 2rem; 
         text-align: center; 
         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
         border: 2px solid #D89DA3;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{avatar}</div>
        <h2 style="color: #8b0000; margin: 0.5rem 0;">{level_name}</h2>
        <p style="color: #8b0000; margin: 1rem 0; font-size: 1.1rem;">{description}</p>
     </div>
     """, unsafe_allow_html=True)

    st.markdown (f"""
    <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap;">
        <span style="background: white; padding: 0.5rem 1rem; border-radius: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            🏆 {st.session_state.reward_stamps} Stempel
        </span>
        <span style="background: white; padding: 0.5rem 1rem; border-radius: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            🧘 {st.session_state.pause_statistics["solo_pausen"]} Pausen
        </span>
        <span style="background: white; padding: 0.5rem 1rem; border-radius: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            👥 {len(st.session_state.joined_groups)} Gruppen
        </span>
     </div>
     """, unsafe_allow_html=True)

# Fortschritts-Hinweise
st.markdown("### Nächste Level-Ziele:")

next_goals = []
stats = st.session_state.pause_statistics

if stats["solo_pausen"] < 5:
    next_goals.append(f"Noch {5 - stats['solo_pausen']} Solo-Pausen bis zum 'Entspannungs-Entdecker'")
if stats["meditation_minuten"] < 10:
    next_goals.append(f"Noch {10 - stats['meditation_minuten']} Minuten meditieren bis zum 'Zen-Schüler'")
if len(st.session_state.joined_groups) < 2:
    next_goals.append(f"Noch {2 - len(st.session_state.joined_groups)} Gruppe beitreten bis zum 'Gruppen-Liebhaber'")

if next_goals:
    for goal in next_goals[:3]:  # Zeige max. 3 Ziele
        st.info(goal)
else:
    st.success("Wow! Du hast schon viele Level erreicht! Weiter so!")




    
