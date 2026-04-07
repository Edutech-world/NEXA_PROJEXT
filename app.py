import streamlit as st
import google.generativeai as genai
import urllib.parse
from PIL import Image

# --- CONFIGURATION CERVEAU ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="NEXA SUPREME", page_icon="💎", layout="wide")

# --- DESIGN CSS (Interface Alignée + Filigrane) ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 60px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 20px #0ea5e9; text-align: center; }
    
    /* Réponses en rouge néon */
    [data-testid="stChatMessage"] p { color: #ef4444 !important; text-shadow: 0 0 5px #ef4444; }

    /* --- FILIGRANE N SUR IMAGE --- */
    .image-container { position: relative; display: inline-block; width: 100%; border-radius: 15px; overflow: hidden; }
    .watermark {
        position: absolute; bottom: 15px; right: 15px;
        color: #0ea5e9; font-size: 40px; font-weight: 900;
        text-shadow: 0 0 15px #0ea5e9; background: rgba(2, 6, 23, 0.4);
        padding: 5px 15px; border-radius: 10px; pointer-events: none;
    }
    
    /* Cacher les labels inutiles pour gagner de la place */
    label { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
if "users_list" not in st.session_state:
    st.session_state.users_list = []

# --- BARRE LATÉRALE (EMAIL & LAB) ---
with st.sidebar:
    st.markdown('<div class="n-logo" style="font-size:30px;">N</div>', unsafe_allow_html=True)
    st.markdown("### 👤 CONNEXION")
    email_user = st.text_input("Email", placeholder="votre@email.com")
    if