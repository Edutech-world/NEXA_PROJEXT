import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION ---
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA AI", layout="wide")

# --- SYSTÈME DE CONNEXION SIMPLE ---
if "user_name" not in st.session_state:
    st.markdown("# 🌐 Bienvenue sur NEXA")
    name = st.text_input("Entre ton nom ou email pour commencer :")
    if st.button("Se connecter"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- INITIALISATION PRO ---
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# --- FONCTION VOIX ---
def parler(texte):
    try:
        tts = gTTS(text=texte[:300], lang='fr')
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        os.remove("voice.mp3")
    except: pass

# --- SIDEBAR (ADMIN & PAIEMENT) ---
with st.sidebar:
    st.title("NEXA 🚀")
    st.write(f"👤 Utilisateur : *{st.session_state.user_name}*")
    st.divider()
    
    if not st.session_state.is_pro:
        st.subheader("💎 NEXA PRO+")
        st.write("Pour débloquer la *Caméra* et la *Voix* :")
        st.info("📲 MonCash : +509 4769-2489\n\n📲 Natcash : +509 4208-7977")
        code = st.text_input("Code d'activation (234)", type="password")
        if code == "234":
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.success("MODE PRO+ ACTIVÉ ✅")

    st.divider()
    admin = st.text_input("⚙️ Admin (1234)", type="password")
    if admin == "1234":
        st.warning("PANNEAU PDG KARL")
        st.write(f"Utilisateur actuel : {st.session_state.user_name}")

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align: center;'>NEXA AI</h1>", unsafe_allow_html=True)

# CAMÉRA (Affiche le logo uniquement si PRO+)
if st.session_state.is_pro:
    st.subheader("📸 Vision & Caméra")
    photo = st.camera_input("Scanner un document")
    if photo:
        img = Image.open(photo)
        response = model.generate_content(["Analyse cette image", img])
        st.write(response.text)
        parler(response.text)
else:
    st.warning("🔒 Activez le mode PRO+ pour voir la Caméra.")

# CHAT
if prompt := st.chat_input("Dis quelque chose..."):
    st.chat_message("user").write(prompt)
    response = model.generate_content(prompt)
    st.chat_message("assistant").write(response.text)
    parler(response.text)
