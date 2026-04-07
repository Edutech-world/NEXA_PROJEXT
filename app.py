import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from PIL import Image

# --- CONFIGURATION GOOGLE ---
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEXA PRO", layout="wide")

# --- SYSTÈME DE CONTRÔLE (LOGIN) ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌐 Bienvenue sur NEXA</h1>", unsafe_allow_html=True)
    st.write("---")
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.subheader("Connexion requise")
        email_input = st.text_input("Entre ton adresse email pour accéder au service :")
        if st.button("Se connecter à NEXA"):
            if "@" in email_input: # Vérification simple de l'email
                st.session_state.user_email = email_input
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Veuillez entrer un email valide.")
    st.stop() # Bloque le reste de l'app tant qu'on n'est pas connecté

# --- INITIALISATION PRO ---
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# --- FONCTION VOIX ---
def parler(texte):
    try:
        tts = gTTS(text=texte[:300], lang='fr')
        tts.save("nexa_voice.mp3")
        with open("nexa_voice.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        os.remove("nexa_voice.mp3")
    except: pass

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("NEXA 🚀")
    st.write(f"👤 Connecté : *{st.session_state.user_email}*")
    st.divider()
    
    # Section Paiement
    if not st.session_state.is_pro:
        st.subheader("💰 Activer NEXA PRO+")
        st.write("Envoyez *250 HTG* :")
        st.info("📲 MonCash : +509 4769-2489\n📲 Natcash : +509 4208-7977")
        code = st.text_input("Code secret (234)", type="password")
        if code == "234":
            st.session_state.is_pro = True
            st.rerun()
    else:
        st.success("MODE PRO+ ACTIF ✅")

    st.divider()
    # Zone Admin (Pour toi, Alejandro)
    admin_code = st.text_input("⚙️ Espace PDG (1234)", type="password")
    if admin_code == "1234":
        st.warning("LISTE DES UTILISATEURS")
        # Ici, l'email de la personne actuelle s'affiche pour que tu puisses le noter
        st.write(f"Utilisateur en ligne : {st.session_state.user_email}")

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align: center; color: #4285F4;'>NEXA AI</h1>", unsafe_allow_html=True)

# Caméra (A gauche) et Micro (A droite) simulés
if st.session_state.is_pro:
    st.subheader("📸 Caméra & Vision")
    photo = st.camera_input("Scanner un document")
    if photo:
        img = Image.open(photo)
        res = model.generate_content(["Analyse cette image", img])
        st.write(res.text)
        parler(res.text)
else:
    st.warning("🔒 Débloquez le mode PRO+ pour utiliser la caméra et la voix.")

# Zone de Chat
if prompt := st.chat_input("Pose ta question..."):
    st.chat_message("user").write(prompt)
    response = model.generate_content(prompt)
    st.chat_message("assistant").write(response.text)
    parler(response.text)
