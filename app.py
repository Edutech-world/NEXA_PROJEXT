import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION (FINI GROQ, BIENVENUE GEMINI) ---
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA AI", layout="wide")

# --- LOGIN OBLIGATOIRE ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Connexion NEXA</h1>", unsafe_allow_html=True)
    email_input = st.text_input("Entre ton email pour continuer :")
    if st.button("Se connecter"):
        if "@" in email_input:
            st.session_state.user_email = email_input
            st.rerun()
    st.stop()

# Initialisation
if "is_pro" not in st.session_state: st.session_state.is_pro = False

# --- BARRE LATÉRALE (TES NUMÉROS ICI) ---
with st.sidebar:
    st.title("NEXA 🚀")
    st.write(f"👤 {st.session_state.user_email}")
    st.divider()
    
    if not st.session_state.is_pro:
        st.subheader("💰 ACTIVER NEXA PRO+")
        st.write("Envoie 250 HTG pour débloquer la caméra :")
        # TES NUMÉROS SONT ICI
        st.info("📲 MonCash : +509 4769-2489")
        st.info("📲 Natcash : +509 4208-7977")
        
        if st.text_input("Code (234)", type="password") == "234":
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.success("MODE PRO+ ACTIF ✅")

# --- INTERFACE DE CHAT ---
st.markdown("<h1 style='text-align: center; color: #4285F4;'>NEXA AI</h1>", unsafe_allow_html=True)

if st.session_state.is_pro:
    photo = st.camera_input("Scanner un exercice")
    if photo:
        img = Image.open(photo)
        res = model.generate_content(["Analyse cette image", img])
        st.write(res.text)

# Chat Box
if p := st.chat_input("Pose ta question..."):
    st.chat_message("user").write(p)
    response = model.generate_content(p)
    st.chat_message("assistant").write(response.text)
    
    # Voix automatique
    tts = gTTS(text=response.text[:300], lang='fr')
    tts.save("v.mp3")
    with open("v.mp3", "rb") as f:
        data = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{data}">', unsafe_allow_html=True)
    os.remove("v.mp3")
