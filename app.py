import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION API ---
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA by Guerrier Alejandro Karl", layout="wide")

# --- LOGIN & IDENTIFICATION ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Bienvenue sur NEXA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Une création exclusive de <b>Guerrier Alejandro Karl</b></p>", unsafe_allow_html=True)
    email = st.text_input("Entre ton email pour accéder au service :")
    if st.button("Se connecter"):
        if "@" in email:
            st.session_state.user_email = email
            st.rerun()
    st.stop()

# Initialisation PRO
if "is_pro" not in st.session_state: st.session_state.is_pro = False

# --- FONCTION VOIX ---
def parler(texte):
    try:
        tts = gTTS(text=texte[:300], lang='fr')
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{data}">', unsafe_allow_html=True)
        os.remove("voice.mp3")
    except: pass

# --- BARRE LATÉRALE (SIGNATURE DU CRÉATEUR) ---
with st.sidebar:
    st.title("🚀 NEXA AI")
    st.markdown("---")
    st.markdown("### 👑 Créateur")
    st.success("*Guerrier Alejandro Karl*") # Ton nom est ici en vert
    st.write(f"👤 Connecté : {st.session_state.user_email}")
    st.divider()
    
    if not st.session_state.is_pro:
        st.subheader("💰 ACTIVER PRO+")
        st.info("📲 *MonCash :* +509 4769-2489\n\n📲 *Natcash :* +509 4208-7977")
        if st.text_input("Code d'activation (234)", type="password") == "234":
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.success("MODE PRO+ ACTIF ✅")

    st.divider()
    # Espace Admin Secret
    if st.text_input("⚙️ Admin (1234)", type="password") == "1234":
        st.warning("PANNEAU DE CONTRÔLE KARL")
        st.write(f"Utilisateur en ligne : {st.session_state.user_email}")

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align: center; color: #4285F4;'>NEXA AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Propulsé par l'intelligence artificielle — Développé par Guerrier Alejandro Karl</p>", unsafe_allow_html=True)

# Zone Caméra Pro
if st.session_state.is_pro:
    photo = st.camera_input("Scanner un document ou un exercice")
    if photo:
        img = Image.open(photo)
        res = model.generate_content(["Analyse cette image et explique en détail", img])
        st.write(res.text)
        parler(res.text)
else:
    st.warning("🔒 Activez le mode PRO+ dans le menu latéral pour débloquer la caméra.")

# Chat principal
if p := st.chat_input("Pose ta question à NEXA..."):
    st.chat_message("user").write(p)
    response = model.generate_content(p)
    st.chat_message("assistant").write(response.text)
    parler(response.text)
