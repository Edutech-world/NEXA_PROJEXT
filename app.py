import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION (REMPLACE LLAMA PAR GEMINI) ---
# On utilise ta clé Google Gemini ici
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA AI", layout="wide")

# --- LOGIN & CONTRÔLE ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Connexion NEXA</h1>", unsafe_allow_html=True)
    email = st.text_input("Entre ton email :")
    if st.button("Accéder"):
        if "@" in email:
            st.session_state.user_email = email
            st.rerun()
    st.stop()

# --- SIDEBAR (TES NUMÉROS ICI) ---
with st.sidebar:
    st.title("NEXA PRO 🚀")
    st.write(f"Email: {st.session_state.user_email}")
    st.divider()
    
    if not st.session_state.get("is_pro", False):
        st.subheader("💰 PAIEMENT ACTIVATION")
        # Voici tes numéros bien visibles
        st.info("📲 *MonCash* : +509 4769-2489")
        st.info("📲 *Natcash* : +509 4208-7977")
        
        code = st.text_input("Code (234)", type="password")
        if code == "234":
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.success("MODE PRO+ ACTIF ✅")

# --- CHAT & VISION ---
st.markdown("<h1 style='text-align: center;'>NEXA AI</h1>", unsafe_allow_html=True)

if st.session_state.get("is_pro", False):
    # Caméra uniquement en mode Pro
    img_file = st.camera_input("Scanner un exercice")
    if img_file:
        img = Image.open(img_file)
        response = model.generate_content(["Analyse cette image", img])
        st.write(response.text)

# Zone de texte
prompt = st.chat_input("Pose ta question...")
if prompt:
    st.chat_message("user").write(prompt)
    response = model.generate_content(prompt)
    st.chat_message("assistant").write(response.text)
    
    # Voix automatique
    tts = gTTS(text=response.text[:300], lang='fr')
    tts.save("v.mp3")
    with open("v.mp3", "rb") as f:
        data = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{data}">', unsafe_allow_html=True)
    os.remove("v.mp3")
