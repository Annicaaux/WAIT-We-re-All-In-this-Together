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
        margin-bottom: 0.8rem !important;
    }
    
    .stMarkdown {
        margin-bottom: 0.5rem !important;
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
        padding: 0;
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: clamp(1rem, 3vw, 1.2rem);
        margin-bottom: 1.5rem;
        opacity: 0.9;
        padding: 0;
    }
    
    /* Tab styling - Mobile optimized */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.1);
        padding: 6px;
        border-radius: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        overflow-x: auto;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 40px;
        padding: 8px 12px;
        background: transparent;
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        font-size: 0.85rem;
        white-space: nowrap;
        flex-shrink: 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B5A6B, #6B2C3A) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 90, 107, 0.4);
    }
    
    /* Card styling - Better spacing */
    .group-card, .form-container, .my-group-card, .pinnwand-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: clamp(1rem, 4vw, 2rem);
        margin: 1rem auto 1.5rem auto;
        max-width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        color: #374151;
        word-wrap: break-word;
    }
    
    .group-card {
        border-top: 4px solid;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
    }
    
    .group-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .group-card-stats { border-top-color: #A0616A; }
    .group-card-psychology { border-top-color: #C4626D; }
    .group-card-bio { border-top-color: #B85450; }
    .group-card-new { border-top-color: #8B5A6B; }
    
    /* Group header - Mobile responsive */
    .group-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1.2rem;
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
        margin: 0 0 0.5rem 0;
        line-height: 1.3;
    }
    
    /* Meta information - Mobile stack */
    .group-meta {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        font-size: 0.8rem;
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
        font-size: 0.75rem;
        flex-shrink: 0;
    }
    
    /* Question styling */
    .group-question {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #BE185D;
    }
    
    .question-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #831843;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .question-text {
        font-style: italic;
        color: #374151;
        font-size: clamp(0.9rem, 3vw, 1rem);
        line-height: 1.5;
        margin: 0;
    }
    
    .spaces-badge {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: #831843;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #F9A8D4;
        display: inline-block;
        margin-top: 0.3rem;
    }
    
    /* Form improvements */
    .form-title {
        text-align: center;
        font-size: clamp(1.3rem, 4vw, 1.8rem);
        font-weight: 600;
        color: #374151;
        margin-bottom: 1.5rem;
        line-height: 1.3;
    }
    
    /* Button styling - Touch friendly */
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
        margin: 0.3rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(160, 97, 106, 0.6);
        background: linear-gradient(135deg, #8B5A6B, #5A1F2A);
    }
    
    /* Input styling - Mobile friendly */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stTimeInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.8rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        min-height: 44px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stTimeInput > div > div > input:focus {
        border-color: #A0616A;
        box-shadow: 0 0 0 3px rgba(160, 97, 106, 0.1);
        outline: none;
    }
    
    /* Metrics styling - Mobile grid */
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
        line-height: 1;
    }
    
    .metric-label {
        font-size: clamp(0.7rem, 2.5vw, 0.85rem);
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
        line-height: 1.2;
    }
    
    /* Tags and badges */
    .member-tag {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: #831843;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.75rem;
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
        font-size: 0.9rem;
    }
    
    /* Countdown specific styles */
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
        line-height: 1;
    }
    
    .countdown-text {
        font-size: clamp(0.9rem, 3vw, 1.1rem);
        color: #6B2C3A;
        margin: 1rem 0;
        font-style: italic;
        line-height: 1.4;
    }
    
    /* Reward system styles */
    .reward-container {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .stamp {
        width: clamp(35px, 8vw, 45px);
        height: clamp(35px, 8vw, 45px);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(1rem, 3vw, 1.3rem);
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
        font-size: clamp(0.7rem, 2vw, 0.9rem);
    }
    
    /* Mobile specific adjustments */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.75rem;
            padding: 6px 10px;
        }
        
        .group-header {
            flex-direction: column;
            align-items: flex-start;
            text-align: left;
        }
        
        .group-meta {
            flex-direction: column;
            gap: 0.3rem;
        }
        
        .meta-item {
            width: fit-content;
        }
        
        .group-card, .form-container, .my-group-card, .pinnwand-container {
            padding: 1rem;
            margin: 0.5rem auto 1rem auto;
        }
        
        .stColumns {
            gap: 0.5rem;
        }
        
        .countdown-container {
            padding: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.7rem;
            padding: 5px 8px;
        }
        
        .group-card, .form-container, .my-group-card, .pinnwand-container {
            padding: 0.8rem;
            margin: 0.3rem auto 0.8rem auto;
        }
        
        .group-question {
            padding: 0.8rem;
        }
        
        .countdown-container {
            padding: 1rem;
        }
    }
    
    /* Text color fixes for all containers */
    .stForm, .stExpander, .stSelectbox label, .stTextInput label, 
    .stTextArea label, .stTimeInput label, .stSlider label,
    .stRadio label, .stCheckbox label {
        color: #374151 !important;
    }
    
    /* Success/Warning/Info styling */
    .stSuccess, .stWarning, .stInfo, .stError {
        border-radius: 12px;
        margin: 0.8rem 0;
        border: none;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
        border-left: 4px solid #10B981;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));
        border-left: 4px solid #F59E0B;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
        border-left: 4px solid #3B82F6;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Loading states */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #A0616A;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
def init_session_state():
    """Initialize all session state variables"""
    
    # Basic groups data with Lübeck locations
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
            },
            {
                "id": "med_001",
                "topic": "Anatomie Testat",
                "time": "16:00",
                "room": "Trave-Promenade",
                "max": 6,
                "members": ["Lisa", "Tom", "Sarah"],
                "question": "Welche Lernmethode hilft dir am besten beim Auswendiglernen?",
                "answers": {
                    "Lisa": "Karteikarten und ständige Wiederholung",
                    "Tom": "Zusammen mit anderen laut vorsagen",
                    "Sarah": "Eselsbrücken und verrückte Geschichten erfinden"
                },
                "icon": "⚕️",
                "category": "medicine"
            }
        ]
    
    # User's joined groups
    if "joined_groups" not in st.session_state:
        st.session_state.joined_groups = []
    
    # Pinnwand entries with Lübeck flavor
    if "pinnwand_entries" not in st.session_state:
        st.session_state.pinnwand_entries = [
            "Gute Musik und der Gedanke an die wohlverdienten Ferien danach",
            "Lerngruppen wie diese - gemeinsam macht alles mehr Spaß!",
            "Starker Kaffee und die Aussicht auf beruflichen Erfolg",
            "Die Wakenitz hilft mir beim Entspannen zwischen den Vorlesungen",
            "Marzipan von Niederegger als kleine Belohnung nach dem Lernen",
            "Ein Spaziergang zur Trave bringt mich immer auf andere Gedanken",
            "Die Bibliothek mit Blick auf den Campus motiviert mich sehr"
        ]
    
    # Current week question
    if "current_question" not in st.session_state:
        st.session_state.current_question = "Was gibt dir gerade Energie beim Lernen?"
    
    # Pause statistics with Lübeck integration
    if "pause_statistics" not in st.session_state:
        st.session_state.pause_statistics = {
            "solo_pausen": 0,
            "gruppen_pausen": 0,
            "total_time": 0,
            "trave_spaziergaenge": 0,
            "wakenitz_besuche": 0,
            "mensa_pausen": 0,
            "altstadt_besuche": 0,
            "ostsee_trips": 0
        }
    
    # Reward system (Mensa stamps)
    if "reward_stamps" not in st.session_state:
        st.session_state.reward_stamps = 0
    
    if "reward_claimed" not in st.session_state:
        st.session_state.reward_claimed = False
    
    # Countdown state
    if "countdown_active" not in st.session_state:
        st.session_state.countdown_active = False
    
    if "countdown_time" not in st.session_state:
        st.session_state.countdown_time = 120  # 2 minutes in seconds
    
    # Activity states
    if "current_solo_activity" not in st.session_state:
        st.session_state.current_solo_activity = None
    
    if "current_group_activity" not in st.session_state:
        st.session_state.current_group_activity = None

