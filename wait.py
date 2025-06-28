import streamlit as st
from datetime import datetime, time
import random
import uuid
import time as time_module

# --- Page Config ---
st.set_page_config(
    page_title="WAITT - Uni Lübeck",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS - Mobile Optimized ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #A0616A 0%, #6B2C3A 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container spacing fixes */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: clamp(1rem, 3vw, 1.2rem);
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Tab styling - Mobile optimized */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.1);
        padding: 6px;
        border-radius: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 40px;
        padding: 8px 16px;
        background: transparent;
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        font-size: 0.9rem;
        white-space: nowrap;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B5A6B, #6B2C3A) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 90, 107, 0.4);
    }
    
    /* Card styling */
    .group-card, .form-container, .my-group-card, .pinnwand-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: clamp(1rem, 4vw, 2rem);
        margin: 1rem auto;
        max-width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        color: #374151;
    }
    
    .group-card {
        border-top: 4px solid;
        transition: all 0.3s ease;
    }
    
    .group-card-stats { border-top-color: #A0616A; }
    .group-card-psychology { border-top-color: #C4626D; }
    .group-card-bio { border-top-color: #B85450; }
    .group-card-new { border-top-color: #8B5A6B; }
    
    .group-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .group-icon {
        width: clamp(50px, 12vw, 60px);
        height: clamp(50px, 12vw, 60px);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(1.2rem, 4vw, 1.8rem);
        background: linear-gradient(135deg, #A0616A, #6B2C3A);
        color: white;
        box-shadow: 0 4px 15px rgba(160, 97, 106, 0.3);
        flex-shrink: 0;
    }
    
    .group-title {
        font-size: clamp(1.1rem, 4vw, 1.4rem);
        font-weight: 600;
        color: #1f2937 !important;
        margin: 0;
        line-height: 1.3;
    }
    
    .group-meta {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: #6b7280;
        flex-wrap: wrap;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        background: #f3f4f6;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-weight: 500;
        font-size: 0.8rem;
    }
    
    .group-question {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #BE185D;
    }
    
    .question-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #831843;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .question-text {
        font-style: italic;
        color: #374151;
        font-size: clamp(0.9rem, 3vw, 1.1rem);
        line-height: 1.5;
    }
    
    .spaces-badge {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: #831843;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #F9A8D4;
    }
    
    .form-title {
        text-align: center;
        font-size: clamp(1.3rem, 4vw, 1.8rem);
        font-weight: 600;
        color: #374151;
        margin-bottom: 1.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #A0616A, #6B2C3A);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(160, 97, 106, 0.4);
        min-height: 44px;
        font-size: 0.9rem;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(160, 97, 106, 0.6);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stTimeInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.8rem;
        font-size: 1rem;
        min-height: 44px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stTimeInput > div > div > input:focus {
        border-color: #A0616A;
        box-shadow: 0 0 0 3px rgba(160, 97, 106, 0.1);
    }
    
    /* Metrics styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: clamp(1.5rem, 5vw, 2rem);
        font-weight: 700;
        color: white;
    }
    
    .metric-label {
        font-size: clamp(0.8rem, 2.5vw, 0.9rem);
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
    }
    
    .member-tag {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: #831843;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid #F9A8D4;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .answer-item {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #A0616A;
        color: #374151;
    }
    
    .answer-author {
        font-weight: 600;
        color: #831843;
        margin-bottom: 0.5rem;
    }
    
    /* Countdown styles */
    .countdown-container {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 2px solid #F9A8D4;
        margin: 1rem 0;
    }
    
    .countdown-display {
        font-size: clamp(3rem, 10vw, 6rem);
        font-weight: bold;
        color: #831843;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .countdown-text {
        font-size: clamp(1rem, 3vw, 1.2rem);
        color: #6B2C3A;
        margin: 1rem 0;
        font-style: italic;
    }
    
    /* Reward system */
    .reward-container {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .stamp {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin: 0.2rem;
        transition: all 0.3s ease;
    }
    
    .stamp-earned {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .stamp-empty {
        background: #E5E7EB;
        color: #9CA3AF;
        border: 2px dashed #D1D5DB;
    }
    
    /* Mobile adjustments */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.8rem;
            padding: 6px 12px;
        }
        
        .group-header {
            flex-direction: column;
            align-items: flex-start;
        }
        
        .group-meta {
            flex-direction: column;
            gap: 0.3rem;
        }
        
        .group-card, .form-container, .my-group-card, .pinnwand-container {
            padding: 1rem;
            margin: 0.5rem auto;
        }
    }
    
    /* Text color fixes */
    .stForm, .stExpander, .stSelectbox label, .stTextInput label, 
    .stTextArea label, .stTimeInput label, .stSlider label,
    .stRadio label, .stCheckbox label {
        color: #374151 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
def init_session_state():
    """Initialize all session state variables"""
    
    if "groups" not in st.session_state:
        st.session_state.groups = [
            {
                "id": "stats_001",
                "topic": "Statistik Klausur",
                "time": "10:00",
                "room": "Bibliothek Gruppenraum 1",
                "max": 4,
                "members": ["Anna", "Ben"],
                "question": "Was ist deine größte Prokrastinationsgefahr beim Lernen?",
                "answers": {
                    "Anna": "Netflix-Marathons und endloses Scrollen durch Social Media",
                    "Ben": "Perfektionismus - ich bleibe zu lange an einzelnen Aufgaben hängen"
                },
                "icon": "📊",
                "category": "stats"
            },
            {
                "id": "psych_001", 
                "topic": "Klinische Psychologie",
                "time": "14:30",
                "room": "Mensa Terrasse",
                "max": 3,
                "members": ["Chris"],
                "question": "Was motiviert dich heute am meisten zum Lernen?",
                "answers": {
                    "Chris": "Die Vorstellung, später Menschen wirklich helfen zu können"
                },
                "icon": "🧠",
                "category": "psychology"
            },
            {
                "id": "bio_001",
                "topic": "Biopsychologie",
                "time": "09:00", 
                "room": "Wakenitz-Ufer",
                "max": 5,
                "members": [],
                "question": "Wenn dein Gehirn eine Farbe hätte – welche wäre es und warum?",
                "answers": {},
                "icon": "🔬",
                "category": "bio"
            }
        ]
    
    if "joined_groups" not in st.session_state:
        st.session_state.joined_groups = []
    
    if "pinnwand_entries" not in st.session_state:
        st.session_state.pinnwand_entries = [
            "Gute Musik und der Gedanke an die wohlverdienten Ferien danach",
            "Lerngruppen wie diese - gemeinsam macht alles mehr Spaß!",
            "Starker Kaffee und die Aussicht auf beruflichen Erfolg",
            "Die Wakenitz hilft mir beim Entspannen zwischen den Vorlesungen",
            "Marzipan von Niederegger als kleine Belohnung nach dem Lernen"
        ]
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "Was gibt dir gerade Energie beim Lernen?"
    
    if "pause_statistics" not in st.session_state:
        st.session_state.pause_statistics = {
            "solo_pausen": 0,
            "gruppen_pausen": 0,
            "total_time": 0,
            "trave_spaziergaenge": 0,
            "wakenitz_besuche": 0,
            "mensa_pausen": 0
        }
    
    if "reward_stamps" not in st.session_state:
        st.session_state.reward_stamps = 0
    
    if "reward_claimed" not in st.session_state:
        st.session_state.reward_claimed = False
    
    if "countdown_active" not in st.session_state:
        st.session_state.countdown_active = False
    
    if "countdown_time" not in st.session_state:
        st.session_state.countdown_time = 120

# --- Helper Functions ---
def get_group_card_class(category):
    classes = {
        "stats": "group-card-stats",
        "psychology": "group-card-psychology", 
        "bio": "group-card-bio",
        "new": "group-card-new"
    }
    return classes.get(category, "group-card-stats")

def show_success_message(message):
    st.success(f"✅ {message}")

def show_warning_message(message):
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    st.info(f"ℹ️ {message}")

def add_reward_stamp(activity_type="general"):
    if st.session_state.reward_stamps < 10:
        st.session_state.reward_stamps += 1
        
        if st.session_state.reward_stamps >= 10 and not st.session_state.reward_claimed:
            st.balloons()
            show_success_message("🎉 Glückwunsch! Du hast 10 Stempel gesammelt! Zeige diese App in der Mensa vor und erhalte ein kostenloses Essen!")
            st.session_state.reward_claimed = True
        else:
            remaining = 10 - st.session_state.reward_stamps
            show_success_message(f"Stempel erhalten! Noch {remaining} bis zum kostenlosen Mensa-Essen! 🍽️")

def render_group_card(group):
    card_class = get_group_card_class(group.get("category", "new"))
    free_spaces = group["max"] - len(group["members"])
    is_joined = group["id"] in st.session_state.joined_groups
    
    st.markdown(f"""
    <div class="group-card {card_class}">
        <div class="group-header">
            <div class="group-icon">{group["icon"]}</div>
            <div style="flex: 1;">
                <h3 class="group-title">{group["topic"]}</h3>
                <span class="spaces-badge">{free_spaces} freie Plätze</span>
            </div>
        </div>
        <div class="group-meta">
            <div class="meta-item">🕐 {group["time"]}</div>
            <div class="meta-item">📍 {group["room"]}</div>
            <div class="meta-item">👥 {len(group["members"])}/{group["max"]}</div>
        </div>
        <div class="group-question">
            <div class="question-label">Einstiegsfrage</div>
            <div class="question-text">"{group["question"]}"</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return is_joined, free_spaces

def render_reward_system():
    stamps = st.session_state.reward_stamps
    
    st.markdown("""
    <div class="reward-container">
        <h4 style="color: #92400e; margin-bottom: 1rem; text-align: center;">
            🏆 Mensa-Belohnungssystem
        </h4>
        <p style="color: #78350f; text-align: center; margin-bottom: 1rem;">
            Sammle 10 Stempel durch Lerngruppen-Aktivitäten und Pausen!<br>
            <strong>Belohnung: Kostenloses Essen in der Mensa der Uni Lübeck! 🍽️</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render stamp grid
    cols = st.columns(5)
    for i in range(10):
        with col2:
        total_members = sum(len(group["members"]) for group in st.session_state.groups)
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_members}</div>
            <div class="metric-label">Lernende</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_pauses = st.session_state.pause_statistics["solo_pausen"] + st.session_state.pause_statistics["gruppen_pausen"]
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_pauses}</div>
            <div class="metric-label">Pausen genommen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        stamps = st.session_state.reward_stamps
        stamp_emoji = "🏆" if stamps >= 10 else "⭐"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{stamps}{stamp_emoji}</div>
            <div class="metric-label">Mensa-Stempel</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show reward system if close to completion
    if st.session_state.reward_stamps >= 7:
        render_reward_system()
    
    # Main Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Gruppen finden", 
        "➕ Gruppe erstellen", 
        "👥 Meine Gruppen", 
        "📌 Pinnwand", 
        "🌿 Lernpausen"
    ])
    
    # Tab 1: Find Groups
    with tab1:
        st.markdown("## 🎓 Lerngruppen an der Uni Lübeck")
        
        # Filter options
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Suche nach Thema", placeholder="z.B. Statistik, Psychologie...")
        with col2:
            show_full_only = st.checkbox("Nur freie Plätze", value=True)
        
        # Filter groups
        filtered_groups = st.session_state.groups
        if search_term:
            filtered_groups = [g for g in filtered_groups if search_term.lower() in g["topic"].lower()]
        if show_full_only:
            filtered_groups = [g for g in filtered_groups if len(g["members"]) < g["max"]]
        
        # Display groups
        for group in filtered_groups:
            is_joined, free_spaces = render_group_card(group)
            
            if not is_joined and free_spaces > 0:
                answer = st.text_area(
                    "💭 Deine Antwort auf die Einstiegsfrage:",
                    key=f"answer_{group['id']}",
                    height=100,
                    placeholder="Teile deine Gedanken mit der Gruppe..."
                )
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button(f"🚀 Gruppe beitreten", key=f"join_{group['id']}", use_container_width=True):
                        if answer.strip():
                            group["members"].append("Du")
                            group["answers"]["Du"] = answer.strip()
                            st.session_state.joined_groups.append(group["id"])
                            add_reward_stamp("group_join")
                            st.rerun()
                        else:
                            show_warning_message("Bitte beantworte zuerst die Einstiegsfrage.")
                
                with col2:
                    if st.button("👁️ Vorschau", key=f"preview_{group['id']}", use_container_width=True):
                        with st.expander("Bisherige Antworten", expanded=True):
                            if group["answers"]:
                                for name, ans in group["answers"].items():
                                    st.markdown(f"""
                                    <div class="answer-item">
                                        <div class="answer-author">{name}</div>
                                        <div>"{ans}"</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.write("Noch keine Antworten vorhanden.")
            
            elif is_joined:
                st.success("✅ Du bist bereits Mitglied dieser Gruppe")
            else:
                st.warning("⚠️ Gruppe ist bereits voll")
            
            st.markdown("---")
    
    # Tab 2: Create Group
    with tab2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="form-title">🏗️ Neue Lerngruppe erstellen</h2>', unsafe_allow_html=True)
        
        luebeck_locations = [
            "Bibliothek Gruppenraum 1", "Bibliothek Gruppenraum 2", 
            "Mensa Terrasse", "Café Campus", "Lernwiese (bei schönem Wetter)",
            "Wakenitz-Ufer", "Trave-Promenade", "St. Annen-Museum Café",
            "Ratzeburger Allee Campus", "Online (Zoom)", "Online (Teams)"
        ]
        
        with st.form("create_group_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input("📚 Thema", placeholder="z.B. Statistik Klausur...")
                time_input = st.time_input("🕐 Uhrzeit", value=time(10, 0))
                room = st.selectbox("📍 Treffpunkt in Lübeck", luebeck_locations)
            
            with col2:
                max_members = st.slider("👥 Maximale Teilnehmerzahl", 2, 10, 4)
                icon = st.selectbox("🎯 Icon", ["📊", "🧠", "🔬", "📚", "💡", "🎯", "🧮", "🎨", "🌟", "⚡", "🚀", "💻"])
                category = st.selectbox("📂 Fachbereich", ["psychology", "medicine", "computer_science", "bio", "stats", "other"])
            
            question = st.text_area(
                "❓ Einstiegsfrage für neue Mitglieder",
                placeholder="Was möchtest du von deiner Lerngruppe wissen?",
                height=100
            )
            
            submitted = st.form_submit_button("🚀 Gruppe erstellen", use_container_width=True)
            
            if submitted:
                if topic.strip() and question.strip():
                    new_group = {
                        "id": str(uuid.uuid4()),
                        "topic": topic.strip(),
                        "time": time_input.strftime("%H:%M"),
                        "room": room,
                        "max": max_members,
                        "members": ["Du"],
                        "question": question.strip(),
                        "answers": {"Du": "(Gruppengründer)"},
                        "icon": icon,
                        "category": category
                    }
                    
                    st.session_state.groups.append(new_group)
                    st.session_state.joined_groups.append(new_group["id"])
                    add_reward_stamp("group_create")
                    
                    show_success_message(f"Gruppe '{topic}' erfolgreich erstellt!")
                    st.balloons()
                    st.rerun()
                else:
                    show_warning_message("Bitte fülle alle Pflichtfelder aus.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Lübeck tips
        st.markdown("""
        ### 💡 Tipps für Lerngruppen in Lübeck
        
        **🏛️ Campus-Tipps:**
        - Bibliothek: Ruhige Gruppenräume - früh buchen!
        - Mensa-Terrasse: Perfekt für entspannte Gespräche
        - Wakenitz-Ufer: Outdoor-Sessions bei schönem Wetter
        
        **🚲 Mobilität:**
        - Lübeck ist fahrradfreundlich - fast alles erreichbar
        - Semesterticket für kostenlosen ÖPNV
        """)
    
    # Tab 3: My Groups
    with tab3:
        st.markdown("## 👥 Deine Lerngruppen")
        
        my_groups = [g for g in st.session_state.groups if g["id"] in st.session_state.joined_groups]
        
        if not my_groups:
            st.info("Du bist noch keiner Gruppe beigetreten. Entdecke spannende Lerngruppen oder erstelle deine eigene!")
        else:
            for group in my_groups:
                st.markdown(f"""
                <div class="my-group-card">
                    <div class="group-header">
                        <div class="group-icon">{group["icon"]}</div>
                        <div style="flex: 1;">
                            <h3 class="group-title">{group["topic"]}</h3>
                            <div class="group-meta">
                                <div class="meta-item">🕐 {group["time"]}</div>
                                <div class="meta-item">📍 {group["room"]}</div>
                                <div class="meta-item">👥 {len(group["members"])}/{group["max"]}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="group-question">
                        <div class="question-label">Einstiegsfrage</div>
                        <div class="question-text">"{group["question"]}"</div>
                    </div>
                    
                    <h4 style="margin: 1.5rem 0 1rem 0; color: #374151;">Mitglieder:</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;">
                """, unsafe_allow_html=True)
                
                for member in group["members"]:
                    st.markdown(f'<span class="member-tag">{member}</span>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                if group["answers"]:
                    st.markdown('<h4 style="margin: 1.5rem 0 1rem 0; color: #374151;">Antworten:</h4>', unsafe_allow_html=True)
                    for name, answer in group["answers"].items():
                        st.markdown(f"""
                        <div class="answer-item">
                            <div class="answer-author">{name}</div>
                            <div>"{answer}"</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🌿 Gruppenpause planen", key=f"pause_{group['id']}", use_container_width=True):
                        activities = get_luebeck_activities()["gruppe"]
                        activity = random.choice(activities)
                        st.info(f"**{activity['name']}** - {activity['location']} ({activity['duration']})")
                        st.write(activity['instructions'])
                        
                        if st.button(f"✅ Pause gemacht!", key=f"done_{group['id']}", use_container_width=True):
                            st.session_state.pause_statistics["gruppen_pausen"] += 1
                            st.session_state.pause_statistics["total_time"] += 30
                            for _ in range(activity['stamps']):
                                add_reward_stamp("group_activity")
                            st.rerun()
                
                with col2:
                    if st.button(f"👋 Gruppe verlassen", key=f"leave_{group['id']}", use_container_width=True):
                        if "Du" in group["members"]:
                            group["members"].remove("Du")
                        if "Du" in group["answers"]:
                            del group["answers"]["Du"]
                        if group["id"] in st.session_state.joined_groups:
                            st.session_state.joined_groups.remove(group["id"])
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
    
    # Tab 4: Pinnwand
    with tab4:
        st.markdown(f"""
        <div class="pinnwand-container">
            <h2 style="color: #831843; margin-bottom: 2rem;">📌 Frage der Woche</h2>
            <div style="background: linear-gradient(135deg, #FDF2F8, #FCE7F3); padding: 1.5rem; border-radius: 15px; border: 2px solid #F9A8D4;">
                <h3 style="color: #831843; margin: 0;">{st.session_state.current_question}</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("pinnwand_form"):
            new_entry = st.text_area(
                "💭 Dein Beitrag:",
                placeholder="Was gibt dir gerade Energie beim Lernen?",
                height=100
            )
            
            if st.form_submit_button("📌 Auf Pinnwand posten", use_container_width=True):
                if new_entry.strip():
                    st.session_state.pinnwand_entries.append(new_entry.strip())
                    add_reward_stamp("pinnwand_post")
                    show_success_message("Dein Beitrag wurde zur Pinnwand hinzugefügt!")
                    st.rerun()
                else:
                    show_warning_message("Bitte schreibe etwas, bevor du postest.")
        
        st.markdown("### 💫 Antworten der Uni Lübeck Community")
        
        if st.session_state.pinnwand_entries:
            cols_per_row = 2
            num_entries = len(st.session_state.pinnwand_entries)
            
            for i in range(0, num_entries, cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    entry_idx = i + j
                    if entry_idx < num_entries:
                        entry = st.session_state.pinnwand_entries[entry_idx]
                        with col:
                            colors = [
                                ("#fef3c7", "#f59e0b", "-1deg"),
                                ("#dcfce7", "#10b981", "1deg"), 
                                ("#fce7f3", "#ec4899", "-0.5deg"),
                                ("#dbeafe", "#3b82f6", "0.8deg")
                            ]
                            bg_color, border_color, rotation = colors[entry_idx % 4]
                            
                            st.markdown(f"""
                            <div style="
                                background: {bg_color};
                                padding: 1.5rem;
                                border-radius: 15px;
                                margin: 1rem 0;
                                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                                border: 1px solid {border_color};
                                position: relative;
                                transform: rotate({rotation});
                                min-height: 120px;
                                display: flex;
                                align-items: center;
                            ">
                                <div style="position: absolute; top: -10px; right: 15px; font-size: 1.2rem;">📌</div>
                                <p style="margin: 0; font-size: 1rem; line-height: 1.5; color: #374151; font-style: italic;">"{entry}"</p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("Noch keine Beiträge. Sei der Erste und teile deine Motivation!")
        
        with st.expander("🔧 Admin: Pinnwand verwalten"):
            new_question = st.text_input("Neue Frage der Woche:", value=st.session_state.current_question)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Frage ändern", use_container_width=True):
                    if new_question.strip():
                        st.session_state.current_question = new_question.strip()
                        show_success_message("Frage der Woche wurde aktualisiert!")
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Pinnwand leeren", use_container_width=True):
                    st.session_state.pinnwand_entries = []
                    show_info_message("Pinnwand wurde geleert.")
                    st.rerun()
    
    # Tab 5: Lernpausen
    with tab5:
        st.markdown("# 🌿 Gesunde Lernpausen in Lübeck")
        st.info("🌊 Nutze Lübecks einzigartige Lage für deine Pausen! Von der Wakenitz bis zur Ostsee - hier findest du Entspannung und sammelst Stempel für kostenlose Mensa-Mahlzeiten! 🍽️")
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["solo_pausen"]}</div>
                <div class="metric-label">Solo-Pausen</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["trave_spaziergaenge"]}</div>
                <div class="metric-label">Trave-Spaziergänge</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["wakenitz_besuche"]}</div>
                <div class="metric-label">Wakenitz-Besuche</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["total_time"]}</div>
                <div class="metric-label">Min. Pause</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 2-Minute Countdown
        st.markdown("### 🧘 Sofort-Entspannung")
        render_countdown_timer()
        
        # Activity selection
        pause_type = st.radio(
            "Was für eine Pause brauchst du?",
            ["🧘 Solo-Pause (Allein entspannen)", "👥 Gruppen-Pause (Mit anderen Zeit verbringen)"],
            horizontal=True
        )
        
        activities = get_luebeck_activities()
        
        if "Solo-Pause" in pause_type:
            st.markdown("### 🌊 Solo-Aktivitäten in Lübeck")
            
            if st.button("🎲 Zufällige Lübeck-Aktivität", use_container_width=True):
                activity = random.choice(activities["solo"])
                st.session_state.current_solo_activity = activity
            
            if "current_solo_activity" in st.session_state:
                activity = st.session_state.current_solo_activity
                st.markdown(f"""
                <div class="form-container">
                    <h3 style="color: #831843;">📍 {activity["name"]}</h3>
                    <p><strong>Ort:</strong> {activity["location"]} | <strong>Dauer:</strong> {activity["duration"]}</p>
                    <p><strong>Beschreibung:</strong> {activity["description"]}</p>
                    <div style="background: #F9FAFB; padding: 1rem; border-radius: 10px; border-left: 4px solid #A0616A;">
                        <h4 style="color: #374151;">📝 So geht's:</h4>
                        <p style="color: #374151;">{activity["instructions"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Pause gemacht!", key="solo_done", use_container_width=True):
                        st.session_state.pause_statistics["solo_pausen"] += 1
                        duration = int(activity['duration'].split()[0])
                        st.session_state.pause_statistics["total_time"] += duration
                        
                        if "trave" in activity['name'].lower():
                            st.session_state.pause_statistics["trave_spaziergaenge"] += 1
                        elif "wakenitz" in activity['name'].lower():
                            st.session_state.pause_statistics["wakenitz_besuche"] += 1
                        elif "mensa" in activity['name'].lower():
                            st.session_state.pause_statistics["mensa_pausen"] += 1
                        
                        for _ in range(activity['stamps']):
                            add_reward_stamp("solo_activity")
                        
                        show_success_message(f"Super! +{activity['stamps']} Stempel für deine Lübeck-Pause! 🌟")
                        st.balloons()
                
                with col2:
                    if st.button("🔄 Andere Aktivität", key="solo_new", use_container_width=True):
                        st.session_state.current_solo_activity = random.choice(activities["solo"])
                        st.rerun()
        
        else:  # Group activities
            st.markdown("### 👥 Gruppen-Aktivitäten in Lübeck")
            
            my_groups = [g for g in st.session_state.groups if g["id"] in st.session_state.joined_groups]
            if my_groups:
                group_for_pause = st.selectbox("Mit welcher Lerngruppe?", [g["topic"] for g in my_groups])
                
                if st.button("🎲 Gruppen-Aktivität in Lübeck vorschlagen", use_container_width=True):
                    activity = random.choice(activities["gruppe"])
                    st.session_state.current_group_activity = activity
                
                if "current_group_activity" in st.session_state:
                    activity = st.session_state.current_group_activity
                    st.markdown(f"""
                    <div class="form-container">
                        <h3 style="color: #831843;">👥 {activity["name"]}</h3>
                        <p><strong>Ort:</strong> {activity["location"]} | <strong>Dauer:</strong> {activity["duration"]} | <strong>Stempel:</strong> +{activity["stamps"]}</p>
                        <p><strong>Beschreibung:</strong> {activity["description"]}</p>
                        <div style="background: #F9FAFB; padding: 1rem; border-radius: 10px; border-left: 4px solid #A0616A;">
                            <h4 style="color: #374151;">📝 So geht's:</h4>
                            <p style="color: #374151;">{activity["instructions"]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Gruppenpause gemacht!", key="group_done", use_container_width=True):
                            st.session_state.pause_statistics["gruppen_pausen"] += 1
                            duration = int(activity['duration'].split()[0])
                            st.session_state.pause_statistics["total_time"] += duration
                            
                            if "trave" in activity['name'].lower():
                                st.session_state.pause_statistics["trave_spaziergaenge"] += 1
                            elif "wakenitz" in activity['name'].lower():
                                st.session_state.pause_statistics["wakenitz_besuche"] += 1
                            elif "mensa" in activity['name'].lower():
                                st.session_state.pause_statistics["mensa_pausen"] += 1
                            
                            for _ in range(activity['stamps']):
                                add_reward_stamp("group_activity")
                            
                            show_success_message(f"Fantastisch! +{activity['stamps']} Stempel für eure Lübeck-Gruppenpause! 🤝")
                            st.balloons()
                    
                    with col2:
                        if st.button("🔄 Andere Gruppenaktivität", key="group_new", use_container_width=True):
                            st.session_state.current_group_activity = random.choice(activities["gruppe"])
                            st.rerun()
            else:
                st.info("Tritt erst einer Lerngruppe bei, um Gruppen-Pausen in Lübeck zu planen!")
        
        # Lübeck wellness tips
        st.markdown("---")
        st.markdown("### 💡 Lübeck-Wellness-Tipps für Studierende")
        
        tips = [
            "🌊 **Ostsee-Therapie**: 20 Min. Meeresluft in Travemünde = Reset für Körper & Geist",
            "🚲 **Fahrrad-Meditation**: Lübeck ist perfekt zum entspannten Radeln",
            "🦆 **Wakenitz-Regel**: 'Amazonas des Nordens' - 10 Min. am Wasser = Stressabbau",
            "🏛️ **Kultur-Pausen**: Altstadt-Spaziergang durch UNESCO-Welterbe entspannt",
            "🍯 **Marzipan-Achtsamkeit**: Ein Stück Niederegger bewusst genießen",
            "⛵ **Trave-Therapie**: Schiffe beobachten beruhigt sofort"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
        
        # Show reward system
        if st.session_state.reward_stamps >= 5:
            st.markdown("---")
            render_reward_system()
        
        # Help resources
        st.markdown("---")
        st.markdown("### 🆘 Hilfe & Beratung an der Uni Lübeck")
        st.markdown("""
        **📞 Psychologische Beratung:**
        - **Studentenwerk S-H** - Mönkhofer Weg 241 (Mensagebäude), Raum 44
        - **Tel:** 0451/29220-908
        - **Kostenlos und vertraulich** für alle Studierenden
        
        **🏥 Krisenhilfe:**
        - **Zentrum für Integrative Psychiatrie (ZiP)**
        - **Dr. Bartosz Zurowski** - Tel: 0451/500-98831
        
        **💬 Online-Unterstützung:**
        - **StudiCare** - Online-Trainings für Studierende in Krisen
        """)

if __name__ == "__main__":
    main()s[i % 5]:
            if i < stamps:
                st.markdown('<div class="stamp stamp-earned">⭐</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="stamp stamp-empty">{i+1}</div>', unsafe_allow_html=True)
    
    # Show progress
    progress = stamps / 10
    st.progress(progress)
    
    if stamps >= 10 and not st.session_state.reward_claimed:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10B981, #059669); color: white; 
             padding: 1rem; border-radius: 12px; text-align: center; margin: 1rem 0;">
            <h4>🎉 BELOHNUNG BEREIT! 🎉</h4>
            <p>Zeige diese App-Seite in der Mensa vor und erhalte dein kostenloses Essen!</p>
            <p><strong>Mensa-Standort:</strong> Mönkhofer Weg 241, 23562 Lübeck</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ Belohnung eingelöst", use_container_width=True):
            st.session_state.reward_claimed = True
            st.session_state.reward_stamps = 0
            show_success_message("Belohnung eingelöst! Du kannst wieder neue Stempel sammeln.")
            st.rerun()
    
    elif stamps < 10:
        remaining = 10 - stamps
        st.write(f"**Noch {remaining} Stempel bis zur Belohnung!**")

def render_countdown_timer():
    if not st.session_state.countdown_active:
        st.markdown("""
        <div class="countdown-container">
            <h3 style="color: #831843; margin-bottom: 1rem;">🧘 2-Minuten Nichtstun-Challenge</h3>
            <p style="color: #6B2C3A; margin-bottom: 1.5rem;">
                Manchmal ist das Beste, was wir tun können, einfach <strong>nichts zu tun</strong>.<br>
                Diese 2 Minuten gehören nur dir - keine Aufgaben, kein Handy, nur du und der Moment.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎯 2-Minuten Timer starten", use_container_width=True):
            st.session_state.countdown_active = True
            st.session_state.countdown_time = 120
            st.rerun()
    
    else:
        if st.session_state.countdown_time > 0:
            minutes = st.session_state.countdown_time // 60
            seconds = st.session_state.countdown_time % 60
            
            st.markdown(f"""
            <div class="countdown-container">
                <div class="countdown-display">{minutes:02d}:{seconds:02d}</div>
                <div class="countdown-text">
                    Einfach dasitzen und atmen...<br>
                    Du musst nichts tun. Du musst nichts erreichen.<br>
                    Dieser Moment gehört nur dir. 🌸
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Simple countdown without auto-refresh (to avoid Streamlit issues)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏸️ Pause", use_container_width=True):
                    st.session_state.countdown_active = False
                    st.rerun()
            with col2:
                if st.button("⬇️ -10 Sek", use_container_width=True):
                    st.session_state.countdown_time = max(0, st.session_state.countdown_time - 10)
                    st.rerun()
        
        else:
            st.markdown("""
            <div class="countdown-container">
                <div style="font-size: 3rem; margin: 1rem 0;">🎉</div>
                <h3 style="color: #831843;">Geschafft!</h3>
                <p style="color: #6B2C3A;">
                    Du hast dir 2 Minuten nur für dich genommen.<br>
                    Das war ein Geschenk an dich selbst. 💚
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Pause beendet", use_container_width=True):
                    st.session_state.countdown_active = False
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.pause_statistics["total_time"] += 2
                    add_reward_stamp("countdown")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Nochmal 2 Minuten", use_container_width=True):
                    st.session_state.countdown_time = 120
                    st.rerun()

def get_luebeck_activities():
    return {
        "solo": [
            {
                "name": "Wakenitz-Meditation",
                "duration": "10 min",
                "type": "Natur & Achtsamkeit", 
                "location": "Wakenitz-Ufer",
                "description": "Entspannung am 'Amazonas des Nordens'",
                "instructions": "Gehe zum Wakenitz-Ufer (5 Min. vom Campus). Setze dich ans Wasser und atme die frische Luft.",
                "stamps": 1
            },
            {
                "name": "Trave-Spaziergang",
                "duration": "15 min",
                "type": "Bewegung",
                "location": "Trave-Promenade", 
                "description": "Entspannter Gang entlang Lübecks Lebensader",
                "instructions": "Gehe zur Trave und spaziere entspannt entlang des Wassers bis zur Hubbrücke.",
                "stamps": 1
            },
            {
                "name": "Mensa-Dachterrasse",
                "duration": "5 min",
                "type": "Schnelle Erholung",
                "location": "Mensa",
                "description": "Frischluft zwischen den Vorlesungen", 
                "instructions": "Gehe auf die Mensa-Terrasse, mache 5 tiefe Atemzüge und strecke dich.",
                "stamps": 1
            }
        ],
        "gruppe": [
            {
                "name": "Trave-Rundgang",
                "duration": "30 min", 
                "type": "Bewegung & Soziales",
                "location": "Trave-Ufer",
                "description": "Gemeinsamer Spaziergang entlang der Trave",
                "instructions": "Trefft euch am Campus und geht zur Trave. Erste 15 Min. kein Uni-Talk!",
                "stamps": 2
            },
            {
                "name": "Wakenitz-Picknick",
                "duration": "45 min",
                "type": "Natur & Gemeinschaft",
                "location": "Wakenitz-Wiesen", 
                "description": "Entspanntes Gruppenpicknick am Wasser",
                "instructions": "Bringt Snacks mit und setzt euch an die Wakenitz. Spielt einfache Spiele!",
                "stamps": 2
            },
            {
                "name": "Mensa-Socializing", 
                "duration": "25 min",
                "type": "Entspannung",
                "location": "Mensa",
                "description": "Entspannte Café-Zeit auf dem Campus",
                "instructions": "Trefft euch in der Mensa, holt Getränke und redet über Nicht-Uni-Themen.",
                "stamps": 2
            }
        ]
    }

# --- Main App ---
def main():
    init_session_state()
    
    # Title
    st.markdown('<h1 class="main-title">WAITT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">We\'re all in this together - Uni Lübeck</p>', unsafe_allow_html=True)
    
    # Stats Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(st.session_state.groups)}</div>
            <div class="metric-label">Aktive Gruppen</div>
        </div>
        """, unsafe_allow_html=True)
    
  
