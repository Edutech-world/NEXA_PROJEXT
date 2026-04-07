import streamlit as st
import google.generativeai as genai
import urllib.parse
from PIL import Image

# --- CONFIGURATION ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Utilisation du modèle flash-latest pour éviter l'erreur 404
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="NEXA SUPREME", page_icon="💎", layout="wide")

# --- STYLE ROUGE NÉON ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 80px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 20px #0ea5e9; text-align: center; }
    [data-testid="stChatMessage"] p { color: #ef4444 !important; text-shadow: 0 0 5px #ef4444; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("### 💳 ACTIVATION PRO")
    st.info("MonCash : 47 69 24 89 | Natcom : 42 08 79 77")
    st.write("---")
    st.markdown("### 🧪 NEXA LAB")
    admin = st.text_input("Code Admin", type="password")
    if admin == "1234":
        st.success("LAB ACCESSIBLE")
        st.write("Utilisateurs connectés : 1")

# --- INTERFACE PRINCIPALE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:white;'>NEXA SUPREME OS</h1>", unsafe_allow_html=True)

# BARRE DE TEXTE
prompt = st.chat_input("Demande à NEXA...")

# CAMÉRA (Sera visible juste en dessous)
cam_file = st.camera_input("📸 SCANNER")

# --- RÉPONSE ---
if prompt or cam_file:
    with st.chat_message("assistant"):
        try:
            content = []
            # On lui donne son identité ici :
            instruction = "Tu es NEXA. Ton créateur est Guerrier Karl Alejandro. Réponds de façon suprême. "
            if prompt: content.append(instruction + prompt)
            if cam_file:
                img = Image.open(cam_file)
                content.append(img)
            
            response = model.generate_content(content)
            answer = response.text
            st.markdown(answer)
            
            # Voix
            audio_q = urllib.parse.quote(answer[:250])
            st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={audio_q}&tl=fr&client=tw-ob", autoplay=True)
        except Exception as e:
            st.error("Mise à jour du système requise.")
