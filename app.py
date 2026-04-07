import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION GEMINI ---
# Ta clé API Google (Invisible dans l'interface)
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA SUPRÊME", layout="wide")

# --- SYSTÈME DE CONTRÔLE UTILISATEUR ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Bienvenue sur NEXA</h1>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        email = st.text_input("Veuillez entrer votre email pour continuer :")
        if st.button("Se connecter"):
            if "@" in email:
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Email invalide.")
    st.stop()

# --- INITIALISATION ---
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# --- FONCTION VOIX ---
def parler(texte):
    try:
        tts = gTTS(text=texte[:300], lang='fr')
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
            b64 = base64.base64encode(data).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        os.remove("voice.mp3")
    except: pass

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("NEXA 🚀")
    st.write(f"👤 Utilisateur : *{st.session_state.user_email}*")
    st.divider()
    
    if not st.session_state.is_pro:
        st.subheader("💰 ACTIVER PRO+")
        st.write("Accès illimité pour 250 HTG")
        st.info("📲 MonCash : +509 4769-2489\n\n📲 Natcash : +509 4208-7977")
        if st.text_input("Code d'activation (234)", type="password") == "234":
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.success("MODE PRO+ ACTIF ✅")

    st.divider()
    # Espace Admin pour Karl
    if st.text_input("⚙️ Admin (1234)", type="password") == "1234":
        st.warning("PANNEAU DE CONTRÔLE")
        st.write(f"En ligne : {st.session_state.user_email}")

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align: center; color: #4285F4;'>NEXA AI</h1>", unsafe_allow_html=True)

# Caméra (Seulement pour les membres Pro)
if st.session_state.is_pro:
    st.subheader("📸 Caméra de Vision")
    photo = st.camera_input("Scanner un document")
    if photo:
        img = Image.open(photo)
        with st.spinner("Analyse en cours..."):
            res = model.generate_content(["Analyse cette image", img])
            st.write(res.text)
            parler(res.text)
else:
    st.warning("🔒 Activez le mode PRO+ pour débloquer la caméra et la voix.")

# Zone de Tchat
if p := st.chat_input("Posez votre question à NEXA..."):
    st.chat_message("user").write(p)
    response = model.generate_content(p)
    st.chat_message("assistant").write(response.text)
    parler(response.text)
