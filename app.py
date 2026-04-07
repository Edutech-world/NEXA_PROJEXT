import streamlit as st
from groq import Groq
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION DES CLÉS (AVEC TA NOUVELLE CLÉ GSK) ---
GROQ_API_KEY = "Gsk_LnsmjxnXqydFPDbeiPHzWGdyb3FY393FRsK6lFtTkwj3RtrRFwOw"
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")

client = Groq(api_key=GROQ_API_KEY)
model_vision = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA by Guerrier Alejandro Karl", layout="wide")

# --- SYSTÈME DE CONNEXION ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Accès NEXA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Créé par <b>Guerrier Alejandro Karl</b></p>", unsafe_allow_html=True)
    email = st.text_input("Entre ton email :")
    if st.button("Se connecter"):
        if "@" in email:
            st.session_state.user_email = email
            st.rerun()
    st.stop()

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

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("🚀 NEXA AI")
    st.success(f"👑 Créateur : *Guerrier Alejandro Karl*")
    st.divider()
    
    if not st.session_state.is_pro:
        st.subheader("💰 ACTIVER MODE PRO+")
        st.info("📲 *MonCash* : +509 4769-2489\n\n📲 *Natcash* : +509 4208-7977")
        if st.text_input("Code d'activation (234)", type="password") == "234":
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.success("✅ MODE PRO+ ACTIF")

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align: center;'>NEXA AI</h1>", unsafe_allow_html=True)

# Caméra (Vision via Gemini car Groq ne voit pas les photos)
if st.session_state.is_pro:
    photo = st.camera_input("Scanner un document")
    if photo:
        img = Image.open(photo)
        res = model_vision.generate_content(["Explique cette image", img])
        st.write(res.text)
        parler(res.text)

# Chat (Texte via Groq Llama 3)
if p := st.chat_input("Pose ta question..."):
    st.chat_message("user").write(p)
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": p}],
            model="llama-3.3-70b-versatile",
        )
        response_text = chat_completion.choices[0].message.content
        st.chat_message("assistant").write(response_text)
        parler(response_text)
    except Exception as e:
        st.error("Ta clé Groq est encore rejetée. Vérifie-la sur console.groq.com")
