import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION GOOGLE GEMINI ---
# On utilise uniquement ta clé Google. Plus de Groq = Plus d'erreur rouge !
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA AI", page_icon="🚀", layout="wide")

# --- SYSTÈME DE CONNEXION ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Bienvenue sur NEXA</h1>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        email = st.text_input("Entre ton email pour commencer :")
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
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        os.remove("voice.mp3")
    except: pass

# --- BARRE LATÉRALE (Où sont tes numéros) ---
with st.sidebar:
    st.markdown("## 🚀 NEXA PRO+")
    st.write(f"Utilisateur : *{st.session_state.user_email}*")
    st.divider()
    
    if not st.session_state.is_pro:
        st.error("💎 OPTIONS PRO+ VERROUILLÉES")
        st.write("### 💳 PAIEMENT (250 HTG)")
        
        # Tes numéros sont ici !
        st.info("📲 *MonCash :\n+509 4769-2489*")
        st.info("📲 *Natcash :\n+509 4208-7977*")
        
        st.write("---")
        code = st.text_input("Entre le code d'activation (234)", type="password")
        if code == "234":
            st.session_state.is_pro = True
            st.success("Mode PRO+ activé !")
            st.rerun()
    else:
        st.success("✅ MODE PRO+ ACTIVÉ")
        st.write("Accès illimité à la Caméra et à la Voix.")

    st.divider()
    # Espace Admin pour toi Karl
    if st.text_input("⚙️ Admin (1234)", type="password") == "1234":
        st.warning("PANNEAU PDG KARL")
        st.write(f"Client actuel : {st.session_state.user_email}")

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align: center; color: #4285F4;'>NEXA AI</h1>", unsafe_allow_html=True)

# Zone Caméra pour les membres Pro
if st.session_state.is_pro:
    st.subheader("📸 Vision Artificielle")
    photo = st.camera_input("Prendre une photo pour analyse")
    if photo:
        img = Image.open(photo)
        with st.spinner("NEXA analyse..."):
            res = model.generate_content(["Analyse cette image", img])
            st.write(res.text)
            parler(res.text)
else:
    st.warning("🔒 Activez le mode PRO+ dans le menu de gauche pour utiliser la caméra.")

# Chat Classique
if p := st.chat_input("Pose ta question ici..."):
    st.chat_message("user").write(p)
    response = model.generate_content(p)
    st.chat_message("assistant").write(response.text)
    parler(response.text)
