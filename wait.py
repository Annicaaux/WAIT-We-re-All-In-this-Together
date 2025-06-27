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
        background: linear-gradient(135deg, #A0616A 0%, #6B2C3A 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
        background: linear-gradient(135deg, #8B5A6B, #6B2C3A) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 90, 107, 0.4);
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
        color: #374151;
    }
    
    .group-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .group-card-stats {
        border-top-color: #A0616A;
    }
    
    .group-card-psychology {
        border-top-color: #C4626D;
    }
    
    .group-card-bio {
        border-top-color: #B85450;
    }
    
    .group-card-new {
        border-top-color: #8B5A6B;
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
        background: linear-gradient(135deg, #A0616A, #6B2C3A);
        color: white;
        box-shadow: 0 4px 15px rgba(160, 97, 106, 0.3);
    }
    
    .group-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2937 !important;
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
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border-left: 4px solid #BE185D;
    }
    
    .question-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #831843;
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
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: #831843;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #F9A8D4;
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
        color: #374151;
    }
    
    .form-title {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 2rem;
    }
    
    /* My groups styling */
    .my-group-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 5px solid #A0616A;
        backdrop-filter: blur(20px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        color: #374151;
    }
    
    .member-tag {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: #831843;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #F9A8D4;
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
        color: #374151;
    }
    
    .week-question {
        font-size: 1.5rem;
        font-weight: 600;
        color: #831843;
        margin-bottom: 2rem;
        line-height: 1.4;
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #F9A8D4;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #A0616A, #6B2C3A);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(160, 97, 106, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(160, 97, 106, 0.6);
        background: linear-gradient(135deg, #8B5A6B, #5A1F2A);
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
        border-color: #A0616A;
        box-shadow: 0 0 0 3px rgba(160, 97, 106, 0.1);
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
    
    /* Text color fixes */
    .stForm {
        color: #374151 !important;
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
    
    if "pause_statistics" not in st.session_state:
        st.session_state.pause_statistics = {
            "solo_pausen": 0,
            "gruppen_pausen": 0,
            "total_time": 0
        }

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
        total_pauses = st.session_state.pause_statistics["solo_pausen"] + st.session_state.pause_statistics["gruppen_pausen"]
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_pauses}</div>
            <div class="metric-label">Pausen genommen</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Gruppen finden", "➕ Gruppe erstellen", "👥 Meine Gruppen", "📌 Pinnwand", "🌿 Lernpausen"])
    
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
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;">
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
        # Header Section
        st.markdown(f"""
        <div class="pinnwand-container">
            <h2 class="week-question">Frage der Woche: {st.session_state.current_question}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Add new entry form
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        with st.form("pinnwand_form"):
            new_entry = st.text_area(
                "💭 Dein Beitrag:",
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
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display all pinnwand entries
        st.markdown("### 💫 Antworten der Community")
        
        if st.session_state.pinnwand_entries:
            # Create columns for better layout
            num_entries = len(st.session_state.pinnwand_entries)
            cols_per_row = 2
            
            for i in range(0, num_entries, cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    entry_idx = i + j
                    if entry_idx < num_entries:
                        entry = st.session_state.pinnwand_entries[entry_idx]
                        with col:
                            # Determine post-it style based on index
                            if entry_idx % 3 == 0:
                                bg_color = "#fef3c7"
                                border_color = "#f59e0b"
                                rotation = "-1deg"
                            elif entry_idx % 3 == 1:
                                bg_color = "#dcfce7"
                                border_color = "#10b981"
                                rotation = "1deg"
                            else:
                                bg_color = "#fce7f3"
                                border_color = "#ec4899"
                                rotation = "-0.5deg"
                            
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
                                transition: all 0.3s ease;
                                min-height: 120px;
                                display: flex;
                                align-items: center;
                            ">
                                <div style="
                                    position: absolute;
                                    top: -10px;
                                    right: 15px;
                                    font-size: 1.2rem;
                                ">📌</div>
                                <p style="
                                    margin: 0; 
                                    font-size: 1rem; 
                                    line-height: 1.5; 
                                    color: #374151;
                                    font-style: italic;
                                ">"{entry}"</p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.1); 
                 border-radius: 20px; margin: 2rem 0; backdrop-filter: blur(10px);">
                <h3 style="color: white; margin-bottom: 1rem;">Noch keine Beiträge</h3>
                <p style="color: rgba(255, 255, 255, 0.8);">
                    Sei der Erste und teile deine Motivation!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Admin section to change question (hidden in expander)
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
    
    # Tab 5: Lernpausen
    with tab5:
        st.markdown("# 🌿 Gesunde Lernpausen")
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; backdrop-filter: blur(10px);">
            <p style="color: white; margin: 0; font-size: 1.1rem; text-align: center; line-height: 1.6;">
                <strong>Pausen sind kein Luxus - sie sind essentiell!</strong><br>
                Hier findest du Aktivitäten für erholsame Pausen allein oder in der Gruppe. 
                Kleine Auszeiten stärken deine Konzentration, dein Wohlbefinden und deine sozialen Verbindungen.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pause Statistics
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
                <div class="metric-value">{st.session_state.pause_statistics["gruppen_pausen"]}</div>
                <div class="metric-label">Gruppen-Pausen</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["total_time"]}</div>
                <div class="metric-label">Minuten Pause</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">💚</div>
                <div class="metric-label">Für dich gesorgt</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Simple pause activities
        st.markdown("### 🎯 Schnelle Pausenideen")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🧘 Solo-Pausen")
            if st.button("🌬️ 5-Min Atemübung starten", use_container_width=True):
                st.markdown("""
                <div class="form-container">
                    <h4 style="color: #831843;">🌬️ Entspannte Atmung</h4>
                    <p style="color: #6B7280;">Setze dich bequem hin und folge diesem Rhythmus:</p>
                    <ul style="color: #374151;">
                        <li>4 Sekunden einatmen</li>
                        <li>4 Sekunden anhalten</li>
                        <li>6 Sekunden ausatmen</li>
                        <li>Wiederhole das 10 Mal</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                if st.button("✅ Atemübung gemacht!", key="breath_done"):
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.pause_statistics["total_time"] += 5
                    show_success_message("Super! 5 Minuten für deine Entspannung. 💚")
                    st.balloons()
            
            if st.button("🚶 Zimmer-Spaziergang", use_container_width=True):
                st.markdown("""
                <div class="form-container">
                    <h4 style="color: #831843;">🚶 Sanfte Bewegung</h4>
                    <p style="color: #374151;">
                        Stehe auf und gehe langsam durch dein Zuhause. 
                        Strecke dich, räume 2-3 Dinge auf, öffne ein Fenster für frische Luft.
                        Nimm bewusst deine Umgebung wahr.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("✅ Spaziergang gemacht!", key="walk_done"):
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.pause_statistics["total_time"] += 10
                    show_success_message("Toll! Bewegung tut gut. 💚")
                    st.balloons()
        
        with col2:
            st.markdown("#### 👥 Gruppen-Pausen")
            
            my_groups = [g for g in st.session_state.groups if g["id"] in st.session_state.joined_groups]
            if my_groups:
                if st.button("🌿 Gemeinsamer Spaziergang planen", use_container_width=True):
                    st.markdown("""
                    <div class="form-container">
                        <h4 style="color: #831843;">🌿 Frische Luft & Gespräche</h4>
                        <p style="color: #374151;">
                            Plant einen 20-30 minütigen Spaziergang mit eurer Lerngruppe.
                            <strong>Regel:</strong> Die ersten 10 Minuten wird nicht über die Uni geredet!
                        </p>
                        <p style="color: #6B7280; font-style: italic;">
                            Schreibt in eure Gruppenchats und verabredet euch!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("✅ Spaziergang gemacht!", key="group_walk_done"):
                        st.session_state.pause_statistics["gruppen_pausen"] += 1
                        st.session_state.pause_statistics["total_time"] += 25
                        show_success_message("Fantastisch! Gemeinsame Zeit stärkt euch alle. 🤝💚")
                        st.balloons()
                
                if st.button("☕ Mini-Café Pause", use_container_width=True):
                    st.markdown("""
                    <div class="form-container">
                        <h4 style="color: #831843;">☕ Entspannte Café-Zeit</h4>
                        <p style="color: #374151;">
                            Holt euch Getränke und setzt euch gemütlich zusammen.
                            Redet über alles außer Uni: Hobbys, Träume, lustige Erlebnisse.
                        </p>
                        <p style="color: #6B7280; font-style: italic;">
                            25 Minuten bewusste Auszeit vom Lernstress.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("✅ Café-Pause gemacht!", key="cafe_done"):
                        st.session_state.pause_statistics["gruppen_pausen"] += 1
                        st.session_state.pause_statistics["total_time"] += 25
                        show_success_message("Wunderbar! Soziale Verbindungen sind so wichtig. 💚")
                        st.balloons()
            else:
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; backdrop-filter: blur(10px);">
                    <p style="color: white; margin: 0; text-align: center;">
                        Tritt erst einer Lerngruppe bei, um Gruppen-Pausen zu planen!
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Wellness Tips
        st.markdown("---")
        st.markdown("### 💡 Tipps für gesunde Lerngewohnheiten")
        
        wellness_tips = [
            "🕐 **25-5 Regel**: Nach 25 Minuten Lernen immer 5 Minuten Pause",
            "🚶 **Bewegung**: Mindestens alle 2 Stunden aufstehen und sich bewegen",
            "💧 **Hydration**: Regelmäßig Wasser trinken - dehydrierte Gehirne lernen schlechter",
            "👥 **Soziale Kontakte**: Isolation vermeiden - regelmäßig mit anderen sprechen",
            "😴 **Schlaf**: 7-8 Stunden Schlaf sind wichtiger als eine Nacht durchlernen",
            "🍎 **Ernährung**: Gesunde Snacks statt Zucker - für konstante Energie"
        ]
        
        for tip in wellness_tips:
            st.markdown(f"- {tip}")
        
        # Emergency support
        st.markdown("---")
        st.markdown("### 🆘 Wenn du merkst, dass du überlastet bist")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FDF2F8, #FCE7F3); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #BE185D;">
            <p style="color: #374151; margin: 0; line-height: 1.6;">
                <strong style="color: #831843;">Du bist nicht allein!</strong><br>
                Wenn Lernen zur Belastung wird, Einsamkeit überhandnimmt oder du dich erschöpft fühlst:<br>
                📞 <strong>Studierendenberatung</strong> - kostenlos und vertraulich<br>
                💬 <strong>Psychologische Beratung</strong> - auch online verfügbar<br>
                🤝 <strong>Kommilitonen</strong> - nutze die Lerngruppen für mehr als nur das Studium
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