# --- Helper Functions ---
def get_group_card_class(category):
    """Get CSS class for group card based on category"""
    classes = {
        "stats": "group-card-stats",
        "psychology": "group-card-psychology", 
        "bio": "group-card-bio",
        "medicine": "group-card-psychology",
        "computer_science": "group-card-stats",
        "new": "group-card-new"
    }
    return classes.get(category, "group-card-stats")

def show_success_message(message):
    """Show success message with emoji"""
    st.success(f"✅ {message}")

def show_warning_message(message):
    """Show warning message with emoji"""
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    """Show info message with emoji"""
    st.info(f"ℹ️ {message}")

def add_reward_stamp(activity_type="general"):
    """Add a reward stamp and check for completion"""
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
    """Render a single group card with modern styling and Lübeck locations"""
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
    """Render the reward stamp collection system"""
    stamps = st.session_state.reward_stamps
    
    st.markdown("""
    <div class="reward-container">
        <h4 style="color: #92400e; margin-bottom: 1rem; text-align: center;">
            🏆 Mensa-Belohnungssystem
        </h4>
        <p style="color: #78350f; text-align: center; margin-bottom: 1rem; font-size: 0.9rem; line-height: 1.4;">
            Sammle 10 Stempel durch Lerngruppen-Aktivitäten und Pausen!<br>
            <strong>Belohnung: Kostenloses Essen in der Mensa der Uni Lübeck! 🍽️</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render stamp grid
    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
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
             padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0;">
            <h4 style="margin-bottom: 1rem;">🎉 BELOHNUNG BEREIT! 🎉</h4>
            <p style="margin-bottom: 0.5rem;">Zeige diese App-Seite in der Mensa vor und erhalte dein kostenloses Essen!</p>
            <p style="margin: 0; font-weight: 600;"><strong>Mensa-Standort:</strong> Mönkhofer Weg 241, 23562 Lübeck</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ Belohnung eingelöst", use_container_width=True, key="claim_reward"):
            st.session_state.reward_claimed = True
            st.session_state.reward_stamps = 0
            show_success_message("Belohnung eingelöst! Du kannst wieder neue Stempel sammeln.")
            st.rerun()
    
    elif stamps < 10:
        remaining = 10 - stamps
        st.write(f"**Noch {remaining} Stempel bis zur Belohnung!**")

def render_countdown_timer():
    """Render 2-minute 'do nothing' countdown timer"""
    
    if not st.session_state.countdown_active:
        st.markdown("""
        <div class="countdown-container">
            <h3 style="color: #831843; margin-bottom: 1rem;">🧘 2-Minuten Nichtstun-Challenge</h3>
            <p style="color: #6B2C3A; margin-bottom: 1.5rem; line-height: 1.5;">
                Manchmal ist das Beste, was wir tun können, einfach <strong>nichts zu tun</strong>.<br>
                Diese 2 Minuten gehören nur dir - keine Aufgaben, kein Handy, nur du und der Moment.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎯 2-Minuten Timer starten", use_container_width=True, key="start_countdown"):
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
            
            # Manual controls instead of auto-refresh
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⏸️ Pause", use_container_width=True, key="pause_countdown"):
                    st.session_state.countdown_active = False
                    st.rerun()
            with col2:
                if st.button("⬇️ -10 Sek", use_container_width=True, key="minus_10"):
                    st.session_state.countdown_time = max(0, st.session_state.countdown_time - 10)
                    st.rerun()
            with col3:
                if st.button("⏭️ Fertig", use_container_width=True, key="finish_countdown"):
                    st.session_state.countdown_time = 0
                    st.rerun()
        
        else:
            # Timer finished
            st.markdown("""
            <div class="countdown-container">
                <div style="font-size: 3rem; margin: 1rem 0;">🎉</div>
                <h3 style="color: #831843; margin-bottom: 1rem;">Geschafft!</h3>
                <p style="color: #6B2C3A; line-height: 1.5; margin-bottom: 1.5rem;">
                    Du hast dir 2 Minuten nur für dich genommen.<br>
                    Das war ein Geschenk an dich selbst. 💚
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Pause beendet", use_container_width=True, key="end_countdown"):
                    st.session_state.countdown_active = False
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.pause_statistics["total_time"] += 2
                    add_reward_stamp("countdown")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Nochmal 2 Minuten", use_container_width=True, key="repeat_countdown"):
                    st.session_state.countdown_time = 120
                    st.rerun()

def get_luebeck_activities():
    """Return Lübeck-specific activity recommendations"""
    return {
        "solo": [
            {
                "name": "Wakenitz-Meditation",
                "duration": "10-15 min",
                "type": "Natur & Achtsamkeit",
                "location": "Wakenitz-Ufer",
                "description": "Entspannung am 'Amazonas des Nordens'",
                "instructions": "Gehe zum Wakenitz-Ufer (5 Min. vom Campus). Setze dich ans Wasser, beobachte die Enten und höre dem Plätschern zu. Atme bewusst die frische Luft ein.",
                "stamps": 1
            },
            {
                "name": "Trave-Spaziergang",
                "duration": "15-20 min",
                "type": "Bewegung & Frischluft",
                "location": "Trave-Promenade",
                "description": "Entspannter Gang entlang Lübecks Lebensader",
                "instructions": "Starte an der Uni Richtung Trave. Gehe langsam entlang des Wassers bis zur Hubbrücke. Genieße den Blick auf die Boote und die historische Altstadt.",
                "stamps": 1
            },
            {
                "name": "Holstentor-Pause",
                "duration": "5-10 min",
                "type": "Kultur & Entspannung",
                "location": "Holstentor",
                "description": "Kurze Auszeit am Wahrzeichen",
                "instructions": "Fahre mit dem Rad zum Holstentor. Setze dich auf eine Bank davor und betrachte die imposante Backsteingotik. Denke daran: Du studierst in einer UNESCO-Welterbestadt!",
                "stamps": 1
            },
            {
                "name": "Mensa-Dachterrasse Atempause",
                "duration": "5 min",
                "type": "Schnelle Erholung",
                "location": "Mensa",
                "description": "Frischluft zwischen den Vorlesungen",
                "instructions": "Gehe auf die Mensa-Terrasse. Mache 5 tiefe Atemzüge und strecke dich. Schaue über den Campus und erinnere dich: Du schaffst das!",
                "stamps": 1
            },
            {
                "name": "Niederegger-Entspannung",
                "duration": "10 min",
                "type": "Genuss & Pause",
                "location": "Niederegger Café",
                "description": "Lübecker Marzipan-Meditation",
                "instructions": "Gönne dir ein kleines Stück Marzipan bei Niederegger. Esse es ganz langsam und bewusst. Genieße diesen typisch Lübecker Moment der Süße.",
                "stamps": 1
            },
            {
                "name": "Bibliotheks-Zenmoment",
                "duration": "3-5 min",
                "type": "Schnelle Entspannung",
                "location": "Universitätsbibliothek",
                "description": "Ruhe zwischen den Büchern finden",
                "instructions": "Suche dir einen ruhigen Platz in der Bibliothek. Schließe die Augen und höre 2 Minuten nur auf die Stille und das leise Rascheln der Seiten.",
                "stamps": 1
            }
        ],
        "gruppe": [
            {
                "name": "Trave-Rundgang mit Lerngruppe",
                "duration": "30-45 min",
                "type": "Bewegung & Soziales",
                "location": "Trave-Ufer",
                "description": "Gemeinsamer Spaziergang entlang der Trave",
                "instructions": "Trefft euch am Campus und geht gemeinsam zur Trave. Spaziert entspannt bis zur Fähre und zurück. Regel: Erste 15 Min. kein Uni-Talk!",
                "stamps": 2
            },
            {
                "name": "Wakenitz-Picknick",
                "duration": "45-60 min",
                "type": "Natur & Gemeinschaft",
                "location": "Wakenitz-Wiesen",
                "description": "Entspanntes Gruppenpicknick am Wasser",
                "instructions": "Bringt Snacks mit und setzt euch an die Wakenitz. Spielt einfache Spiele, redet über Nicht-Uni-Themen und genießt die Natur.",
                "stamps": 2
            },
            {
                "name": "Altstadt-Entdeckertour",
                "duration": "60 min",
                "type": "Kultur & Erkundung",
                "location": "Lübecker Altstadt",
                "description": "Gemeinsame Erkundung der Hansestadt",
                "instructions": "Startet am Holstentor und erkundet zusammen die Gänge und Höfe der Altstadt. Macht Fotos, entdeckt versteckte Ecken und genießt das Welterbe.",
                "stamps": 2
            },
            {
                "name": "Mensa-Socializing",
                "duration": "25-30 min",
                "type": "Entspannung & Gespräch",
                "location": "Mensa oder Café Campus",
                "description": "Entspannte Café-Zeit auf dem Campus",
                "instructions": "Trefft euch in der Mensa oder im Café Campus. Holt euch Getränke und redet über Hobbys, Träume und lustige Erlebnisse. Kein Uni-Stress!",
                "stamps": 2
            },
            {
                "name": "Ostsee-Ausflug",
                "duration": "2-3 Stunden",
                "type": "Abenteuer & Entspannung",
                "location": "Travemünde/Timmendorfer Strand",
                "description": "Großer Entspannungsausflug ans Meer",
                "instructions": "Fahrt mit dem Semesterticket nach Travemünde oder Timmendorfer Strand. Spaziert am Strand, atmet Meeresluft und genießt eine große Auszeit vom Lernstress.",
                "stamps": 3
            },
            {
                "name": "Gemeinsames Kochen",
                "duration": "90 min",
                "type": "Kreativität & Teamwork",
                "location": "WG-Küche oder Gemeinschaftsküche",
                "description": "Zusammen kochen und genießen",
                "instructions": "Plant ein einfaches Gericht und kocht gemeinsam. Jeder bringt eine Zutat mit. Beim Essen wird nur über schöne Dinge geredet!",
                "stamps": 2
            }
        ]
    }

def get_luebeck_locations():
    """Return Lübeck-specific meeting locations"""
    return [
        "Bibliothek Gruppenraum 1", "Bibliothek Gruppenraum 2", 
        "Mensa Terrasse", "Café Campus", "Lernwiese (bei schönem Wetter)",
        "Wakenitz-Ufer", "Trave-Promenade", "St. Annen-Museum Café",
        "Holstentor-Platz", "Ratzeburger Allee Campus", 
        "Studentenwohnheim Anschützstraße", "Stadtbibliothek Lübeck",
        "Online (Zoom)", "Online (Teams)", "Online (Discord)"
    ]

def render_luebeck_help_resources():
    """Render Lübeck-specific help and support resources"""
    st.markdown("""
    ### 🆘 Hilfe & Beratung an der Uni Lübeck
    
    **📞 Psychologische Beratung:**
    - **Studentenwerk S-H** - Mönkhofer Weg 241 (Mensagebäude), Raum 44
    - **Tel:** 0451/29220-908 | **Email:** psychologen.hl@studentenwerk.sh
    - **Kostenlos und vertraulich** für alle Studierenden
    - **Sprechzeiten:** Mo, Di, Fr 10-13 Uhr, Do 8-12 & 13-15 Uhr
    
    **🏥 Krisenhilfe:**
    - **Zentrum für Integrative Psychiatrie (ZiP)**
    - **Dr. Bartosz Zurowski** - Tel: 0451/500-98831
    - **Für akute Krisen und psychiatrische Hilfe**
    
    **💬 Online-Unterstützung:**
    - **StudiCare** - Online-Trainings für Studierende in Krisen
    - **Chat-Beratung** der psychologischen Studierendenberatung
    - **Offene Beratung:** Mittwochs 12:30-13:30 Uhr (ohne Voranmeldung)
    
    **🏫 Campus-Angebote:**
    - **Studierenden-Service-Center** - Ratzeburger Allee 160
    - **Allgemeine Studienberatung** - studium@uni-luebeck.de
    - **AG Studierendengesundheit** - Gesunde Hochschule Lübeck
    - **Sozialberatung** - Mensa, Mönkhofer Weg 241, Tel: 0451/500-3301
    
    **🚨 Notfall:**
    - **Krisendienst Schleswig-Holstein:** 0800 / 655 3000 (24/7 kostenlos)
    - **Telefonseelsorge:** 0800 / 111 0 111 oder 0800 / 111 0 222
    """)

def get_category_emoji(category):
    """Get emoji for category"""
    emojis = {
        "stats": "📊",
        "psychology": "🧠", 
        "bio": "🔬",
        "medicine": "⚕️",
        "computer_science": "💻",
        "math": "🧮",
        "physics": "⚛️",
        "chemistry": "🧪",
        "other": "📚"
    }
    return emojis.get(category, "📚")
