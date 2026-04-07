import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from streamlit_google_auth import Authenticate

# --- CONFIGURATION API ---
genai.configure(api_key="AIzaSyDaEaSpHAIMA6ROD8FpS59DsCVpBVnorxo")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- CONFIGURATION AUTHENTIFICATION GOOGLE ---
# Note : Pour que cela fonctionne en production, tu dois créer un Client ID sur Google Cloud Console
auth = Authenticate(
    secret_token="NEXA_SECRET_TOKEN",
    cookie_name="nexa_auth",
    key="nexa_key",
    cookie_expiry_days=30,
)

st.set_page_config(page_title="NEXA SUPRÊME", layout="wide")

# --- VÉRIFICATION DE CONNEXION ---
auth.check_authentification()

# Si l'utilisateur n'est pas connecté, on affiche le bouton Google
if not st.session_state.get('connected', False):
    st.markdown("<h1 style='text-align:center;'>Bienvenue sur NEXA</h1>", unsafe_allow_html=True)
    auth.login()
    st.stop() # Arrête le code ici tant qu'on n'est pas connecté

# --- INITIALISATION ---
user_email = st.session_state.get('user_info', {}).get('email', 'Utilisateur Inconnu')

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

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/avatar_anonymous_120dp.png", width=50)
    st.write(f"📧 {user_email}")
    st.divider()
    
    # Section Paiement & Activation
    if not st.session_state.is_pro:
        st.subheader("💎 DEVENIR PRO+")
        st.error("Options Photo/Vidéo Verrouillées")
        st.write("---")
        st.write("📲 *PAIEMENT :*")
        st.write("✅ *MonCash :* +509 4769-2489")
        st.write("✅ *Natcash :* +509 4208-7977")
        code_activation = st.text_input("Entrez le code reçu (234)", type="password")
        if code_activation == "234":
            st.session_state.is_pro = True
            st.success("Mode PRO+ activé !")
            st.rerun()
    
    st.divider()
    # Section Admin (1234)
    admin_code = st.text_input("⚙️ Accès PDG Karl", type="password")
    if admin_code == "1234":
        st.warning("📊 STATISTIQUES NEXA")
        st.write(f"Dernier utilisateur connecté : {user_email}")
        st.write("Serveur : Google Cloud / Gemini 1.5")

# --- INTERFACE PRINCIPALE ---
st.markdown(f"<h1 style='text-align:center; color:#4285F4;'>NEXA AI</h1>", unsafe_allow_html=True)

if st.session_state.is_pro:
    st.subheader("📸 Caméra & Analyse Vision")
    camera = st.camera_input("Scanner un document")
    if camera:
        # Code d'analyse Gemini ici...
        st.write("Analyse en cours...")
else:
    st.info("Bonjour ! Vous utilisez la version gratuite. Passez en PRO+ pour utiliser la caméra.")

# CHAT
if prompt := st.chat_input("Posez votre question..."):
    st.chat_message("user").write(prompt)
    response = model.generate_content(prompt)
    st.chat_message("assistant").write(response.text)
    parler(response.text)
