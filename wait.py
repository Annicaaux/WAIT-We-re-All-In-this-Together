import streamlit as st
from datetime import datetime, time
import random
import uuid

# --- Page Config ---
st.set_page_config(
    page_title="WAITT - We're all in this together",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px;
        border-radius: 50px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background: transparent;
        border-radius: 50px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Group card styling */
    .group-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border-top: 4px solid;
        transition: all 0.3s ease;
    }
    
    .group-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .group-card-stats {
        border-top-color: #667eea;
    }
    
    .group-card-psychology {
        border-top-color: #10b981;
    }
    
    .group-card-bio {
        border-top-color: #f59e0b;
    }
    
    .group-card-new {
        border-top-color: #ec4899;
    }
    
    .group-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .group-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .group-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }
    
    .group-meta {
        display: flex;
        gap: 1.5rem;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: #f3f4f6;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
    }
    
    .group-question {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border-left: 4px solid #0ea5e9;
    }
    
    .question-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #0369a1;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .question-text {
        font-style: italic;
        color: #374151;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .spaces-badge {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        color: #166534;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #86efac;
    }
    
    /* Form styling */
    .form-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .form-title {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 2rem;
    }
    
    /* My groups styling */
    .my-group-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 5px solid #10b981;
        backdrop-filter: blur(20px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .member-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .member-tag {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        color: #1e40af;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #93c5fd;
    }
    
    .answer-item {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    
    .answer-author {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    /* Pinnwand styling */
    .pinnwand-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .week-question {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 2rem;
        line-height: 1.4;
    }
    
    .postit {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #f59e0b;
        position: relative;
        transform: rotate(-1deg);
        transition: all 0.3s ease;
    }
    
    .postit:nth-child(2n) {
        transform: rotate(1deg);
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        border-color: #10b981;
    }
    
    .postit:nth-child(3n) {
        transform: rotate(-0.5deg);
        background: linear-gradient(135deg, #fce7f3, #fbcfe8);
        border-color: #ec4899;
    }
    
    .postit:hover {
        transform: rotate(0deg) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .postit::before {
        content: '📌';
        position: absolute;
        top: -10px;
        right: 15px;
        font-size: 1.2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Success button */
    .success-btn {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stTimeInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stTimeInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    /* Metrics styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 15px;
        border: none;
        backdrop-filter: blur(10px);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
        border-left: 4px solid #10b981;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));
        border-left: 4px solid #f59e0b;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
        border-left: 4px solid #3b82f6;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .group-meta {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .group-card {
            padding: 1.5rem;
        }
        
        .form-container {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
def init_session_state():
    if "groups" not in st.session_state:
        st.session_state.groups = [
            {
                "id": "stats_001",
                "topic": "Statistik Klausur",
                "time": "10:00",
                "room": "Raum A1",
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
                "room": "Bibliothek Gruppenraum 2",
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
                "room": "Café Campus",
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
            "Meine Katze, die immer neben mir sitzt während ich lerne",
            "Die Vorstellung, dass ich bald Experte in meinem Fach bin"
        ]
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "Was gibt dir gerade Energie beim Lernen?"

# --- Helper Functions ---
def get_group_card_class(category):
    classes = {
        "stats": "group-card-stats",
        "psychology": "group-card-psychology", 
        "bio": "group-card-bio",
        "new": "group-card-new"
    }
    return classes.get(category, "group-card-stats")

def render_group_card(group):
    """Render a single group card with modern styling"""
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

def show_success_message(message):
    st.success(f"✅ {message}")

def show_warning_message(message):
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    st.info(f"ℹ️ {message}")

# --- Main App ---
def main():
    init_session_state()
    
    # Title
    st.markdown('<h1 class="main-title">WAITT</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">We\'re all in this together</p>', unsafe_allow_html=True)
    
    # Stats Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(st.session_state.groups)}</div>
            <div class="metric-label">Aktive Gruppen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_members = sum(len(group["members"]) for group in st.session_state.groups)
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_members}</div>
            <div class="metric-label">Lernende</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(st.session_state.joined_groups)}</div>
            <div class="metric-label">Deine Gruppen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(st.session_state.pinnwand_entries)}</div>
            <div class="metric-label">Pinnwand-Beiträge</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Gruppen finden", "➕ Gruppe erstellen", "👥 Meine Gruppen", "📌 Pinnwand"])
    
    # Tab 1: Find Groups
    with tab1:
        st.markdown("## Offene Lerngruppen")
        
        # Filter options
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Suche nach Thema", placeholder="z.B. Statistik, Psychologie...")
        with col2:
            show_full_only = st.checkbox("Nur Gruppen mit freien Plätzen")
        
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
                with st.container():
                    answer = st.text_area(
                        "Deine Antwort auf die Einstiegsfrage:",
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
                st.markdown("""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #dcfce7, #bbf7d0); 
                     border-radius: 10px; margin: 1rem 0; border: 1px solid #86efac;">
                    <strong style="color: #166534;">✅ Du bist bereits Mitglied dieser Gruppe</strong>
                </div>
                """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #fef3c7, #fde68a); 
                     border-radius: 10px; margin: 1rem 0; border: 1px solid #f59e0b;">
                    <strong style="color: #92400e;">⚠️ Gruppe ist bereits voll</strong>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 2rem 0; border: none; height: 1px; background: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Tab 2: Create Group
    with tab2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="form-title">Neue Lerngruppe erstellen</h2>', unsafe_allow_html=True)
        
        with st.form("create_group_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input("📚 Thema", placeholder="z.B. Statistik Klausur, Organische Chemie...")
                time_input = st.time_input("🕐 Uhrzeit", value=time(10, 0))
                room = st.selectbox("📍 Ort", [
                    "Raum A1", "Raum A2", "Raum B1", "Raum B2",
                    "Bibliothek Gruppenraum 1", "Bibliothek Gruppenraum 2",
                    "Café Campus", "Lernwiese", "Online (Zoom)", "Online (Teams)"
                ])
            
            with col2:
                max_members = st.slider("👥 Maximale Teilnehmerzahl", 2, 10, 4)
                icon = st.selectbox("🎯 Icon für die Gruppe", [
                    "📊", "🧠", "🔬", "📚", "💡", "🎯", "🧮", "🎨", "🌟", "⚡", "🚀", "💻"
                ])
                category = st.selectbox("📂 Kategorie", [
                    "stats", "psychology", "bio", "math", "physics", "chemistry", "other"
                ])
            
            question = st.text_area(
                "❓ Einstiegsfrage für neue Mitglieder",
                placeholder="Was möchtest du von deiner Lerngruppe wissen? z.B. 'Was ist deine größte Herausforderung bei diesem Thema?'",
                height=100
            )
            
            submitted = st.form_submit_button("🚀 Gruppe erstellen und beitreten", use_container_width=True)
            
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
                        "answers": {"Du": "(Gruppengründer - noch keine Antwort)"},
                        "icon": icon,
                        "category": category
                    }
                    
                    st.session_state.groups.append(new_group)
                    st.session_state.joined_groups.append(new_group["id"])
                    
                    show_success_message(f"Gruppe '{topic}' erfolgreich erstellt!")
                    st.balloons()
                    st.rerun()
                else:
                    show_warning_message("Bitte fülle alle Pflichtfelder aus.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 3: My Groups
    with tab3:
        st.markdown("## Deine Lerngruppen")
        
        my_groups = [g for g in st.session_state.groups if g["id"] in st.session_state.joined_groups]
        
        if not my_groups:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.1); 
                 border-radius: 20px; margin: 2rem 0; backdrop-filter: blur(10px);">
                <h3 style="color: white; margin-bottom: 1rem;">Du bist noch keiner Gruppe beigetreten</h3>
                <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 2rem;">
                    Entdecke spannende Lerngruppen oder erstelle deine eigene!
                </p>
            </div>
            """, unsafe_allow_html=True)
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
                    <div class="member-tags">
                """, unsafe_allow_html=True)
                
                for member in group["members"]:
                    st.markdown(f'<span class="member-tag">{member}</span>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show answers from all members
                if group["answers"]:
                    st.markdown('<h4 style="margin: 1.5rem 0 1rem 0; color: #374151;">Antworten der Mitglieder:</h4>', unsafe_allow_html=True)
                    for name, answer in group["answers"].items():
                        st.markdown(f"""
                        <div class="answer-item">
                            <div class="answer-author">{name}</div>
                            <div>"{answer}"</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Option to leave group
                if st.button(f"👋 Gruppe verlassen", key=f"leave_{group['id']}", use_container_width=True):
                    if "Du" in group["members"]:
                        group["members"].remove("Du")
                    if "Du" in group["answers"]:
                        del group["answers"]["Du"]
                    if group["id"] in st.session_state.joined_groups:
                        st.session_state.joined_groups.remove(group["id"])
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<hr style='margin: 2rem 0; border: none; height: 1px; background: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Tab 4: Pinnwand
    with tab4:
        st.markdown('<div class="pinnwand-container">', unsafe_allow_html=True)
        st.markdown(f'<h2 class="week-question">Frage der Woche: {st.session_state.current_question}</h2>', unsafe_allow_html=True)
        
        # Add new entry form
        with st.form("pinnwand_form"):
            new_entry = st.text_area(
                "Dein Beitrag:",
                placeholder="Was gibt dir gerade Energie beim Lernen?",
                height=100
            )
            
            if st.form_submit_button("📌 Auf Pinnwand posten", use_container_width=True):
                if new_entry.strip():
                    st.session_state.pinnwand_entries.append(new_entry.strip())
                    show_success_message("Dein Beitrag wurde zur Pinnwand hinzugefügt!")
                    st.rerun()
                else:
                    show_warning_message("Bitte schreibe etwas, bevor du postest.")
        
        st.markdown("<hr style='margin: 2rem 0; border: none; height: 2px; background: rgba(102, 126, 234, 0.3);'>", unsafe_allow_html=True)
        
        # Display all pinnwand entries
        st.markdown('<h3 style="margin-bottom: 2rem; color: #374151;">Antworten der Community:</h3>', unsafe_allow_html=True)
        
        for i, entry in enumerate(st.session_state.pinnwand_entries):
            st.markdown(f"""
            <div class="postit">
                <p style="margin: 0; font-size: 1rem; line-height: 1.5; color: #374151;">
                    "{entry}"
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Admin section to change question (hidden in expandier)
        with st.expander("🔧 Admin: Frage der Woche ändern"):
            new_question = st.text_input(
                "Neue Frage:",
                value=st.session_state.current_question,
                placeholder="Neue inspirierende Frage eingeben..."
            )
            
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

if __name__ == "__main__":
    main()
