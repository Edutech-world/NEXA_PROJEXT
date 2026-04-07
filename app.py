import streamlit as st
import google.generativeai as genai
import urllib.parse

# --- 1. CONFIGURATION DU CERVEAU GOOGLE ---
# Cette ligne ira chercher la clé que tu as mise dans les "Secrets" de Streamlit
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ Erreur : La clé GOOGLE_API_KEY est introuvable dans les Secrets.")

# --- 2. DESIGN "NEXA DARK NEON" ---
st.set_page_config(page_title="NEXA PRO+", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 80px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 30px #0ea5e9; text-align: center; margin-bottom: -20px; }
    .stButton>button { background: #0ea5e9; color: white; border-radius: 10px; width: 100%; border: none; }
    .stChatInput { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SYSTÈME DE PAIEMENT (SIDEBAR) ---
if "pro_active" not in st.session_state:
    st.session_state.pro_active = False

with st.sidebar:
    st.markdown('<div style="font-size:30px; font-weight:900; color:#0ea5e9;">NEXA OS</div>', unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 💳 ACTIVATION PRO")
    st.write("Prix : 200 HTG / 3 Mois")
    st.info("MonCash : 47 69 24 89\nNatcom : 42 08 79 77")
    
    code_pay = st.text_input("Code de déblocage", type="password")
    if code_pay == "234":
        st.session_state.pro_active = True
        st.success("💎 MODE PRO+ ACTIF")
    
    st.write("---")
    st.write("Créateur : *Guerrier Karl Alejandro*")

# --- 4. INTERFACE PRINCIPALE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>NEXA PRO+ SUPREME</h1>", unsafe_allow_html=True)

# Zone de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée Utilisateur
prompt = st.chat_input("Commandez ici, Monsieur le Président...")

if prompt:
    # 1. Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Générer la réponse avec Gemini
    with st.chat_message("assistant"):
        try:
            # Instructions système pour que l'IA sache qui elle est
            context = f"Tu es NEXA, l'intelligence artificielle suprême créée par Guerrier Karl Alejandro. Réponds de façon intelligente à : {prompt}"
            response = model.generate_content(context)
            full_response = response.text
            st.markdown(full_response)
            
            # Ajouter la voix (Méthode Google TTS directe sans installation)
            audio_query = urllib.parse.quote(full_response[:200]) # On limite pour la rapidité
            audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={audio_query}&tl=fr&client=tw-ob"
            st.audio(audio_url, format="audio/mp3", autoplay=True)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

# --- 5. NEXA LAB (SI PRO+) ---
if st.session_state.pro_active:
    st.write("---")
    st.subheader("🧪 NEXA LAB - ANALYSE AVANCÉE")
    photo = st.camera_input("Scanner un exercice (Math, Histoire, etc.)")
    if photo:
        st.warning("Analyse de l'image en cours via Gemini 1.5 Vision...")