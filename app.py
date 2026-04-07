import streamlit as st
from groq import Groq
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION DES CLÉS (MIS À JOUR) ---
# Ta nouvelle clé Groq est maintenant active dans le code
GROQ_API_KEY = "Gsk_LnsmjxnXqydFPDbeiPHzWGdyb3FY393FRsK6lFtTkwj3RtrRFwOw"

# On garde Gemini pour la vision car Groq ne traite pas les images
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")

client = Groq(api_key=GROQ_API_KEY)
model_vision = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA by Guerrier Alejandro Karl", layout="wide")

# --- SYSTÈME DE CONNEXION (LOGIN) ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Connexion NEXA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Une création exclusive de <b>Guerrier Alejandro Karl</b></p>", unsafe_allow_html=True)
    email = st.text_input("Entre ton email pour accéder au service :")
    if st.button("Se connecter"):
        if "@" in email:
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Veuillez entrer un email valide.")
    st.stop()

# Initialisation de l'état PRO
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

# --- BARRE LATÉRALE (NUMÉROS & CRÉDITS) ---
with st.sidebar:
    st.title("🚀 NEXA AI")
    st.success(f"👑 Créateur : *Guerrier Alejandro Karl*")
    st.write(f"👤 Compte : {st.session_state.user_email}")
    st.divider()
    
    if not st.session_state.is_pro:
        st.subheader("💰 ACTIVER MODE PRO+")
        st.write("Accès Caméra + Voix (250 HTG)")
        
        # TES NUMÉROS POUR LE PAIEMENT
        st.info("📲 *MonCash* : +509 4769-2489")
        st.info("📲 *Natcash* : +509 4208-7977")
        
        code = st.text_input("Entre le code d'activation (234)", type="password")
        if code == "234":
            st.session_state.is_pro = True
            st.success("MODE PRO+ ACTIVÉ ✅")
            st.rerun()
    else:
        st.success("✅ MODE PRO+ ACTIF")

    st.divider()
    # Espace Admin pour Karl
    if st.text_input("⚙️ Admin (1234)", type="password") == "1234":
        st.warning("PANNEAU PDG")
        st.write(f"Utilisateur actif : {st.session_state.user_email}")

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align: center; color: #4285F4;'>NEXA AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Propulsé par Llama 3 & Gemini — Développé par Guerrier Alejandro Karl</p>", unsafe_allow_html=True)

# Zone Caméra (Seulement pour Pro)
if st.session_state.is_pro:
    st.subheader("📸 Vision & Analyse")
    photo = st.camera_input("Scanner un document ou un exercice")
    if photo:
        img = Image.open(photo)
        with st.spinner("Analyse de l'image par NEXA..."):
            res = model_vision.generate_content(["Explique cette image en détail", img])
            st.write(res.text)
            parler(res.text)
else:
    st.warning("🔒 Le mode PRO+ est requis pour utiliser la caméra et la voix.")

# Zone de Chat (Utilise Groq)
if p := st.chat_input("Pose ta question à NEXA..."):
    st.chat_message("user").write(p)
    try:
        # Utilisation de Llama 3 via ta nouvelle clé Groq
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": p}],
            model="llama-3.3-70b-versatile",
        )
        response_text = chat_completion.choices[0].message.content
        st.chat_message("assistant").write(response_text)
        parler(response_text)
    except Exception as e:
        st.error("Erreur technique. Vérifie que ta clé API est bien copiée.")
