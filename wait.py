import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="StudyTogether", layout="wide")

# Farben und Schriftart global setzen
st.markdown("""
    <style>
        html, body, [class*="st"] {
            background-color: #f5f0e6;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: #2f2f2f;
        }
        .toggle-button {
            background: linear-gradient(135deg, #f48fb1, #ce93d8);
            color: #fff;
            font-weight: bold;
            padding: 0.8rem 1.2rem;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.15);
            width: 100%;
            text-align: left;
            font-size: 1.1rem;
            transition: all 0.2s ease-in-out;
        }
        .toggle-button:hover {
            background: linear-gradient(135deg, #ec407a, #ab47bc);
        }
        .toggle-content {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin-top: 0.5rem;
        }
        .postit {
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Patrick Hand', 'Comic Sans MS', cursive;
            text-align: center;
            padding: 1rem;
            margin: 0.5rem;
            width: 160px;
            height: 160px;
            border: 1px solid #e0d97a;
            border-radius: 4px;
            box-shadow: 4px 4px 10px rgba(0,0,0,0.15);
            transform: rotate(-2deg);
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📚 StudyTogether – Finde deine Lerngruppe")

# Tabs einrichten mit Icons
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Lerngruppen finden",
    "🛠️ Gruppe erstellen",
    "👥 Meine Gruppen",
    "📌 Pinnwand"
])
